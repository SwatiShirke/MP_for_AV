import numpy as np
import torch 

class Utilities:
    def __init__(self, max_L, max_W, lidar_max_range, v_max, tf):
        self.max_L, self.max_W = max_L, max_W
        self.lidar_max_range = lidar_max_range        
        self.v_max = v_max        
        self.eps = 1e-6 
        self.tf = tf
        self.pos_scale = float(max(self.lidar_max_range, self.tf * self.v_max, self.eps)) 

    def preprocess_state(self, state: np.ndarray) -> np.ndarray:
        """
        Normalize state using unified spatial scale.

        Input:  (21,8) 
          [x, y, yaw, L, W, vx, vy, flag] - first 11 rows
          [x,y, 0, 0, 0, 0, 0, 0] - next 10 rows (padded traj waypoints in ego frame)

        Output: (21 , 9)
          [x_n, y_n, sin(yaw), cos(yaw),
           L_n, W_n, vx_n, vy_n, flag]
        """

        if state is None:
            return None
        
        s = np.asarray(state, dtype=np.float32)
     
        
        if s.ndim != 2 or s.shape[1] != 8 or s.shape[0] != 21:
            raise ValueError(f"Expected (21,8), got {s.shape}")

        # ----------- scales -----------
        eps = self.eps

        
        

        vmax = float(max(self.v_max, eps))
        maxL = float(max(self.max_L, eps))
        maxW = float(max(self.max_W, eps))

        # ----------- extract columns -----------
        x = s[:, 0].copy()
        y = s[:, 1].copy()
        yaw = s[:, 2].copy()
        L = s[:, 3].copy()
        W = s[:, 4].copy()
        vx = s[:, 5].copy()
        vy = s[:, 6].copy()
        flag = s[:, 7].copy()

        # ----------- angle safety (wrap) -----------
        yaw = (yaw + np.pi) % (2.0 * np.pi) - np.pi

        # ----------- clipping BEFORE normalization -----------
        x = np.clip(x, -self.pos_scale, self.pos_scale)
        y = np.clip(y, -self.pos_scale, self.pos_scale)

        L = np.clip(L, 0.0, maxL)
        W = np.clip(W, 0.0, maxW)

        vx = np.clip(vx, -vmax, vmax)
        vy = np.clip(vy, -vmax, vmax)

        flag = np.clip(flag, 0.0, 1.0)

        # ----------- normalization -----------
        x_n = x / self.pos_scale
        y_n = y / self.pos_scale

        L_n = L / maxL
        W_n = W / maxW

        vx_n = vx / vmax
        vy_n = vy / vmax

        # ----------- yaw -> sin/cos -----------
        sin_y = np.sin(yaw).astype(np.float32)
        cos_y = np.cos(yaw).astype(np.float32)

        # ----------- pack output (N,9) -----------
        out = np.zeros((s.shape[0], 9), dtype=np.float32)

        out[:, 0] = np.clip(x_n, -1.0, 1.0)
        out[:, 1] = np.clip(y_n, -1.0, 1.0)
        out[:, 2] = sin_y
        out[:, 3] = cos_y
        out[:, 4] = np.clip(L_n, 0.0, 1.0)
        out[:, 5] = np.clip(W_n, 0.0, 1.0)
        out[:, 6] = np.clip(vx_n, -1.0, 1.0)
        out[:, 7] = np.clip(vy_n, -1.0, 1.0)
        out[:, 8] = flag

        out = torch.tensor(out, dtype=torch.float32)

        return out
   
    def postprocess(self, trajwaypoints_ego, ego_state):
        """
            cumulate delta values to create continuous traj in ego frame and 
            then convert into world frame 
            trajwaypoints_ego: (10,3) -> (dx, dy, d_yaw)
            ego_state = [x, y, yaw, vx, vy, L, W]

            output: trajwaypoints_world: (10,3) -> (x, y, yaw) in world frame
        """

        trajwaypoints_ego = np.asarray(trajwaypoints_ego, dtype=np.float32)
        if trajwaypoints_ego is None:
            return None
        
        traj = trajwaypoints_ego.copy().reshape(-1, 3)  # (10,3)
        traj[:, 0] = np.clip(traj[:, 0], -self.pos_scale, self.pos_scale)
        traj[:, 1] = np.clip(traj[:, 1], -self.pos_scale, self.pos_scale)
        traj[:, 2] = np.clip(traj[:, 2], -np.pi, np.pi)

        # cumulative local displacement
        x_cum = np.cumsum(traj[:, 0])
        y_cum = np.cumsum(traj[:, 1])
        yaw_cum = np.cumsum(traj[:, 2])

        x_ego, y_ego, yaw_ego = ego_state[0], ego_state[1], ego_state[2]
        yaw_ego = (yaw_ego + np.pi) % (2*np.pi) - np.pi

        cos_yaw = np.cos(yaw_ego)
        sin_yaw = np.sin(yaw_ego)

        x_world = x_ego + x_cum * cos_yaw - y_cum * sin_yaw
        y_world = y_ego + x_cum * sin_yaw + y_cum * cos_yaw
        yaw_world = yaw_ego + yaw_cum
        yaw_world = (yaw_world + np.pi) % (2*np.pi) - np.pi

        trajwaypoints_world = np.stack([x_world, y_world, yaw_world], axis=1)
  

        return trajwaypoints_world

    def postprocess_2(self, action, ego_state, ref_traj_ego):
        """
        add delta point to reference ego trajectory and then convert to world frame"""
        if action is None or ego_state is None or ref_traj_ego is None:
            return None
        traj_delta_ego = action.reshape(-1, 3)
        if ref_traj_ego.shape != (10,3):
            raise ValueError(f"Expected ref_traj_ego shape (10,3), got {ref_traj_ego.shape}")        
        if traj_delta_ego.shape != (10,3):
            raise ValueError(f"Expected traj_delta_ego shape (10,3), got {traj_delta_ego.shape}")
        
        trajwaypoints_ego = ref_traj_ego + traj_delta_ego

        x = trajwaypoints_ego[:, 0]
        y = trajwaypoints_ego[:, 1]
        yaw = trajwaypoints_ego[:, 2]

        x_ego, y_ego, yaw_ego = ego_state[0], ego_state[1], ego_state[2]

        cos_yaw = np.cos(yaw_ego)
        sin_yaw = np.sin(yaw_ego)

        x_world = x_ego + x * cos_yaw - y * sin_yaw
        y_world = y_ego + x * sin_yaw + y * cos_yaw
        yaw_world = yaw_ego + yaw
        yaw_world = (yaw_world + np.pi) % (2*np.pi) - np.pi 
        trajwaypoints_world = np.stack([x_world, y_world, yaw_world], axis=1)
        return trajwaypoints_world
   
        
