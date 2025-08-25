import numpy as np
from scipy.interpolate import CubicSpline
from scipy import sparse

from matplotlib import pyplot as plt
import osqp

class Trajecotry():
    def __init__(self, v_min, v_max, a_min, a_max, lat_acc_a_max):       
        self.track_length = None 
        self.eps = 1e-12
        self.v_min = v_min
        self.v_max = v_max
        self.a_min = a_min 
        self.a_max = a_max
        self.lat_acc_a_max = lat_acc_a_max 


    def create_path_funs(self, path):
        ##waypoints = [x, y, theta, kappa, s_length, speed]
        path_array = np.array([[tuple1[0], tuple1[1]] for tuple1 in path])
        print("creating path fun")
        waypoints = []
        last_del_y = 0
        s_len_curr = 0
        for i in range(len(path_array) -1):           
            curr_pt = path_array[i]
            next_pt = path_array[i+1]
            diff_pt = next_pt -curr_pt            
            yaw = np.arctan2(diff_pt[1], diff_pt[0]) #+ 2*np.pi) % (4*np.pi )  - 2*np.pi            
            dist = np.linalg.norm(diff_pt,2)

            s_len_next = dist + s_len_curr
            if i== 0:
                kappa = 0
            else:                        
                kappa = (yaw - last_yaw) / np.linalg.norm(last_diff,2)

            last_yaw = yaw
            last_diff = diff_pt            
            x, y = path_array[i,0], path_array[i,1]            
            waypoints.append([x,y,yaw, kappa,s_len_curr, 0])
            s_len_curr = s_len_next
        
        self.track_length = s_len_curr
        
        ##add last point
        waypoints.append([path_array[-1][0], path_array[-1][1], yaw, kappa, s_len_curr, 0])        
        self.waypoints =  np.array( waypoints)   
        print("before interpolation")
        self.interploate()

    def interploate(self):              
        self.traj_interpld = CubicSpline(self.waypoints[:, -2], self.waypoints[:, 0:4])        
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



    