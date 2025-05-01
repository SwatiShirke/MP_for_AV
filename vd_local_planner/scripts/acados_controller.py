from acados_template import AcadosOcp, AcadosOcpSolver, AcadosSimSolver
from ackerman_model import ackerman_model
import numpy as np
import casadi as ca
from scipy.spatial.transform import Rotation as R
from CBF_constraints import CBF_constraints
from geometric_utils import get_polytopes
from ament_index_python.packages import get_package_share_directory 
import os
import sys
from vd_config import read_param
from utils import cal_state_cost, cal_input_cost, get_loc_list

def acados_controller(N, Tf, lf, lr, track_width, L, W,  pl_margin, d_safe, KNN):    
    # create ocp object to formulate the OCP
    ocp = AcadosOcp()      
    min_accel = -8.5
    max_accel = +2.5
    min_str_angle_in= -0.7
    max_str_angle_in = 0.7
    min_str_angle_out = -0.7
    max_str_angle_out = 0.7
    vel_min = 0
    vel_max = 30
    steer_rate = 0.01   #2.866242038 deg /sec
    yaw_rate = 0.1
    gamma = 0.8

    model = ackerman_model(lf, lr, KNN)
    ocp.model = model
    
    ocp.dims.np = ocp.model.p.size()[0]
    ocp.parameter_values = np.zeros(ocp.dims.np)

    #ipdb.set_trace()
    nx = model.x.rows()
    nu = model.u.rows()
        
    # set prediction horizon
    ocp.solver_options.N_horizon = N
    ocp.solver_options.tf = Tf
    unscale = 1
    #cost matricesq
    # x, y, yaw, pitch, roll, vel
    Q_mat = unscale * ca.vertcat(100,100,100, 100)
    R_mat = unscale * ca.vertcat( 1e-8, 1e-8, 1e-8)
    Q_emat =  unscale * ca.vertcat(1000, 1000,  1000, 100) 
    control_rate_weight = ca.vertcat(1000, 1000, 1000)
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
    lbx = np.zeros(nu-1)
    lbx[0:3] = min_accel, min_str_angle_in, min_str_angle_out
    ubx = np.ones(nu-1) * 1000
    ubx[0:3] = max_accel, max_str_angle_in, max_str_angle_out
    indices = np.arange(nu-1)
    # lbx = np.array([min_accel, min_str_angle_in, min_str_angle_out])
    # ubx = np.array([max_accel, max_str_angle_in, max_str_angle_out])
    # indices = np.array([0,1,2])
    ocp.constraints.lbu = lbx
    ocp.constraints.ubu = ubx 
    ocp.constraints.idxbu = indices  

    #initial state contraints
    ocp.constraints.x0 = np.array([0, 0, 0, 0] )

    #lower and upper bound constraints on states - velocity and angular velocities
  
    ocp.constraints.lbx = np.array([-2* np.pi ,vel_min])
    ocp.constraints.ubx = np.array([2 * np.pi, vel_max])
    ocp.constraints.idxbx = np.array([2,3] )   
        
    CBF_obj = CBF_constraints( Tf/N, L, W , d_safe, pl_margin, nx, nu)    
    #CBF_obj.external_warm_start()
    h_list, h_lb_list, h_ub_list = CBF_obj.get_cbf_constraints(model.x, model.u, model.p) 
    ocp.model.con_h_expr =h_list
    ocp.dims.nh = len(h_lb_list)
    ocp.constraints.lh = h_lb_list         
    ocp.constraints.uh = h_ub_list            
    ocp.model.lh = h_lb_list       
    ocp.model.uh = h_ub_list 


    ##update last states and input for rate control
    prev_in =  u_aaray 
    prev_state = x_array 

    # set QP solver and integration
    ocp.solver_options.tf = Tf
    #ocp.solver_options.qp_solver = 'FULL_CONDENSING_QPOASES'
    ocp.solver_options.qp_solver = "PARTIAL_CONDENSING_HPIPM"
    ocp.solver_options.nlp_solver_type = "SQP_RTI"
    ocp.solver_options.hessian_approx = "GAUSS_NEWTON"
    ocp.solver_options.integrator_type = "ERK"
    ocp.solver_options.sim_method_num_stages = 4
    ocp.solver_options.sim_method_num_steps = 3


    # create solver
    acados_solver = AcadosOcpSolver(ocp, json_file="acados_ocp.json")
    acados_integrator = AcadosSimSolver(ocp, json_file = "acados_ocp.json")

    return model, acados_solver, acados_integrator


if __name__ == "__main__":
    config_path = get_package_share_directory("vd_config") 
    vd_param_path =  os.path.join(config_path,'config', sys.argv[1])
    control_param_path = os.path.join(config_path, 'config', sys.argv[2])
    planner_param_path = os.path.join(config_path, 'config', sys.argv[3])

    read_param_obj = read_param.read_params()
    control_params = read_param_obj.read_params(control_param_path, "controller_params" )
    vd_params = read_param_obj.read_params(vd_param_path, "VD_params")
    planner_param = read_param_obj.read_params(planner_param_path, "planner_params")


    N = control_params.N
    Tf = control_params.Tf
    pl_margin = control_params.polytope_margin
    d_safe = control_params.d_safe
    lf = vd_params.lf
    lr = vd_params.lr
    track_width = vd_params.track_width
    L = vd_params.L
    W = vd_params.W
    KNN = planner_param.KNN


    
    
    model, acados_solver, acados_integrator = acados_controller(N, Tf, lf, lr, track_width, L, W, pl_margin, d_safe, KNN) 