import numpy as np
import casadi as ca
from geometric_utils import get_polytopes 

class CBF_constraints():
    def __init__(self, loc_list, x_current, u_current, Ts, L, d_safe, pl_margin):
        # loc_list - contains location, w, l (x,y,theta, L, W)
        self.loc_list = loc_list
        self.x_current = x_current
        self.d_safe = d_safe 
        self.pl_margin = pl_margin 
        self.no_object = len(loc_list) - 1  # VD + obstacles
        self.obj_list = get_polytopes(self.no_object, loc_list)  
        self.polytope_row = 4   #2d polytopes hence
        self.u_current = u_current
        self.L = L
        self.Ts = Ts 
        self.create_sim_var()
        self.margin_dist = 1
        self.gamma_mul = 1
        ##call wamr start
        self.warm_start()
        self.inf = 10000


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
    
    def external_warm_start(self, model_params, nx, nu, np):
        ##read warm start values from params
        offset = nx + nu   ## ignore intial nx + nu params as they hold ref trajectory
        no_object =  model_params[offset]  
        ## for each object, we have hx0, lamb_bot, and lamb_obj coming from param - 1 + 4 + 4 = 
        step = self.polytope_row *2 + 1 
        lamb_w = self.polytope_row
        for i in range(no_object): 
            if (offset + 1 + i *step + step > np):
                break
            self.h_x0_list[i] = model_params[(offset +1) + step *i ]
            self.lamb_bot_list[i * lamb_w  :i * lamb_w + lamb_w] = model_params[(offset +2) + step *i : (offset +2) + lamb_w + step *i ]
            self.lamb_obj_list[i * lamb_w  :i * lamb_w + lamb_w] = model_params[(offset + 2 +lamb_w ) + step *i : (offset +2 + lamb_w) + lamb_w + step *i ]


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
        x_next = self.x_current + 1/ 6 * (k1 +k2 +k3 + k4)
        return x_next

    def get_cbf_constraints(self):
        "calculating constraints"
        #self.obj_list - list of polytope objects, first element is VD obj
        h_list = []
        h_lb_list = []
        h_ub_list = []

        vd_obj = self.obj_list[0]
        ##implement RK-45 here 
        x_next = self.RK_45()

        ##get A and B mat for new origin of VD
        A_bot, B_bot = vd_obj.get_matrices()

        
        #for loop 
        for i in range(0, self.no_object ):
            obj = self.obj_list[i+1]
            A_obj, B_obj = obj.get_matrices()
            size = A_obj.shape[0]

            # lamb_bot = lamb_bot_list[i-1*size: (i-1 * size) + size]
            # lamb_obj = lamb_obj_list[i-1*size: (i-1 * size) + size]
            lamb_bot = self.lamb_bot_list[i]
            lamb_obj = self.lamb_obj_list[i]
            omega = self.omega_list[i]
            gamma = self.gamma_list[i]
            hx_0 = self.h_x0_list[i]
            self.gamma_mul *= gamma 
            
            
            

            h_list  = ca.vertcat(h_list, lamb_bot) 
            h_lb_list.extend( np.zeros((self.polytope_row,1)))
            h_ub_list.extend( np.ones( (self.polytope_row,1)) * self.inf)


            h_list  = ca.vertcat(h_list, lamb_obj)
            h_lb_list.extend(  np.zeros((self.polytope_row,1)))
            h_ub_list.extend( np.ones( (self.polytope_row,1)) * self.inf) 


            ##main cbf constraint forward invariance  s
            cbf_h = -ca.mtimes(ca.transpose(B_bot), lamb_bot) + ca.mtimes((ca.mtimes(A_obj, self.P_bot)  - B_obj).T,lamb_obj)
            - (omega * self.gamma_mul * (hx_0 - self.margin_dist) + self.margin_dist) 

            h_list  = ca.vertcat(h_list, cbf_h)
            h_lb_list.extend(np.zeros((1,1)))
            h_ub_list.extend( np.full( (1,1), self.inf))

            cbf_eq_h = ca.mtimes(A_bot.T, lamb_bot) + ca.mtimes(ca.mtimes(self.R_bot,A_obj.T), lamb_obj)   
            h_list  = ca.vertcat(h_list, cbf_eq_h)
            h_lb_list.extend( np.zeros((2,1)))
            h_ub_list.extend( np.zeros((2,1)) )

            cbf_eq_2 = ca.mtimes(ca.transpose( A_obj) ,lamb_obj)
            h_list  = ca.vertcat(h_list, cbf_eq_2)
            h_lb_list.extend( np.ones((2,1))  * -self.inf)
            h_ub_list.extend( np.ones((2,1)) )

            return h_list, np.array(h_lb_list), np.array(h_ub_list)















        h_list = ca.vertcat(h_list, 1)

        return h_list