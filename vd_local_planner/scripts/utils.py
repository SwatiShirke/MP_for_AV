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

