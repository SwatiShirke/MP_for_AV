import casadi as ca
import numpy as np

def cal_state_cost(state_vec, ref_vec, weights, prev_state, state_rate_weight):
    pos_cost = ca.dot((ref_vec[0:2] - state_vec[0:2])**2, weights[0:2])
    vel_cost = (ref_vec[3] - state_vec[3])**2 * weights[3]
    yaw_cost =  ( 1 - np.cos(ref_vec[2] - state_vec[2]))**2  * weights[2]
    cost = (pos_cost + vel_cost ) + yaw_cost
    #state_change_cost = ca.fabs(prev_state[2] - state_vec[2]) < 0.035
    #ipdb.set_trace()    
    return cost 



def cal_input_cost(input_vec, ref_vec, weights, prev_in, control_rate_weight):
    cost = ca.dot((ref_vec - input_vec)**2, weights)      
    rate_cost = ca.dot((prev_in - input_vec)**2, control_rate_weight)
    return cost + rate_cost



def get_loc_list(x_in, L, W, pl_margin):
    obj_list = []
    x,y = x_in[0], x_in[1]
    obj_list.append((x, y, 0, L, W))
    obj_list.append((x+ 2.0, y+ 2.0, 0, L, W))
    return obj_list



def get_dist_constraints(x_array, u_input, ref_params,vd_L, vd_W, no_of_obs, param_window, d_safe, d_th):
    
    half_l_vd = (vd_L)/2 
    half_w_vd = vd_W /2 
    diag_vd  = ca.sqrt(half_l_vd**2 + half_w_vd**2)    
    
    print(" ")
    print("x_array", x_array)     

    obs_params = ref_params
    constraints_list = []
    for i in range(no_of_obs):
        curr_obs_params = obs_params[i * param_window: i * param_window + param_window ]
        #print("curr_obs_params ", curr_obs_params)
        obs_L, obs_W = curr_obs_params[4], curr_obs_params[5]
        half_l_obs = obs_L/2
        half_w_obs = obs_W /2 
        diag_w = ca.sqrt(half_l_obs**2 + half_w_obs**2)

        # current distance 
        dist = ca.norm_2(curr_obs_params[0:2] - x_array[0:2] )
        h_xi = dist**2  - (diag_w + diag_vd + d_safe)**2
        is_obs_abscent_or_far =   ca.logic_or(ca.logic_and(obs_L== 0 , obs_W == 0), dist >= d_th)
        h_xi =  ca.if_else(is_obs_abscent_or_far, 0 , h_xi) 
        constraints_list = ca.vertcat(constraints_list, -h_xi)

    return constraints_list 

