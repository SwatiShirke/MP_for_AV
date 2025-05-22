from acados_template import AcadosOcp, AcadosOcpSolver, AcadosSimSolver
from ackerman_model import ackerman_model
import numpy as np
import casadi as ca
from CBF_constraints import CBF_constraints
from geometric_utils import get_polytopes
import sys
from utils import cal_state_cost, cal_input_cost, get_loc_list

 
no_obj = 1
poly_row = 4
poly_col = 2
W = 2


def get_loc_list(x_in, L, W):
    obj_list = []
    x,y = x_in[0], x_in[1]
    obj_list.append((x, y, 0, L, W))
    obj_list.append((x+0.001, y + 0.001, 0, L, W))
    return obj_list 


def acados_controller(N, Tf, L, pl_margin, d_safe , KNN):
    #model configs param
    # N = params.N
    # Tf = params.Tf
    
    # create ocp object to formulate the OCP
    ocp = AcadosOcp()
    # set model
    
    min_vel = 0
    max_vel = 45
    min_str_angle_in= -0.615
    max_str_angle_in = 0.615
    min_str_angle_out = -0.75
    max_str_angle_out = 0.75
    dthrottle_min = 0
    dthrottle_max = 5
    ddelta_min = -0.5    
    ddelta_max = 0.5

    model = ackerman_model(L, KNN)
    ocp.model = model
    ocp.dims.np = ocp.model.p.size()[0]
    ocp.parameter_values = np.zeros(ocp.dims.np)
    
    #ipdb.set_trace()
    nx = model.x.rows()
    nu = model.u.rows()

    # set prediction horizon
    ocp.solver_options.N_horizon = N
    ocp.solver_options.tf = Tf

    

    #cost matricesq
    Q_mat = 1*np.diag([10e1, 10e1, 100e1, 1e1 ])
    R_mat = 1*np.diag([1e-2, 1e-2, 1e-2])
    Q_emat = 1*np.diag([100e1, 100e1, 100e1, 1e1 ]) 
    unscale = N / Tf 

     
    # path cost
    # smooth u transition
    # u_last = ca.SX.sym("u_last")
    # ocp.cost.cost_type = 'NONLINEAR_LS'
    # ocp.cost.yref = np.array([0.,0,0,0,0,0, 0] )
    # del_error = ca.vertcat(model.x, model.u)- ocp.cost.yref
    # u_delta = u_last - ocp.model.u

    #cost matricesq
    # x, y, yaw, pitch, roll, vel
    Q_mat = unscale * ca.vertcat(100,100,100, 100)
    R_mat = unscale * ca.vertcat( 1e-8, 1e-8, 1e-8)
    Q_emat =  unscale * ca.vertcat(1000,1000,1000, 100) 
    control_rate_weight = ca.vertcat(1000,1000,1000)
    state_rate_weight = ca.vertcat(0, 0, 100, 0)
    prev_in = ca.vertcat(0,0,0)
    prev_state = ca.vertcat(0,0,0,0)

    x_array = model.x
    u_aaray = model.u 
    ref_array = model.p  # x, y, qw, qx,qy,qz, v, acc, del1, del2

    state_error = cal_state_cost(x_array, ref_array, Q_mat, prev_state, state_rate_weight)    
    input_error = cal_input_cost(u_aaray[0:3], ref_array[4:7], R_mat, prev_in, control_rate_weight) 
    
    ocp.cost.cost_type = 'EXTERNAL'
    ocp.model.cost_expr_ext_cost = state_error + input_error 
    ocp.model.cost_expr_ext_cost_0 = state_error  + input_error      

    state_error = cal_state_cost(x_array, ref_array, Q_emat, prev_state, state_rate_weight)    
    ocp.cost.cost_type_e = 'EXTERNAL'
    ocp.model.cost_expr_ext_cost_e = state_error 
    
    # set constraints
    #constraints on control input  
    lbx = np.zeros(nu)
    lbx[0:3] = min_vel, min_str_angle_in, min_str_angle_out    
    ubx = np.ones(nu) * 100
    ubx[0:3] = max_vel, max_str_angle_in, max_str_angle_out
    indices = np.arange(nu)  
    ocp.constraints.lbu = lbx
    ocp.constraints.ubu = ubx
    ocp.constraints.idxbu = indices 

    #initial state contraints
    ocp.constraints.x0 = np.array([0, 0, 0, 0] )

    #lower and upper bound constraints on states - velocity and angular velocities
    ocp.constraints.lbx = np.array([])
    ocp.constraints.ubx = np.array([])
    ocp.constraints.idxbx = np.array([] )


    W = 2.0
    loc_list = get_loc_list(model.x, L, W) 
    x = model.x   
    u = model.u

    CBF_obj = CBF_constraints( Tf/N, L, W , d_safe, pl_margin, nx, nu )   
    #CBF_obj.external_warm_start()
    h_list, h_lb_list, h_ub_list = CBF_obj.get_cbf_constraints(model.x, model.u, model.p) 

    # print("printing sizes")
    # print(h_list.shape)

    # print("lh ")
    # print(h_lb_list.shape)

    # print("uh")
    # print(h_ub_list.shape)

    ocp.model.con_h_expr =h_list
    ocp.dims.nh = len(h_lb_list)
    ocp.constraints.lh = h_lb_list          # lower bound
    ocp.constraints.uh = h_ub_list            # Upper bound 
    ocp.model.lh = h_lb_list         # lower bound
    ocp.model.uh = h_ub_list


    # set QP solver and integration
    ocp.solver_options.tf = Tf
    #ocp.solver_options.qp_solver = 'FULL_CONDENSING_QPOASES'
    ocp.solver_options.qp_solver = "PARTIAL_CONDENSING_HPIPM"
    ocp.solver_options.nlp_solver_type = "SQP_RTI"
    ocp.solver_options.hessian_approx = "GAUSS_NEWTON"
    ocp.solver_options.integrator_type = "ERK"
    ocp.solver_options.sim_method_num_stages = 4
    ocp.solver_options.sim_method_num_steps = 3
    ocp.solver_options.qp_solver_warm_start = 1


    # create solver
    acados_solver = AcadosOcpSolver(ocp, json_file="acados_ocp.json")
    acados_integrator = AcadosSimSolver(ocp, json_file = "acados_ocp.json")

    return model, acados_solver, acados_integrator