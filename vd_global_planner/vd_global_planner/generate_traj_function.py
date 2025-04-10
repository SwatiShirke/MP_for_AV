import numpy as np
from scipy.interpolate import CubicSpline
from scipy import sparse
#import osqp 


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
        self.path = path
        self.waypoints = []
        last_del_y = 0
        s_len_curr = 0
        for i in range(len(path) -1):           
            curr_pt = np.array(path[i])
            next_pt = np.array(path[i+1])
            diff_pt = next_pt -curr_pt
            yaw = ( np.arctan2(diff_pt[1], diff_pt[0]) + 2*np.pi) % 4*np.pi   - 2*np.pi     
            dist = np.linalg.norm(diff_pt,2)

            s_len_next = dist + s_len_curr
            if i== 0:
                kappa = 0
            else:                        
                kappa = (yaw - last_yaw) / np.linalg.norm(last_diff,2)

            last_yaw = yaw
            last_diff = diff_pt
            
            x, y = path[i]
            self.waypoints.append([x,y,yaw, kappa,s_len_curr])
            s_len_curr = s_len_next
        
        self.track_length = s_len_curr
        ##add last point
        self.waypoints.append[[path[-1][0], path[-1][1], yaw, kappa, s_len_curr]]
        self.interploate()

    def interploate(self):
        waypoints = np.array(self.waypoints)
        self.traj_interpld = CubicSpline(waypoints[:, -1], waypoints[:, 0], waypoints[:, 1], waypoints[:, 2], waypoints[:,3])
        
        #testing
        s_range = np.linspace(0, len(waypoints[-1, -1]))
        x,y,yaw, kappa = self.traj_interpld(s_range)


    # def compute_speed_profile(self):
    #     #optimization horizon
    #     N = len(self.waypoints)

    #     #constraints
    #     a_min = np.ones(N-1) * self.a_min
    #     a_max = np.ones(N-1) * self.a_max
    #     v_min = np.ones(N) * self.v_min
    #     v_max = np.ones(N) * self.v_max
    #     ay_max = self.lat_acc_a_max
        

    #     # Inequality Matrix
    #     D1 = np.zeros((N-1, N))

    #     # Iterate over horizon
    #     for i in range(N):

    #         # Get information about current waypoint
    #         current_waypoint = self.get_waypoint(i)
    #         next_waypoint = self.get_waypoint(i+1)
    #         # distance between waypoints
    #         li = next_waypoint - current_waypoint
    #         # curvature of waypoint
    #         ki = current_waypoint.kappa

    #         # Fill operator matrix
    #         # dynamics of acceleration
    #         if i < N-1:
    #             D1[i, i:i+2] = np.array([-1/(2*li), 1/(2*li)])

    #         # Compute dynamic constraint on velocity
    #         v_max_dyn = np.sqrt(ay_max / (np.abs(ki) + self.eps))
    #         if v_max_dyn < v_max[i]:
    #             v_max[i] = v_max_dyn

    #         # Construct inequality matrix
    #         D1 = sparse.csc_matrix(D1)
    #         D2 = sparse.eye(N)
    #         D = sparse.vstack([D1, D2], format='csc')

    #         # Get upper and lower bound vectors for inequality constraints
    #         l = np.hstack([a_min, v_min])
    #         u = np.hstack([a_max, v_max])

    #         # Set cost matrices
    #         P = sparse.eye(N, format='csc')
    #         q = -1 * v_max

    #         # Solve optimization problem
    #         problem = osqp.OSQP()
    #         problem.setup(P=P, q=q, A=D, l=l, u=u, verbose=False)
    #         speed_profile = problem.solve().x

    #         for i, wp in enumerate(self.waypoints):
    #             self.waypoints[i].append(speed_profile[i]) 
    #         speed_profile = problem.solve().x
    #         self.waypoints[-1].append(speed_profile[-1])











