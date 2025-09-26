from acados_template import AcadosOcp, AcadosOcpSolver, AcadosSimSolver
from ackerman_model import ackerman_model
import numpy as np
import casadi as ca
from scipy.spatial.transform import Rotation as R
from utils import get_constraints

def cal_state_cost(state_vec, ref_vec, weights, prev_state, state_rate_weight):
    pos_cost = ca.dot((ref_vec[0:2] - state_vec[0:2])**2, weights[0:2])
    vel_cost = (ref_vec[3] - state_vec[3])**2 * weights[3]
    yaw_cost =  ( 1 - np.cos(ca.fabs(ref_vec[2] - state_vec[2])))**2  * weights[2]
    #yaw_cost = (ref_vec[2] - state_vec[2])**2 * weights[2]
    cost = pos_cost + yaw_cost + vel_cost       
    return cost 

def cal_input_cost(input_vec, ref_vec, weights, prev_in, control_rate_weight):
    cost = ca.dot((ref_vec - input_vec)**2, weights)      
    rate_cost = ca.dot((prev_in - input_vec)**2, control_rate_weight)
    return cost + rate_cost

def cal_cost_to_lane_center(ref_lane_center, x_array, param_weights):
    dx = ref_lane_center[0] - x_array[0]
    dy = ref_lane_center[1] - x_array[1]
    yaw = ref_lane_center[2]

    nx = ca.cos(yaw + ca.pi / 2.0)
    ny = ca.sin(yaw + ca.pi / 2.0)
    cost = ca.fabs(dx * nx + dy * ny)**2 * param_weights[0]

    #cost = (ref_lane_center[0] - x_array[0])**2  * param_weights[0] +   (ref_lane_center[1] - x_array[1])**2 * param_weights[1]
    return cost


def acados_controller(N, Tf, lf, lr, vd_width, no_of_obs, no_of_obs_params, input_offset, barrier_width):
    #model configs param
    # N = params.N
    # Tf = params.Tf
    
    # create ocp object to formulate the OCP
    ocp = AcadosOcp()
    # set model    
    min_accel = -8.5
    max_accel = +2.5
    min_str_angle_in= -0.7
    max_str_angle_in = 0.7
    min_str_angle_out = -0.7
    max_str_angle_out = 0.7
    vel_min = 0
    vel_max = 5
    steer_rate = 0.01   #2.866242038 deg /sec
    yaw_rate = 0.1

    

    model = ackerman_model(lf, lr, no_of_obs, no_of_obs_params, input_offset)
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
    # x, y, yaw,  vel, s_len
    Q_mat = unscale * ca.vertcat(10, 10,   10, 10)
    R_mat = unscale * ca.vertcat( 1e-8, 1e-8, 1e-8)
    Q_emat =  unscale * ca.vertcat(1000, 1000, 1000, 1000) 
    control_rate_weight = ca.vertcat(100, 100, 100)
    state_rate_weight = ca.vertcat(0, 0, 100, 0)
    param_weights = ca.vertcat(100, 100) 
    prev_in = ca.vertcat(0,0, 0)
    prev_state = ca.vertcat(0,0,0,0)

    x_array = model.x
    u_aaray = model.u 
    ref_array = model.p  # x, y, qw, qx,qy,qz, v, acc, del1, del2
    ref_states = ref_array[0:5]
    ref_u = ref_array[5:8]
    ref_params = ref_array[8:]   #lane center x, y, yaw + 30 params for 5 vehicles, 6 for each 
    # ref_lane_center = ref_params[0:3]
    state_error = cal_state_cost(x_array, ref_states, Q_mat, prev_state, state_rate_weight )    
    input_error = cal_input_cost(u_aaray, ref_u, R_mat, prev_in, control_rate_weight)  
    #cost_to_lane_center = cal_cost_to_lane_center(ref_lane_center, x_array, param_weights)
    

    ocp.cost.cost_type = 'EXTERNAL'
    ocp.model.cost_expr_ext_cost = state_error + input_error   #+ cost_to_lane_center
    ocp.model.cost_expr_ext_cost_0 = state_error  + input_error  #+ cost_to_lane_center  
    
    

    state_error = cal_state_cost(x_array, ref_array, Q_emat, prev_state, state_rate_weight)    
    ocp.cost.cost_type_e = 'EXTERNAL'
    ocp.model.cost_expr_ext_cost_e = state_error 

    
    
    # set constraints
    #constraints on control input    
    ocp.constraints.lbu = np.array([min_accel, min_str_angle_in, min_str_angle_out])
    ocp.constraints.ubu = np.array([max_accel, max_str_angle_in, max_str_angle_out])
    ocp.constraints.idxbu = np.array([0, 1, 2])

    #initial state contraints
    ocp.constraints.x0 = np.array([0, 0, 0, 0, 0] )

    #lower and upper bound constraints on states - velocity and angular velocities
    ocp.constraints.lbx = np.array([-2* np.pi ,vel_min])
    ocp.constraints.ubx = np.array([2 * np.pi, vel_max])
    ocp.constraints.idxbx = np.array([2,3] )
    
  
    ##inequality constrainst
    # h_list = get_constraints(x_array, ref_params, lf+lr, vd_width,  no_of_obs, no_of_obs_params, input_offset, barrier_width)
    # ocp.model.con_h_expr = h_list
    # ocp.dims.nh = h_list.shape[0]
    # ocp.constraints.lh = np.array([0,0,0,0,0])  #np.array([0,0,0])        # yaw rate, delta rate constraints
    # ocp.constraints.uh =  np.array([10,10,10,10,10])  #np.array([yaw_rate, steer_rate,state_error])             # Upper bound 
    # ocp.model.lh = np.array([0,0,0,0,0])# np.array([0,0,0])            # lower bound
    # ocp.model.uh = np.array([10,10,10,10,10]) #np.array([yaw_rate, steer_rate,state_error])  

    ##update last states and input for rate control
    prev_in =  u_aaray 
    prev_state = x_array

    # set QP solver and integration
    ocp.solver_options.tf = Tf
    #ocp.solver_options.qp_solver = 'FULL_CONDENSING_QPOASES'
    ocp.solver_options.qp_solver = "PARTIAL_CONDENSING_HPIPM"
    ocp.solver_options.nlp_solver_type = "SQP"
    ocp.solver_options.hessian_approx = "GAUSS_NEWTON"
    ocp.solver_options.integrator_type = "ERK"
    ocp.solver_options.sim_method_num_stages = 4
    ocp.solver_options.sim_method_num_steps = 3
    # ocp.solver_options.regularize_method     = 'CONVEXIFY'
    # ocp.solver_options.levenberg_marquardt   = 0.0000000001
    #ocp.solver_options.ext_cost_num_hess = 1


    # create solver
    acados_solver = AcadosOcpSolver(ocp, json_file="acados_ocp.json")
    acados_integrator = AcadosSimSolver(ocp, json_file = "acados_ocp.json")

    return model, acados_solver, acados_integrator


if __name__ == "__main__":
    N = 10
    Tf = 5
    lf = 2.56/2
    lr = 2.56/2
    no_of_obs = 5          # n obstalces in close vicinity are considered for collision avoidance 
    no_of_obs_params = 6   #x, y, yaw, vel, lenght, width
    input_offset = 3
    vd_width = 1.77
    barrier_width = 0.2
    #L =  2.5654
    model, acados_solver, acados_integrator = acados_controller(N, Tf, lf, lr,vd_width,  no_of_obs, no_of_obs_params, input_offset, barrier_width)