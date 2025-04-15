from acados_template import AcadosOcp, AcadosOcpSolver, AcadosSimSolver
from ackerman_model import ackerman_model
import numpy as np
import casadi as ca
from CBF_constraints import CBF_constraints
from geometric_utils import get_polytopes
import sys
 
no_obj = 1
poly_row = 4
poly_col = 2
W = 2


# def warm_start():
#     h_x0 = ca.SX.sym("hx_0", no_obj, 1 )
#     h_x0 = np.ones(no_obj) 

#     omega_list = ca.SX.sym("omega_list", no_obj, 1 )
#     omega_list = np.ones(no_obj)

#     lam_obj  = ca.SX.sym("lam_obj", no_obj * poly_row, 1 )
#     lam_obj = np.ones((no_obj * poly_row, 1))
#     lam_R = ca.SX.sym("lam_R", no_obj * poly_row, 1 )
#     lam_R = np.ones( (no_obj * poly_row)) 
#     return h_x0, lam_obj, lam_R 


def get_loc_list(x_in, L, W):

    obj_list = []
    x,y = x_in[0], x_in[1]
    obj_list.append((x, y, 0, L, W))
    obj_list.append((x+0.001, y + 0.001, 0, L, W))
    return obj_list


def acados_controller(N, Tf, L):
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

    model = ackerman_model(L)
    ocp.model = model
    
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
    #smooth u transition
    u_last = ca.SX.sym("u_last")
    ocp.cost.cost_type = 'NONLINEAR_LS'
    ocp.cost.yref = np.array([0.,0,0,0,0,0, 0] )
    del_error = ca.vertcat(model.x, model.u)- ocp.cost.yref
    u_delta = u_last - ocp.model.u
    
    #print(loss)
    #print(u_delta)
    ocp.model.cost_y_expr =  ca.vertcat(model.x, model.u)- ocp.cost.yref #ca.vertcat(del_error, u_delta)
    #ocp.cost.yref = np.zeros((nx+nu,))    
    ocp.cost.W = unscale * ca.diagcat(Q_mat, R_mat).full()

    # terminal cost
    ocp.cost.cost_type_e = 'NONLINEAR_LS'
    ocp.cost.yref_e = np.array([0., 0, 0, 0])
    cost = model.x - ocp.cost.yref_e
    ocp.model.cost_y_expr_e = cost #model.x # 
    ocp.cost.W_e = unscale * Q_emat
    
    # set constraints
    #constraints on control input    
    ocp.constraints.lbu = np.array([min_vel, min_str_angle_in, min_str_angle_out])
    ocp.constraints.ubu = np.array([max_vel, max_str_angle_in, max_str_angle_out])
    ocp.constraints.idxbu = np.array([0,1,2])

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
    CBF_obj = CBF_constraints(loc_list, x, u, Tf/N, L )
    #CBF_constraints.warm_start()
    h_list, h_lb_list, h_ub_list = CBF_obj.get_cbf_constraints() 

    print("printing sizes")
    print(h_list.shape)

    print("lh ")
    print(h_lb_list.shape)

    print("uh")
    print(h_ub_list.shape)

    ocp.model.con_h_expr =h_list
    ocp.dims.nh = h_list.shape[0]
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