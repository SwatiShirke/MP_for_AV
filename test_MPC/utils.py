import casadi as ca
import numpy as np

def cal_state_cost(state_vec, ref_vec, weights, prev_state, state_rate_weight):
    pos_cost = ca.dot((ref_vec[0:2] - state_vec[0:2])**2, weights[0:2])
    #dist_cost = (ref_vec[3] - state_vec[3])**2 * weights[3]
    yaw_cost =  ( 1 - np.cos(ref_vec[2] - state_vec[2]))**2  * weights[2]
    cost = pos_cost + yaw_cost #+ dist_cost
    #state_change_cost = ca.fabs(prev_state[2] - state_vec[2]) < 0.035
    #ipdb.set_trace()    
    return cost 

def cal_input_cost(input_vec, ref_vec, weights, prev_in, control_rate_weight, ):
    cost = ca.dot((ref_vec[0]- input_vec[0])**2, weights[0])      
    #rate_cost = ca.dot((prev_in - input_vec)**2, control_rate_weight)
    return cost #+ rate_cost 

def get_loc_list( L, W, x0 ):
    obj_list = []    
    obj_list.append([x0[0], x0[1], 0, L, W])
    return np.array(obj_list)

def create_polytope( L, W):
        A_mat = np.array([[-1,0], [0, -1], [1, 0], [0, 1]])
        B_mat = np.array([L/2, W/2, L/2, W/2])
        return A_mat.reshape(4,2), B_mat.reshape(4,1)


def create_vd_polytope( L, W):       
        A_mat = np.array([[-1,0], [0, -1], [1, 0], [0, 1]])
        B_mat = np.array([L/2,  W/2,L/2, W/2])
        return A_mat, B_mat

def get_transofrmation( x,y, theta):
    obj_pos = np.array([x, y])
    R_obj = np.array([[ca.cos(theta), -ca.sin(theta)],
                      [ca.sin(theta), ca.cos(theta)] ]) 
    return obj_pos.reshape(2,1), R_obj.reshape(2,2)


def get_dist_region_to_region(L, W, x_current, object_list): 
    print("starting warm start")
    A_bot, B_bot = create_polytope(L, W) 
    P_bot, R_bot = get_transofrmation(x_current[0], x_current[1], x_current[2])
    #print("P_bot", P_bot )
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

    opti = ca.Opti()
    # variables and cost
    point1 = opti.variable(A_bot.shape[-1], 1)
    point2 = opti.variable(A_obj.shape[-1], 1)
    cost = 0
    # constraints
    constraint1 = ca.mtimes(A_bot, point1) <= B_bot
    constraint2 = ca.mtimes(A_obj, point2) <= B_obj
    opti.subject_to(constraint1)
    opti.subject_to(constraint2)
    dist_vec = point1 - point2
    cost += ca.mtimes(dist_vec.T, dist_vec)
    # solve optimization
    opti.minimize(cost)
    option = {"verbose": False, "ipopt.print_level": 0, "print_time": 0}
    opti.solver("ipopt", option)
    opt_sol = opti.solve()
    # minimum distance & dual variables
    dist = opt_sol.value(ca.norm_2(dist_vec))
    if dist > 0:
        lamb_bot = opt_sol.value(opti.dual(constraint1)) / (2 * dist)
        lamb_obj = opt_sol.value(opti.dual(constraint2)) / (2 * dist)
    else:
        lamb_bot = np.zeros(shape=(A_bot.shape[0],1))
        lamb_obj = np.zeros(shape=(A_obj.shape[0],1))

    hx0_list.append(dist)
    lamb_bot_list.append(lamb_bot )
    lamb_obj_list.append(lamb_obj)
    cbf_h = -ca.mtimes(ca.transpose(B_bot), lamb_bot) - ca.mtimes(ca.transpose(B_obj),lamb_obj) 
    print("inside warm start cbf_h", cbf_h)
    return hx0_list, lamb_bot_list, lamb_obj_list


