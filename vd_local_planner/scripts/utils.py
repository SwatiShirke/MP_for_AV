import numpy as np
import casadi as ca
import math

def check_collision(curr_obs_params, x_min_vd, x_max_vd, y_min_vd, y_max_vd):
    x_obs = curr_obs_params[0]
    y_obs = curr_obs_params[1]
    vel_obs = curr_obs_params[2]
    yaw_obs = curr_obs_params[3]
    L_obs =  curr_obs_params[4]
    W_obs = curr_obs_params[5] 

    half_l, half_w = L_obs /2, W_obs/2 

    R_mat_obs = ca.vertcat(
            ca.horzcat(ca.cos(yaw_obs), -ca.sin(yaw_obs)),
            ca.horzcat(ca.sin(yaw_obs),  ca.cos(yaw_obs))
            )
    
    
    corners_in_obs_frame = ca.vertcat(
                    ca.horzcat(x_obs + half_l, y_obs - half_w),
                    ca.horzcat(x_obs + half_l, y_obs + half_w),
                    ca.horzcat(x_obs - half_l, y_obs - half_w),
                    ca.horzcat(x_obs - half_l, y_obs + half_w) )
 
    #obs_corners_in_vd_world = (R_mat_obs @ corners_in_obs_frame.T).T + np.array([x_obs, y_obs])

    obs_corners_in_vd_world = (R_mat_obs @ corners_in_obs_frame.T).T + ca.repmat(ca.vertcat(x_obs, y_obs).T, corners_in_obs_frame.shape[0], 1)
    x_min_obs, x_max_obs, y_min_obs, y_max_obs  = get_min_max(obs_corners_in_vd_world)
    

    # if(x_min_vd < x_min_obs and x_max_vd < x_min_obs) or (x_min_vd > x_max_obs and x_max_vd > x_max_obs) or (y_min_vd < y_min_obs and y_max_vd < y_min_obs) or (y_min_vd > y_max_obs and y_max_vd > y_max_obs):
    #     return 1
    # else:
    #     return -1 

    cond = ca.logic_or(     ca.logic_or(
                            ca.logic_and(x_min_vd < x_min_obs, x_max_vd < x_min_obs),
                            ca.logic_and(x_min_vd > x_max_obs, x_max_vd > x_max_obs)
                        ),
                        ca.logic_or(
                            ca.logic_and(y_min_vd < y_min_obs, y_max_vd < y_min_obs),
                            ca.logic_and(y_min_vd > y_max_obs, y_max_vd > y_max_obs)
                        )
                        )

    result = ca.if_else(cond, 1, -1)
    return result

def get_min_max(points):
    x_obs, y_obs = points[:,0], points[:,1]
    x_min_obs = ca.fmin(ca.fmin(ca.fmin(x_obs[0], x_obs[1]), x_obs[2]), x_obs[3])
    x_max_obs = ca.fmax(ca.fmax(ca.fmax(x_obs[0], x_obs[1]), x_obs[2]), x_obs[3])

    y_min_obs = ca.fmin(ca.fmin(ca.fmin(y_obs[0], y_obs[1]), y_obs[2]), y_obs[3])
    y_max_obs = ca.fmax(ca.fmax(ca.fmax(y_obs[0], y_obs[1]), y_obs[2]), y_obs[3])

    return x_min_obs, x_max_obs, y_min_obs, y_max_obs

def get_constraints(x_array, ref_params,vd_L, vd_W, no_of_obs, param_window,  input_offset, barrier):    
    # 30 params for 5 nearby neighbours: , x, y, yaw, vel, lenght, width
    x_vd, y_vd, yaw_vd, vel, dist = x_array[0], x_array[1], x_array[2], x_array[3], x_array[4]

    R_mat = ca.vertcat(
            ca.horzcat(ca.cos(yaw_vd), -ca.sin(yaw_vd)),
            ca.horzcat(ca.sin(yaw_vd),  ca.cos(yaw_vd))
            )

    half_l = (vd_L)/2 + barrier
    half_w = vd_W /2 + barrier

    corners_in_vd_frame = ca.vertcat(
            ca.horzcat( x_vd + half_l, y_vd - half_w),
            ca.horzcat( x_vd + half_l, y_vd + half_w),
            ca.horzcat(x_vd - half_l, y_vd - half_w),
            ca.horzcat(x_vd - half_l, y_vd + half_w)
        )

    #vd_corners_in_vd_world = (R_mat @ corners_in_vd_frame.T).T + ca.horzcat(x_vd, y_vd)
    vd_corners_in_vd_world = (R_mat @ corners_in_vd_frame.T).T \
             + ca.repmat(ca.horzcat(x_vd, y_vd), corners_in_vd_frame.size1(), 1)

    
    # x_vd_w, y_vd_w = vd_corners_in_vd_world[:,0], vd_corners_in_vd_world[:,1]
    # x_min_vd, x_max_vd = ca.fmin(x_vd_w), ca.fmax(x_vd_w)
    # y_min_vd, y_max_vd = ca.fmin(y_vd_w), ca.fmax(y_vd_w)
    x_min_vd, x_max_vd, y_min_vd, y_max_vd =  get_min_max(vd_corners_in_vd_world)


    obs_params = ref_params[input_offset:]
    constraint_list = []
    for i in range(no_of_obs):
        curr_obs_params = obs_params[i * param_window: i * param_window + param_window ]  
        is_obs_not_present = ca.logic_and(curr_obs_params[4] == 0, curr_obs_params[5]==0)

         
        # if is_all_zero:
        #     is_no_collision = 1
        # else:
        #     is_no_collision = check_collision(curr_obs_params, x_min_vd, x_max_vd, y_min_vd, y_max_vd)  
        #is_no_collision = ca.if_else(is_obs_not_present, 1, check_collision(curr_obs_params, x_min_vd, x_max_vd, y_min_vd, y_max_vd) )

        is_no_collision = ca.if_else(is_obs_not_present, 1,- 1) 
        constraint_list = ca.vertcat(constraint_list, is_no_collision) 
        

    return constraint_list





