
import numpy as np

"""This file constains code for trajectory optimization to travel the trajectory in minimum time.
It calculated max velocity at each point calculated from max allowed acceleration and performs optimization over it.
Further, we applied cross-over logic to find braking distance"""

class Trajectory_Optimization:
    def __init__(self, V_max, V_min, Acc_max, Acc_min, Lat_acc_max):
        """
        V_max: maximum achievable velocity for the vehicle / max velocity allowed for the road
        V_min: minimum velocity to drive vehicle
        Acc_max: Max logitudinal acceleration
        Acc_min: Min logitudinal acceleration (decceleration)
        Lat_acc_max: Maximum lateral acceleration allowed
        """

        self.V_max = V_max
        self.V_min = V_min
        self.Acc_max = Acc_max
        self.Acc_min = Acc_min
        self.Lat_acc_max = Lat_acc_max

    def optimize(self, path):
        """
        path: list of tuples (x,y)
        returns:
        braking distance : array of braking distances for all the corners
        velocities: an array of velocities at all the points on the path        
        """
        self.path = self.calculate_traj_params(path)

    def calculate_traj_params(self, path):
        """
        This function calculates theta(heading angle), delta_s (delta distance between 2 points), kappa (curvature).
        returns
        arrays of theta, delta_s and kappa
        """
        path = np.asarray(path, dtype=float)
        print(path)
        diff = np.diff(path, axis = 0)
        dx, dy = diff[:,0], diff[:,1]
        theta = np.arctan2(dy, dx)        
        s_delta = np.linalg.norm(diff, axis= 1)        
        s_cumm = np.cumsum(s_delta)       
        
        kappa = np.diff(theta,axis = 0)
        kappa = kappa/s_delta[:-1]
        s_cumm = np.insert(s_cumm,0,0)
        theta = np.append(theta, 0)
        kappa = np.append(kappa, 0)
        kappa = np.append(kappa, 0)
        # print(s_cumm)
        # print(theta)        
        # print(kappa)

        return  s_cumm, theta, kappa       


if __name__ == "__main__":
    path = [(1,2), (3,4), (8,8)]
    traj_obj = Trajectory_Optimization(0,10, 0, 2.5,0.05)
    traj_obj.calculate_traj_params(path)

