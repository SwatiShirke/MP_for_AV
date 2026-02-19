import numpy as np
from scipy.interpolate import CubicSpline
import scipy.spatial as sp
from matplotlib import pyplot as plt


class Trajectory():
    def __init__(self, v_min, v_max, a_min, a_max, lat_acc_a_max, N=10, Tf=5.0, resoultion=0.25):       
        self.track_length = None 
        self.eps = 1e-12
        self.v_min = v_min
        self.v_max = v_max
        self.a_min = a_min 
        self.a_max = a_max
        self.lat_acc_a_max = lat_acc_a_max 
        self.N = N            #MPC horizon
        self.Tf = Tf          #MPC time horizon time frame
        self.resoultion = resoultion #resoultion for the interpolated trajectory, used for plotting and generating waypoints for the MPC planner.

    def create_path_funs(self, path):
        ##waypoints = [x, y, theta, s_length]
        """
        input:
        path : 2d array with n * 2 dimension

        returns:
        waypoints : 2d array with n * 4 dimension, where each row is [x, y, theta, s_length]
        """   
      

        if path is not None:
            if not isinstance(path, np.ndarray):
                raise TypeError("path should be a numpy array")
                return None 
            else:
                path_array = path
        else:
            raise ValueError("path should not be None")
            return None
        
        #compute track length for each waypoint
        d = np.diff(path_array, axis=0)
        dist = np.linalg.norm(d, axis=1)
        s_len = np.cumsum(dist)
        s_len = np.insert(s_len, 0, 0)

        #compute heading angle 
        yaw = np.arctan2(d[:,1], d[:,0])
        yaw = np.r_[yaw, yaw[-1]] 

        wps = np.hstack((path_array, yaw.reshape(-1,1), s_len.reshape(-1,1)))        
        self.track_length = s_len[-1]  

        self._interploate(wps)
        self.generate_WP_KD_tree(self.resoultion)

    def get_interpolated_path(self, resoultion = 0.25):
        """
        This function genrated interpolated path for the max_track length of the trajectory and returns it. 
        This is useful to plot generated trajectory or generate waypoints for the current trajectory. 

        input:
        resoultion : distance between two consecutive waypoints in the interpolated trajectory.
        Returns:
        points : 2d array with n * 4 dimension, where each row is [x, y, theta, s_length]
        """
        s_min, s_max = 0, self.track_length
        n = int(np.floor(self.track_length / resoultion)) + 1
        s_points = np.linspace(0.0, self.track_length, n)

        points = self.traj_interpld(s_points)        
        return points

    def get_traj_wps(self, current_location, ref_velocity):
        """
        This function calculates next (N) waypoints using interpolated trajectory. 
        The genrated trajectory is used as a referenc trajectory for the MPC planner. 

        current_location : (x,y,yaw) current location of the ego vehicle, used to find the closest point on the trajectory. 
        """
        x_current, y_current, yaw_current = current_location[0:3]
        _, index = self.path_kd_tree.query([x_current, y_current], k=1)
        s_init = self.waypoints[index, 3] #x,y,yaw of the closest point on the trajectory
        ds= (self.Tf / self.N) * ref_velocity
        traj_wps = []
       
        for i in range(self.N):
            s_current = s_init +  i * ds 
            point = self.traj_interpld(s_current)          

            if not np.all(np.isfinite(point)):
             break
            
            traj_wps.append(point)
    
        return np.array(traj_wps)

    def get_traj_wps_ego(self, current_location, ref_velocity):
        """
        This function calculates next (N) waypoints using interpolated trajectory. 
        The genrated trajectory is used as a referenc trajectory for the MPC planner. 

        current_location : (x,y,yaw) current location of the ego vehicle, used to find the closest point on the trajectory. 
        """
        x0, y0, yaw,_ , _ , _, _ = current_location   # yaw MUST be radians

        traj_world = self.get_traj_wps(current_location, ref_velocity)  # (N,4)
        if traj_world.size == 0:
            return None

        dx = traj_world[:, 0] - x0
        dy = traj_world[:, 1] - y0

        c = np.cos(yaw)
        s = np.sin(yaw)

        # world -> ego (rotate by -yaw)
        x_e =  c * dx + s * dy
        y_e = -s * dx + c * dy

        return np.stack([x_e, y_e], axis=1)  # (N,2)
 
    def generate_WP_KD_tree(self, resoultion=0.25):
        """
        This function generates waypoints from the interpolated trajectory obejct with required resoultion.
        User can choose, how many waypoints to be generated for the given trajectory.
        This functiona also creates KD tree used for finding closest point on the trajectory for the given location.
        """
        self.waypoints = self.get_interpolated_path(resoultion)
        self.path_kd_tree = sp.KDTree(self.waypoints[:, 0:2])

    def _interploate(self, wps):
        """
        This function creates a cubic spline interpolation of the given waypoints.
        The waypoints should be in the format [x, y, theta, s_length].
        """               
        self.traj_interpld = CubicSpline(wps[:, 3], wps, extrapolate=False)
                 
    def plot_path(self):
        s_range = np.linspace(0, self.track_length, 100)
        points = self.traj_interpld(s_range)
        plt.plot(points[:,0], points[:,1])
        plt.show()