def warm_start( L, W, x_current, object_list):
        print("starting warm start")
        A_bot, B_bot = create_polytope(L, W) 
        P_bot, R_bot = get_transofrmation(x_current[0], x_current[1], x_current[2])


        #print("P_bot", P_bot )
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

            sol = solver(lbg=-np.inf,ubg=0)
            opt_x = sol["x"]
            print("opt_x", opt_x)
            opt_dist = ca.norm_2(opt_x[0:2]- opt_x[2:4]) #sol['f']
            #print(opt_dist)
            lamb_g = sol["lam_g"]
            lamb_bot = lamb_g[:A_bot.shape[0]]
            lamb_obj = lamb_g[A_obj.shape[0]:]

            if opt_dist>0:
                lamb_bot = lamb_bot/2*opt_dist
                lamb_obj = lamb_obj/2*opt_dist
                # lamb_bot =  0.125 * lamb_bot
                # lamb_obj = 0.125 * lamb_obj
            
            else:
                # opt_dist=-1
                lamb_bot = np.zeros(shape = (A_bot.shape[0],))
                lamb_obj = np.zeros(shape = (A_obj.shape[0],))
            
            hx0_list.append(opt_dist)
            lamb_bot_list.append(lamb_bot)
            lamb_obj_list.append(lamb_obj)  
            cbf_h = -ca.mtimes(ca.transpose(B_bot), lamb_bot) - ca.mtimes(ca.transpose(B_obj),lamb_obj) 
            print("inside warm start cbf_h", cbf_h)


        return hx0_list, lamb_bot_list, lamb_obj_list

def RK_45(x_current, u_current, Ts, L):
        k1 = vd_kinematic_model(x_current, u_current, L) 
        k2 = vd_kinematic_model(x_current + (Ts/2 * k1), u_current, L )
        k3 = vd_kinematic_model(x_current + (Ts/2 * k2), u_current, L)
        k4 = vd_kinematic_model(x_current + (Ts * k3), u_current, L)
        dt = 1/ 6 * (k1 + 2*k2 + 2*k3 + k4)
        print("dt", dt)
        x_next = x_current + dt * Ts 
        
        return x_next 

def vd_kinematic_model(x_state, u_current, L ):
        ## continuous time kinematic model
        vel = u_current[0]
        steer_left = u_current[1]
        steer_right = u_current[2]
        steer = (steer_left + steer_right)/2
        x = x_state[0]
        y = x_state[1]
        theta = x_state[2]
        dist = x_state[3] 
        x_dt = vel * ca.cos(theta)
        y_dt = vel * ca.sin(theta)
        theta_dt = vel / L * ca.tan(steer)    
        dist_dt = vel
        dt = ca.vertcat(x_dt, y_dt, theta_dt, dist_dt)
        return dt

