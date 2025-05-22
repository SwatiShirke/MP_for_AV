import numpy as np
import casadi as ca
from geometric_utils import get_polytopes 

class CBF_constraints():
    def __init__(self, Ts, L, W, d_safe, pl_margin, NX, NU):
        #loc_list - contains location, w, l (x,y,theta, L, W)
        self.loc_list = []
        self.x_current = None
        self.u_current = None
        self.d_safe = d_safe 
        self.pl_margin = pl_margin 
        self.no_object = 1   # VD + obstacles
        self.obj_list = None 
        self.polytope_row = 4   #2d polytopes hence        
        self.L = L
        self.W = W
        self.Ts = Ts         
        self.margin_dist = 0.0
        # ##call wamr start
        # self.warm_start()
        self.inf = 10e10    
        self.NX = NX 
        self.NU = NU
        self.params_WINDOW = 6 
        self.lambda_WINDOW = 8 
        self.input_offset = 3
        self.param_offset = 7 
         

    def create_location_list(self, params):        
        offset= self.NX + self.NU +1    
        for i in range(self.no_object):
            self.loc_list.append(params[(offset + i * self.Window_size) : offset + (i * self.Window_size) + self.Window_size ])
        print(self.loc_list)

    def create_sim_var(self):        
        ##create sim variables for lambda values, so that will get chnaged by optimizer in all shooting node
        #gets intialized only once by warm start
        #hx0(1), omega(1), lambda_bot (4,1) , lambda_obj (4,1) - for each obstacle 
        self.h_x0_list = ca.SX.sym("h_x0_list", self.no_object, 1 )
        self.omega_list = ca.SX.sym("omega_list", self.no_object, 1 )
        self.lamb_obj_list  = ca.SX.sym("lamb_obj_list", self.no_object * self.polytope_row, 1 )
        self.lamb_bot_list = ca.SX.sym("lamb_bot_list", self.no_object * self.polytope_row, 1 )
        self.gamma_list = ca.SX.sym("gamma_list", self.no_object, 1 )
        
     
    def get_robot_pose(self):
        x,y,theta = self.x_current[0], self.x_current[1], self.x_current[3]
         
        R_bot =  ca.hcat([
                        ca.vcat(
                            [
                                ca.cos(theta),
                                ca.sin(theta),
                            ]
                        ),
                        ca.vcat(
                            [
                                -ca.sin(theta),
                                ca.cos(theta),
                            ]
                        )])
        P_bot = ca.vertcat(x,y)
        self.R_bot = R_bot
        self.P_bot = P_bot
        return R_bot, P_bot
    

    def warm_start(self):
        print("starting warm start")
        A_bot, B_bot = self.obj_list[0].get_matrices()
        R_bot, P_bot = self.get_robot_pose() 
        ##rotate robot mat
        A_bot = ca.mtimes(A_bot, ca.transpose(R_bot))
        B_bot = ca.mtimes(ca.mtimes(A_bot, ca.transpose(R_bot)), P_bot) + B_bot
        hx0_list = []
        lamb_bot_list = []
        lamb_obj_list = []
        x = self.x_current
        for i in range(1, len(self.obj_list)):
            obj = self.obj_list[i]
            A_obj, B_obj = obj.get_matrices()
            point1 = ca.SX.sym("point1",A_bot.shape[-1],1)
            point2 = ca.SX.sym("point2",A_obj.shape[-1],1)            
            x = ca.vertcat(point1, point2, x)
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

            sol = solver(lbg=-ca.inf,ubg=0)
            opt_x = sol["x"]
            opt_dist = ca.sqrt(sol["f"])
            lamb_g = sol["lam_g"]
            lamb_bot = lamb_g[:A_bot.shape[0]]
            lamb_obj = lamb_g[A_obj.shape[0]:]

            if opt_dist>0:
                lamb_bot = lamb_bot/2*opt_dist
                lamb_obj = lamb_obj/2*opt_dist
            
            else:
                opt_dist=-1
                lamb_bot = np.zeros(shape = (A_bot.shape[0],))
                lamb_obj = np.zeros(shape = (A_obj.shape[0],))
            
            hx0_list.append(opt_dist)
            lamb_bot_list.append(lamb_bot)
            lamb_obj_list.append(lamb_obj)   

        self.h_x0_list = hx0_list
        self.lamb_bot_list = lamb_bot_list
        self.lamb_obj_list = lamb_obj_list 
    
    def external_warm_start(self):
        for i in range(self.no_object):
            obj_vec = self.loc_list[i]
            self.h_x0_list[i] = ca.sqrt(obj_vec[5])
            self.lamb_bot_list[i * self.no_lambda  :i * self.no_lambda + self.no_lambda] = obj_vec[6:10]
            self.lamb_obj_list[i * self.no_lambda  :i * self.no_lambda + self.no_lambda] = obj_vec[10:14]

        
    def create_polytope(self, L, W):
        # x = origin[0]
        # y = origin[1]
        A_mat = np.array([[-1,0], [0, -1], [1, 0], [0, 1]])
        #B_mat = np.array([-x + L/2, -y + W/2, x + L/2, y +W/2])
        B_mat = np.array([L/2,  W/2,L/2, W/2])
        return A_mat, B_mat
    
    def create_vd_polytope(self, L, W):       
        A_mat = np.array([[-1,0], [0, -1], [1, 0], [0, 1]])
        B_mat = np.array([L/2,  W/2,L/2, W/2])
        return A_mat, B_mat

    def get_transofrmation(self, x,y, theta):
        obj_pos = np.array([x, y])
        R_obj = np.array([[ca.cos(theta), -ca.sin(theta)],
                          [ca.sin(theta), ca.cos(theta)] ]) 
        return obj_pos, R_obj

    def vd_kinematic_model(self, x_state):
        ## continuous time kinematic model
        acc = self.u_current[0]
        steer_left = self.u_current[1]
        steer_right = self.u_current[2]
        steer = (steer_left + steer_right)/2
        x = x_state[0]
        y = x_state[1]
        theta = x_state[2]
        vel = x_state[3] 
        x_dt = vel * ca.cos(theta)
        y_dt = vel * ca.sin(theta)
        theta_dt = vel / self.L * ca.tan(steer)    
        vel_dt = acc
        dt = ca.vertcat(x_dt, y_dt, theta_dt, vel_dt)
        return dt

    def RK_45(self):
        k1 = self.vd_kinematic_model(self.x_current) 
        k2 = self.vd_kinematic_model(self.x_current + (self.Ts/2 * k1) )
        k3 = self.vd_kinematic_model(self.x_current + (self.Ts/2 * k2))
        k4 = self.vd_kinematic_model(self.x_current + (self.Ts * k3))
        x_next = self.x_current + 1/ 6 * (k1 +k2 +k3 + k4)* self.Ts
        return x_next

    # def get_cbf_constraints(self, x_current, u_current, params):
    #     # x = , x, y, theta, vel        
    #     # accel, steer left, steer right, 40 values in sequence (lambda bot + lambda_ob ) * no of objetc 
    #     self.x_current = x_current  
    #     self.u_current = u_current
    #     self.params = params 

    #     #self.obj_list - list of polytope objects, first element is VD obj
    #     h_list = []
    #     h_lb_list = []
    #     h_ub_list = []
    #     A_bot, B_bot = self.create_vd_polytope( self.L, self.W )
    #     # P_bot, R_bot = self.get_transofrmation(x_current[0], x_current[1], x_current[2])
    
    #     ##implement RK-45 here 
    #     x_next = self.RK_45()
    #     P_bot, R_bot = self.get_transofrmation(x_next[0], x_next[1], x_next[2])
    #     # A_bot_world = ca.mtimes(A_bot, R_bot.T)
    #     # B_bot_world = ca.mtimes (ca.mtimes(A_bot, R_bot.T), P_bot)  + B_bot 
                
    #     #for loop 
    #     for i in range(self.no_object):
    #         obj_info_array = self.params[i* self.params_WINDOW: i* self.params_WINDOW + self.params_WINDOW]
    #         obj_x = obj_info_array[0]
    #         obj_y = obj_info_array[1]
    #         obj_theta = obj_info_array[2]
    #         obj_L = obj_info_array[3]
    #         obj_W = obj_info_array[4] 
    #         cost = obj_info_array[5] 

    #         A_obj, B_obj = self.create_polytope(obj_L, obj_W, obj_info_array)             
    #         # P_obj, R_obj = self.get_transofrmation(obj_x, obj_y, obj_theta)            
    #         # A_obj_world = ca.mtimes(A_obj, R_obj.T)
    #         # B_obj_world = ca.mtimes (ca.mtimes(A_obj, R_obj.T), P_obj)  + B_obj

    #         lambda_val = self.u_current[self.input_offset + self.lambda_WINDOW *i : self.input_offset + self.lambda_WINDOW *i + self.lambda_WINDOW]
    #         #lambda_val = self.u_current[3 :11]
            
    #         lamb_bot = lambda_val[0:4]
    #         lamb_obj = lambda_val[4:8]
    #         omega =  self.u_current[-1] 
            
    #         hx_0 = cost
    #         self.gamma  = self.params[-1]    
            
    #         #print(lamb_bot)
    #         h_list  = ca.vertcat(h_list, lamb_bot) 
    #         h_lb_list.extend( np.zeros((self.polytope_row,1)))
    #         h_ub_list.extend( np.ones( (self.polytope_row,1)) * 10)

    #         h_list  = ca.vertcat(h_list, lamb_obj)
    #         h_lb_list.extend(  np.zeros((self.polytope_row,1)))
    #         h_ub_list.extend( np.ones( (self.polytope_row,1)) * 10)           

    #         ##main cbf constraint forward invariance
    #         cbf_h =  -ca.mtimes(ca.transpose(B_bot), lamb_bot) + ca.mtimes((ca.mtimes(A_obj, P_bot)  - B_obj).T,lamb_obj)
    #         -  (self.gamma * hx_0) 

    #         # cbf_h = -ca.mtimes(ca.transpose(B_bot_world), lamb_bot) - ca.mtimes(B_obj_world.T,lamb_obj)
    #         # - (self.gamma * hx_0) 

    #         h_list  = ca.vertcat(h_list, cbf_h)
    #         h_lb_list.extend(np.zeros((1,1)))
    #         h_ub_list.extend( np.ones( (1,1) )* 10)

    #         cbf_eq_h = ca.mtimes(A_bot.T, lamb_bot) +  ca.mtimes(ca.mtimes(R_bot.T,A_obj.T), lamb_obj)  
    #         #cbf_eq_h = ca.mtimes(A_bot_world.T, lamb_bot) + ca.mtimes(A_obj_world.T, lamb_obj) 
    #         h_list  = ca.vertcat(h_list, cbf_eq_h) 
    #         h_lb_list.extend( np.zeros((2,1)))
    #         h_ub_list.extend( np.zeros((2,1)))
    #         #h_ub_list.extend( np.ones((2,1))* 0.00001)

    #         temp_cbf_equ= ca.mtimes( A_obj.T, lamb_obj) 
    #         cbf_eq_2 = temp_cbf_equ.T @ temp_cbf_equ
    #         h_list  = ca.vertcat(h_list, cbf_eq_2)
    #         h_lb_list.extend( np.ones((1,1))  * -10)
    #         h_ub_list.extend( np.ones((1,1)))
        
    #     return h_list, np.array(h_lb_list), np.array(h_ub_list)


    def get_cbf_constraints(self, x_current, u_current, params):
            # x = , x, y, theta, vel        
            # accel, steer left, steer right, 40 values in sequence (lambda bot + lambda_ob ) * no of objetc 
            self.x_current = x_current  
            self.u_current = u_current
            self.params = params 

            #self.obj_list - list of polytope objects, first element is VD obj
            h_list = []
            h_lb_list = []
            h_ub_list = []
            A_bot, B_bot = self.create_polytope(self.L, self.W)
            # P_bot, R_bot = self.get_transofrmation(x_current[0], x_current[1], x_current[2])
            

            ##implement RK-45 here 
            x_next = self.RK_45()
            P_bot, R_bot = self.get_transofrmation(x_next[0], x_next[1], x_next[2])
            print("here")
            print("P_bot", P_bot)
            print("R_bot", R_bot)
            A_bot_world = ca.mtimes(A_bot, R_bot.T)
            B_bot_world = ca.mtimes (ca.mtimes(A_bot, R_bot.T), P_bot)  + B_bot 
                    
            #for loop 
            for i in range(self.no_object):
                obj_info_array = self.params[(self.param_offset + i* self.params_WINDOW): (self.param_offset + i* self.params_WINDOW + self.params_WINDOW)]
                obj_x = obj_info_array[0]
                obj_y = obj_info_array[1]
                obj_theta = obj_info_array[2]
                obj_L = obj_info_array[3]
                obj_W = obj_info_array[4] 
                cost = obj_info_array[5] 

                A_obj, B_obj = self.create_polytope(obj_L, obj_W)            
                P_obj, R_obj = self.get_transofrmation(obj_x, obj_y, obj_theta)            
                A_obj_world = ca.mtimes(A_obj, R_obj.T)
                B_obj_world = ca.mtimes (ca.mtimes(A_obj, R_obj.T), P_obj)  + B_obj

                lambda_val = self.u_current[self.input_offset + self.lambda_WINDOW *i : self.input_offset + self.lambda_WINDOW *i + self.lambda_WINDOW]
                #lambda_val = self.u_current[3 :11]
                
                lamb_bot = lambda_val[0:4]
                lamb_obj = lambda_val[4:8]
                omega =  self.u_current[-1]                 
                hx_0 = cost
                self.gamma  = self.params[-1]    
                
                #print(lamb_bot)
                h_list  = ca.vertcat(h_list, lamb_bot) 
                h_lb_list.extend( np.zeros((self.polytope_row,1)))
                h_ub_list.extend( np.ones( (self.polytope_row,1)) * 100)

                h_list  = ca.vertcat(h_list, lamb_obj)
                h_lb_list.extend(  np.zeros((self.polytope_row,1)))
                h_ub_list.extend( np.ones( (self.polytope_row,1)) *  100)           

                #main cbf constraint forward invariance
                # cbf_h = -ca.mtimes(ca.transpose(B_bot), lamb_bot) + ca.mtimes((ca.mtimes(A_obj, P_bot)  - B_obj_world).T,lamb_obj)
                # -  (self.gamma * hx_0) 

            
                # #- omega * self.gamma * (hx_0- self.margin_dist) + self.margin_dist
                cbf_h = -ca.mtimes(ca.transpose(B_bot_world), lamb_bot) - ca.mtimes(ca.transpose(B_obj_world),lamb_obj)
                - self.gamma * (hx_0- self.margin_dist) + self.margin_dist 
                h_list  = ca.vertcat(h_list, cbf_h)
                h_lb_list.extend(np.zeros((1,1)))
                h_ub_list.extend( np.ones( (1,1) )*  100)

                # #cbf_eq_h = ca.mtimes(A_bot.T, lamb_bot) + ca.mtimes(ca.mtimes(R_bot.T,A_obj.T), lamb_obj)  
                # cbf_eq_h =  ca.mtimes(A_bot_world.T, lamb_bot) + ca.mtimes(A_obj_world.T, lamb_obj)
                # h_list  = ca.vertcat(h_list, cbf_eq_h) 
                # h_lb_list.extend( np.zeros((2,1)))
                # h_ub_list.extend( np.zeros((2,1)))
                

                # temp_cbf_equ= ca.mtimes( A_obj_world.T, lamb_obj) 
                # cbf_eq_2 = temp_cbf_equ.T @ temp_cbf_equ
                # h_list  = ca.vertcat(h_list, cbf_eq_2)
                # h_lb_list.extend( np.zeros((1,1)))
                # h_ub_list.extend( np.ones((1,1))) 

                # hlist = ca.vertcat(h_list,omega)                
                # h_lb_list.extend(np.zeros((1,1)))
                # h_ub_list.extend(np.ones((1,1))*10) 
            
            return h_list, np.array(h_lb_list), np.array(h_ub_list)