def test_create_path(traj: Trajectory, path: np.ndarray):
    print("\n[TEST] create_path_funs()")
    traj.create_path_funs(path)

    assert traj.track_length is not None and traj.track_length > 0.0
    assert hasattr(traj, "traj_interpld")
    assert hasattr(traj, "waypoints")
    assert traj.waypoints.shape[1] == 4, f"Expected waypoints (n,4), got {traj.waypoints.shape}"
    assert hasattr(traj, "path_kd_tree")

    print(f"  track_length = {traj.track_length:.3f}")
    print(f"  waypoints shape = {traj.waypoints.shape}")
    print("  OK")


def test_interpolated_path(traj: Trajectory):
    print("\n[TEST] get_interpolated_path()")
    pts = traj.get_interpolated_path(traj.resoultion)

    assert pts.ndim == 2 and pts.shape[1] == 4, f"Expected (n,4), got {pts.shape}"
    assert np.all(np.isfinite(pts)), "Interpolated path contains NaNs/Infs"

    # s should be non-decreasing and end near track_length
    s = pts[:, 3]
    assert np.all(np.diff(s) >= -1e-6), "Interpolated s is not non-decreasing"
    assert abs(float(s[-1]) - float(traj.track_length)) < 1e-2 + traj.resoultion, \
        f"Last s={s[-1]} not near track_length={traj.track_length}"

    print(f"  interpolated points shape = {pts.shape}")
    print(f"  s range = [{s[0]:.3f}, {s[-1]:.3f}]")
    print("  OK")


def test_kdtree_nearest(traj: Trajectory):
    print("\n[TEST] KDTree nearest query")
    # pick a point from the path and perturb it
    p = traj.waypoints[len(traj.waypoints)//3, 0:2]
    q = p + np.array([0.1, -0.1])

    dist, idx = traj.path_kd_tree.query(q, k=1)
    assert 0 <= idx < traj.waypoints.shape[0]
    s_nn = traj.waypoints[idx, 3]

    print(f"  query = {q}, nearest idx={idx}, dist={dist:.3f}, s_nn={s_nn:.3f}")
    print("  OK")


def test_get_traj_wps(traj: Trajectory):
    print("\n[TEST] get_traj_wps() basic")
    # Choose a current location near the beginning
    x0, y0 = traj.waypoints[0, 0], traj.waypoints[0, 1]
    yaw0 = 0.0  # radians (your function assumes radians)
    ref_v = 5.0

    wps = traj.get_traj_wps((x0, y0, yaw0), ref_v)
    assert wps.ndim == 2 and wps.shape[1] == 4, f"Expected (N,4-ish), got {wps.shape}"
    assert wps.shape[0] > 0, "No waypoints produced"

    # s should be non-decreasing in returned waypoints
    s = wps[:, 3]
    assert np.all(np.diff(s) >= -1e-6), "Returned waypoint s is not non-decreasing"

    print(f"  traj_wps shape = {wps.shape}")
    print(f"  s start={s[0]:.3f}, s end={s[-1]:.3f}")
    print("  OK")


def test_get_traj_wps_near_end(traj: Trajectory):
    print("\n[TEST] get_traj_wps() near end-of-track")
    # Set current location near the end
    x0, y0 = traj.waypoints[-1, 0], traj.waypoints[-1, 1]
    yaw0 = 0.0
    ref_v = 8.0

    wps = traj.get_traj_wps((x0, y0, yaw0), ref_v)

    # It may return fewer than N due to extrapolate=False + break. That's acceptable.
    assert wps.ndim == 2 and wps.shape[1] == 4, f"Expected (*,4), got {wps.shape}"

    print(f"  produced {wps.shape[0]} / {traj.N} waypoints (expected may be < N near end)")
    if wps.shape[0] > 0:
        print(f"  last s = {wps[-1,3]:.3f} (track_length={traj.track_length:.3f})")
    print("  OK")


def test_get_traj_wps_ego(traj: Trajectory):
    print("\n[TEST] get_traj_wps_ego() sanity")
    # pick a mid-track pose
    mid = traj.waypoints[len(traj.waypoints)//2]
    x0, y0 = float(mid[0]), float(mid[1])

    # Use ego yaw aligned with path yaw at that point (already radians)
    yaw0 = float(mid[2])
    ref_v = 5.0

    wps_ego = traj.get_traj_wps_ego((x0, y0, yaw0), ref_v)
    assert wps_ego is not None, "wps_ego returned None"
    assert wps_ego.ndim == 2 and wps_ego.shape[1] == 2, f"Expected (N,2), got {wps_ego.shape}"
    assert np.all(np.isfinite(wps_ego)), "Ego waypoints contain NaNs/Infs"

    # In ego frame, points should be mostly in front (x >= ~0) if yaw aligns with path
    frac_in_front = float(np.mean(wps_ego[:, 0] >= -1e-3))
    print(f"  wps_ego shape = {wps_ego.shape}, frac_in_front={frac_in_front:.2f}")
    print(f"  first ego wp = {wps_ego[0]}")
    print("  OK")



if __name__ == "__main__":
    # A slightly more interesting path than a straight line helps test yaw
    path = np.array([
        [0.0, 0.0],
        [5.0, 0.0],
        [10.0, 2.0],
        [15.0, 6.0],
        [20.0, 12.0],
        [25.0, 20.0],
    ], dtype=np.float32)

    traj = Trajectory(0.0, 10.0, -5.0, 5.0, 2.0, N=10, Tf=5.0, resoultion=0.25)

    test_create_path(traj, path)
    test_interpolated_path(traj)
    test_kdtree_nearest(traj)
    test_get_traj_wps(traj)
    test_get_traj_wps_near_end(traj)
    test_get_traj_wps_ego(traj)

    # optional: visual
    traj.plot_path()