def print_cbf_constraints( x_current, u_current, params, L, W, margin_dist, Ts, nx, nu):  
            # print("x_current", x_current)
            # print("u_current", u_current)
            params_WINDOW = 6 
            lambda_WINDOW = 8 
            input_offset = 3
            param_offset = nx + nu + 1                     
            polytope_row = 4

            #self.obj_list - list of polytope objects, first element is VD obj
            h_list = []
            h_lb_list = []
            h_ub_list = []
            A_bot, B_bot = create_polytope(L, W)            
            
            ##implement RK-45 here             
            x_next = RK_45(x_current, u_current, Ts, L)
            print("x_current", x_current)
            print("x_next",x_next)
            P_bot, R_bot = get_transofrmation(x_next[0], x_next[1], x_next[2])      
            A_bot_world = (A_bot @ R_bot.T)            
            B_bot_world = (A_bot_world) @ P_bot + B_bot
            # print("A_bot_world", A_bot_world)
            # print("B_bot_world", B_bot_world) 
                    
            #for loop 
            for i in range(1):
                obj_info_array = params[(param_offset + i* params_WINDOW): (param_offset + i*params_WINDOW + params_WINDOW)]
                #print("obj_info_array", obj_info_array)
                obj_x = obj_info_array[0]
                obj_y = obj_info_array[1]
                obj_theta = obj_info_array[2]
                obj_L = obj_info_array[3]
                obj_W = obj_info_array[4] 
                cost = obj_info_array[5] 

                print(obj_info_array)
                print("cost", cost)

                A_obj, B_obj = create_polytope(obj_L, obj_W)            
                P_obj, R_obj = get_transofrmation(obj_x, obj_y, obj_theta)                         
                A_obj_world = A_obj @ R_obj.T                
                B_obj_world = (A_obj @ R_obj.T) @ P_obj  + B_obj                            

                lambda_val = u_current[input_offset + lambda_WINDOW *i : input_offset + lambda_WINDOW *i + lambda_WINDOW]             
                lamb_bot = lambda_val[0:4].reshape(4,1)
                lamb_obj = lambda_val[4:8].reshape(4,1)

                
                omega =  u_current[-1]                             
                hx_0 = cost                
                gamma  = params[-1]    
                
                lamb_bot = ca.if_else(cost == 0,np.zeros(4),  lambda_val[0:4])
                lamb_obj = ca.if_else(cost == 0,np.zeros(4),  lambda_val[4:8]) 
                margin_dist = ca.if_else(cost == 0, 0, margin_dist)

                h_list  = ca.vertcat(h_list, lamb_bot) 
                h_lb_list = np.concatenate((h_lb_list, np.zeros(polytope_row)))
                h_ub_list = np.concatenate((h_ub_list,  np.ones(polytope_row) * 100))

                h_list  = ca.vertcat(h_list, lamb_obj)
                h_lb_list = np.concatenate((h_lb_list, np.zeros(polytope_row)))
                h_ub_list = np.concatenate((h_ub_list,  np.ones(polytope_row)* 100))        
                print("lamb_obj", lamb_obj)
                print("lamb_bot", lamb_bot)

                # #main cbf constraint forward invariance
                # cbf_h = -ca.mtimes(ca.transpose(B_bot), lamb_bot) + ca.mtimes((ca.mtimes(A_obj, P_bot)  - B_obj_world).T,lamb_obj) - omega * gamma * (hx_0) 
                # print("cbf_h", cbf_h)
                # print("B_bot_world", -ca.mtimes(ca.transpose(B_bot), lamb_bot))
                # print("B_obj_world", ca.mtimes((ca.mtimes(A_obj, P_bot)  - B_obj_world).T,lamb_obj))
                # print("B_bot", B_bot)
                # print("B_bot_world", B_bot_world)  
                             
                cbf_h = -ca.mtimes(ca.transpose(B_bot_world), lamb_bot) - ca.mtimes(ca.transpose(B_obj_world),lamb_obj) - omega * gamma * (hx_0) + margin_dist
                h_list  = ca.vertcat(h_list, cbf_h)
                h_lb_list = np.concatenate((h_lb_list, np.zeros(1))) 
                h_ub_list = np.concatenate((h_ub_list,  np.ones(1)*10))  
                print("B_bot_world", -ca.mtimes(ca.transpose(B_bot_world), lamb_bot) - ca.mtimes(ca.transpose(B_obj_world),lamb_obj) )
                # print("B_obj_world",- ca.mtimes(ca.transpose(B_obj_world),lamb_obj) )
                # print("omega", omega)
                # print("gamma", gamma)
                # print(- omega * gamma * (hx_0)) 
                print("cbf_h", cbf_h) 


                #cbf_eq_h = ca.mtimes(A_bot.T, lamb_bot) + ca.mtimes(ca.mtimes(R_bot.T,A_obj.T), lamb_obj)  
                cbf_eq_h =  ca.mtimes(A_bot_world.T, lamb_bot) + ca.mtimes(A_obj_world.T, lamb_obj)
                h_list  = ca.vertcat(h_list, cbf_eq_h) 
                h_lb_list = np.concatenate((h_lb_list, np.zeros(2)))
                h_ub_list = np.concatenate((h_ub_list,  np.zeros(2)))     
                # print("lamb_bot", lamb_bot)
                # print("lamb_obj", lamb_obj)  
                # print("A_bot_world", A_bot_world)
                # print("A_obj_world", A_obj_world)           
                print("cbf_eq_h", cbf_eq_h)                

                #temp_cbf_equ= ca.mtimes( A_obj.T, lamb_obj) 
                temp_cbf_equ= ca.mtimes( A_obj_world.T, lamb_obj) 
                cbf_eq_2 = temp_cbf_equ.T @ temp_cbf_equ
                h_list  = ca.vertcat(h_list, cbf_eq_2)
                h_lb_list = np.append(h_lb_list, 0)
                h_ub_list = np.append(h_ub_list,  1)
                print("cbf_eq_2", cbf_eq_2) 

                h_list = ca.vertcat(h_list,omega)                
                h_lb_list = np.append(h_lb_list, 0)
                h_ub_list = np.append(h_ub_list,   10)     

            return h_list, np.array(h_lb_list), np.array(h_ub_list)