def test_utilities():
    print("Running Utilities tests...\n")

    utils = Utilities(
        max_L=12,
        max_W=5,
        lidar_max_range=50,
        v_max=10,
        tf=5
    )

    # -------------------------------
    # 1️⃣ Test preprocess_state
    # -------------------------------

    # Create synthetic raw state (21,8)
    state = np.zeros((21, 8), dtype=np.float32)

    # Ego row
    state[0] = [10, -5, np.pi/2, 4, 2, 3, -2, 1]

    # 10 obstacle rows
    for i in range(1, 11):
        state[i] = [i, i*0.5, 0.1*i, 4, 2, 1, 1, 1]

    # 10 traj rows (absolute ego frame)
    for i in range(11, 21):
        state[i] = [i-10, (i-10)*0.2, 0, 0, 0, 0, 0, 0]

    processed = utils.preprocess_state(state)

    assert processed.shape == (21, 9)
    assert not np.isnan(processed).any()
    assert np.max(np.abs(processed[:, :2])) <= 1.0
    assert np.max(np.abs(processed[:, 6:8])) <= 1.0

    print("preprocess_state ✅ passed")

    # -------------------------------
    # 2️⃣ Test postprocess
    # -------------------------------

    # Fake network output: small forward motion
    traj_deltas = np.zeros((10, 3), dtype=np.float32)
    traj_deltas[:, 0] = 1.0   # dx = 1m per step
    traj_deltas[:, 1] = 0.0
    traj_deltas[:, 2] = 0.05  # small yaw increment

    ego_state = [0.0, 0.0, 0.0, 0, 0, 4, 2]

    traj_world = utils.postprocess(traj_deltas, ego_state)

    assert traj_world.shape == (10, 3)
    assert not np.isnan(traj_world).any()

    # Check monotonic forward motion
    assert np.all(np.diff(traj_world[:, 0]) >= 0)

    print("postprocess ✅ passed")

    print("\nAll tests passed 🚀")

def test_utilities_values():
    print("Running deterministic value tests...\n")

    utils = Utilities(
        max_L=10,
        max_W=4,
        lidar_max_range=50,
        v_max=10,
        tf=5
    )

    # pos_scale = max(50, 5*10) = 50
    # vmax = 10

    # -------------------------------
    # 1️⃣ Test preprocess_state
    # -------------------------------

    state = np.zeros((21, 8), dtype=np.float32)

    # Set one row to known values
    state[0] = [25.0, -50.0, np.pi/2, 5.0, 2.0, 5.0, -10.0, 1.0]

    processed = utils.preprocess_state(state)

    # Manual expected values:
    # x_n = 25 / 50 = 0.5
    # y_n = -50 / 50 = -1.0 (clipped)
    # sin(pi/2) = 1
    # cos(pi/2) = 0
    # L_n = 5 / 10 = 0.5
    # W_n = 2 / 4 = 0.5
    # vx_n = 5 / 10 = 0.5
    # vy_n = -10 / 10 = -1.0
    # flag = 1

    expected = np.array([
        0.5,
        -1.0,
        1.0,
        0.0,
        0.5,
        0.5,
        0.5,
        -1.0,
        1.0
    ], dtype=np.float32)

    print("Processed row:", processed[0])
    print("Expected row :", expected)

    assert np.allclose(processed[0], expected, atol=1e-5)

    print("preprocess_state values ✅ correct")

    # -------------------------------
    # 2️⃣ Test postprocess
    # -------------------------------

    # Simple case:
    # ego at (0,0), yaw=0
    ego_state = [0.0, 0.0, 0.0, 0, 0, 0, 0]

    # Move straight 1m each step, no yaw change
    traj_deltas = np.zeros((10, 3), dtype=np.float32)
    traj_deltas[:, 0] = 1.0  # dx = 1

    traj_world = utils.postprocess(traj_deltas, ego_state)

    # Expected world:
    # x = [1,2,3,...,10]
    # y = all zeros
    # yaw = all zeros

    expected_x = np.arange(1, 11, dtype=np.float32)
    expected_y = np.zeros(10, dtype=np.float32)
    expected_yaw = np.zeros(10, dtype=np.float32)

    print("Postprocess x:", traj_world[:, 0])
    print("Expected x   :", expected_x)

    assert np.allclose(traj_world[:, 0], expected_x, atol=1e-5)
    assert np.allclose(traj_world[:, 1], expected_y, atol=1e-5)
    assert np.allclose(traj_world[:, 2], expected_yaw, atol=1e-5)

    print("postprocess values ✅ correct")

    print("\nAll deterministic value tests passed 🚀")


if __name__ == "__main__":
    test_utilities()
    test_utilities_values()
