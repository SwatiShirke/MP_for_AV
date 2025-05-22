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


def get_loc_list( L, W, x0 ):
    obj_list = []    
    obj_list.append([x0[0], x0[1], 0, L, W])
    return np.array(obj_list)

def create_polytope( L, W):
        A_mat = np.array([[-1,0], [0, -1], [1, 0], [0, 1]])
        B_mat = np.array([L/2, W/2, L/2, W/2])
        return A_mat, B_mat

# def create_polytope(L, W, origin):
#         x = origin[0]
#         y = origin[1]
#         A_mat = np.array([[-1,0], [0, -1], [1, 0], [0, 1]])
#         B_mat = np.array([-x + L/2, -y + W/2, x + L/2, y +W/2])
#         return A_mat, B_mat

# def create_vd_polytope( L, W):       
#         A_mat = np.array([[-1,0], [0, -1], [1, 0], [0, 1]])
#         B_mat = np.array([L/2,  W/2,L/2, W/2])
#         return A_mat, B_mat

def get_transofrmation( x,y, theta):
    obj_pos = np.array([x, y])
    R_obj = np.array([[ca.cos(theta), -ca.sin(theta)],
                      [ca.sin(theta), ca.cos(theta)] ]) 
    return obj_pos, R_obj


def warm_start( L, W, x_current, object_list):
        print("starting warm start")
        A_bot, B_bot = create_polytope(L, W) 
        P_bot, R_bot = get_transofrmation(x_current[0], x_current[1], x_current[2])

        # print("A_bot", A_bot)
        # print("B_bot", B_bot)


        # print("P_bot", P_bot )
        # print("R_bot", R_bot)
        A_bot = ca.mtimes(A_bot, ca.transpose(R_bot))
        B_bot = ca.mtimes(ca.mtimes(A_bot, ca.transpose(R_bot)), P_bot) + B_bot

        # print("A_bot_W", A_bot)
        # print("B_bot_W", B_bot)
                
        hx0_list = []
        lamb_bot_list = []
        lamb_obj_list = []
        
        for i in range(len(object_list)):
            x_obj, y_obj, theta_obj, L, W = object_list[i]
            #print("x_obj, y_obj, theta_obj, L, W", x_obj, y_obj, theta_obj, L, W)
            A_obj, B_obj = create_polytope(L, W)
            P_obj, R_obj = get_transofrmation(x_obj, y_obj, theta_obj)
            # print("A_obj", A_obj)
            # print("B_obj", B_obj)
            # print("P_obj", P_obj)
            # print("R_obj", R_obj)
            A_obj = ca.mtimes(A_obj, ca.transpose(R_obj))
            B_obj = ca.mtimes(ca.mtimes(A_obj, ca.transpose(R_obj)), P_obj) + B_obj

            # print(A_obj, A_obj)
            # print("B_obj", B_obj)
            point1 = ca.SX.sym("point1",A_bot.shape[-1],1)
            point2 = ca.SX.sym("point2",A_obj.shape[-1],1)            
            x = ca.vertcat(point1, point2)
            cost=0   
            dist_vec = point1-point2
            cost = dist_vec.T@dist_vec 

            g = ca.vertcat(ca.mtimes(A_bot, point1) - B_bot,
                        ca.mtimes(A_obj, point2) - B_obj)
            
            nlp = {}
            nlp["f"] = cost
            nlp["g"] = g
            nlp["x"] = x
            #nlp["p"] = {x_pos, y_pos}
            option = {"verbose": False, "ipopt.print_level": 0, "print_time": 0}
            solver = ca.nlpsol("solver","ipopt",nlp,option) 

            sol = solver(lbg=-100,ubg=0)
            opt_x = sol["x"]
            opt_dist = ca.norm_2(opt_x[0:2]- opt_x[2:4]) #sol['f']
            #print(opt_dist)
            lamb_g = sol["lam_g"]
            lamb_bot = lamb_g[:A_bot.shape[0]]
            lamb_obj = lamb_g[A_obj.shape[0]:]

            if opt_dist>0:
                # lamb_bot = lamb_bot/2*opt_dist
                # lamb_obj = lamb_obj/2*opt_dist
                lamb_bot = lamb_bot/2*opt_dist
                lamb_obj = lamb_obj/2*opt_dist
            
            else:
                opt_dist=-1
                lamb_bot = np.zeros(shape = (A_bot.shape[0],))
                lamb_obj = np.zeros(shape = (A_obj.shape[0],))
            
            hx0_list.append(opt_dist)
            lamb_bot_list.append(lamb_bot)
            lamb_obj_list.append(lamb_obj)   

        return hx0_list, lamb_bot_list, lamb_obj_list