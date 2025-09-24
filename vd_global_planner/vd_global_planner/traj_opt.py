import numpy as np
from scipy.interpolate import CubicSpline
from scipy import sparse

from matplotlib import pyplot as plt
import osqp
from scipy.interpolate import make_interp_spline, interp2d

class Trajecotry():
    def __init__(self, v_min, v_max, a_min, a_max, lat_acc_a_max):       
        self.track_length = None 
        self.eps = 1e-12
        self.v_min = v_min
        self.v_max = v_max
        self.a_min = a_min 
        self.a_max = a_max
        self.lat_acc_a_max = lat_acc_a_max 


    def create_path_funs(self, path_array):
        ##waypoints = [x, y, theta, kappa, s_length, speed]
        """
        path : 2d array with n * 2 dimension
        """   
        print("creating path fun")
        waypoints = []       
# 

        # for i in range(len(path_array)):           
        #     x = path_array[i,0]  
        #     y = path_array[i,1]  
        #     yaw =  path_array[i,2]           
        #     dist = path_array[i,3]
        #     vel = path_array[i,4 ]
        #     steer = path_array[i, 5]
        #     s_len_curr = dist + s_len_curr
        #     if i== 0:
        #         kappa = 0
        #     else:                        
        #         kappa = (yaw - last_yaw) / dist

        #     last_yaw = yaw
                       
        #     x, y = path_array[i,0:2]           
        #     waypoints.append([x,y,yaw, kappa, s_len_curr, vel, steer])
               
        self.track_length = path_array[-1, 3]

            
        self.waypoints = path_array #np.array( waypoints)   
        print("before interpolation")
        self.interploate()

    def get_interpld_path(self):
        s_min, s_max = 0, self.track_length
        s_points = np.linspace(0,self.track_length, 20000 )
        points = self.traj_interpld(s_points)
        print("points", points[:, 0:2]) 
        return points
        

    def interploate(self):              
            
        #print("s_len",self.waypoints[0:50, 3])
        #s_len = self.waypoints[:, 3]
        
        # vals, first_idx, counts = np.unique(s_len, return_index=True, return_counts=True)
        # dup_vals = vals[counts > 1]        
        # dup_indices = [np.where(s_len == v)[0] for v in dup_vals]

        # print("dup_indices ", dup_indices)

        #self.traj_interpld = make_interp_spline(self.waypoints[:, 3], self.waypoints[:, 0:3], k=5)  
        
         
        self.traj_interpld = CubicSpline(self.waypoints[:, 3], self.waypoints[:, 0:3], extrapolate=False)
        
        #testing
        
    def compute_speed_profile(self):
        #optimization horizon
        N = self.waypoints.shape[0]

        #constraints
        a_min = np.ones(N-1) * self.a_min
        a_max = np.ones(N-1) * self.a_max
        v_min = np.ones(N) * self.v_min
        v_max = np.ones(N) * self.v_max
        ay_max = self.lat_acc_a_max
        

        # Inequality Matrix
        D1 = np.zeros((N-1, N))

        # Iterate over horizon
        for i in range(N-1):
            #Get information about current waypoint
            current_waypoint = self.waypoints[i]
            next_waypoint = self.waypoints[i+1]
            delta_wp = next_waypoint[0:2] - current_waypoint[0:2]
            # distance between waypoints
            li = np.linalg.norm(delta_wp)
            # curvature of waypoint
            ki = current_waypoint[3]

            # Fill operator matrix
            # dynamics of acceleration
            if i < N-1:
                D1[i, i:i+2] = np.array([-1/(2*li), 1/(2*li)])

            # Compute dynamic constraint on velocity
            v_max_dyn = np.sqrt(ay_max / (np.abs(ki) + self.eps))
            if v_max_dyn < v_max[i]:
                v_max[i] = v_max_dyn 

            # Construct inequality matrix
            D1 = sparse.csc_matrix(D1)
            D2 = sparse.eye(N)
            D = sparse.vstack([D1, D2], format='csc')

            # Get upper and lower bound vectors for inequality constraints
            l = np.hstack([a_min, v_min])
            u = np.hstack([a_max, v_max])

            # Set cost matrices
            P = sparse.eye(N, format='csc')
            q = -1 * v_max

            # Solve optimization problem
            problem = osqp.OSQP()
            problem.setup(P=P, q=q, A=D, l=l, u=u, verbose=False)
            speed_profile = problem.solve().x

            for i, wp in enumerate(self.waypoints):
                self.waypoints[i, -1]=  speed_profile[i] 
                print("speeed", speed_profile[i] )
            speed_profile = problem.solve().x
            self.waypoints[-1, -1]=  speed_profile[-1]

        
        # N = self.waypoints.shape[0]

        # a_min = np.ones(N-1) * self.a_min
        # a_max = np.ones(N-1) * self.a_max
        # v_min = np.ones(N) * self.v_min
        # v_max = np.ones(N) * self.v_max
        # ay_max = self.lat_acc_a_max

        # D1 = np.zeros((N-1, N))

        # for i in range(N-1):
        #     current = self.waypoints[i]
        #     next_ = self.waypoints[i+1]
        #     delta = next_[:2] - current[:2]
        #     li = np.linalg.norm(delta)
        #     ki = current[3]

        #     if li > self.eps:
        #         D1[i, i:i+2] = np.array([-1/(2*li), 1/(2*li)])

        #     # Apply dynamic velocity constraint from lateral acceleration
        #     v_max_dyn = np.sqrt(ay_max / (np.abs(ki) + self.eps)) if ay_max > 0 else self.v_max
        #     v_max[i] = min(v_max[i], v_max_dyn)

        # # Build inequality constraint matrices
        # D = sparse.vstack([
        #     sparse.csc_matrix(D1),      # acceleration constraints
        #     sparse.eye(N)               # speed bounds
        # ], format='csc')

        # l = np.hstack([a_min, v_min])
        # u = np.hstack([a_max, v_max])

        # # Cost: maximize speed (minimize -v)
        # P = sparse.eye(N, format='csc') * 1e-6  # small regularization
        # q = -1.0 * v_max

        # problem = osqp.OSQP()
        # problem.setup(P=P, q=q, A=D, l=l, u=u, verbose=False)
        # result = problem.solve()

        # speed_profile = result.x
        # self.waypoints[:, -1] = speed_profile

        
    def plot_path(self):
        s_range = np.linspace(0, len(self.waypoints[:, -1]), 100)
        points = self.traj_interpld(s_range)
        plt.plot(points[:,0], points[:,1])
        plt.show()

    def plot_speed_profile(self):
        plt.plot(range(self.waypoints.shape[0]), self.waypoints[:, -1])
        plt.show()



    