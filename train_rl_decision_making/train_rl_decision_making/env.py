import carla
import random 
import numpy as np
from get_map import Grid_map
from a_star import a_star
from traj import Trajectory
from sensor_fusion import SensorFusion
import math

class Env:
    """
    Class of the environment for training the RL decision making model. The environment should be able to reset and step according to the action taken by the agent.
    This class connects with Carla and provides the necessary functions for the agent to interact with the environment. The environment should also provide the necessary information for the agent to make decisions, such as the current state of the environment and the reward for taking a certain action.
    """
    
    def __init__(self, min_distance_lidar, waypoint_publisher, traffic_manager_port, traffic_size, v_min, v_max, a_min, a_max, lateral_accel, max_obj, N, tf, traj_resolution, goal_radius, lidar_max_range):
        self.ros_publisher = waypoint_publisher
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()
        self.vehicle = None 
        self.traj = None  
        self.interp_traj = None
        self.start_point = None
        self.goal_point = None
        self.traffic_manager_port = traffic_manager_port
        self.traffic_size = traffic_size 
        self.is_test_mode = True 
        self.v_min = v_min
        self.v_max = v_max
        self.a_min = a_min
        self.a_max = a_max
        self.lateral_accel = lateral_accel 
        self.N = N
        self.tf = tf
        self.traj_resolution = traj_resolution
        self.yollow_model_path = "/home/swati/Motion_Planning/MP_for_AV/src/MP_for_AV/train_rl_decision_making/train_rl_decision_making/yolov8n.pt"
        self.max_obs_detections = max_obj #max obstacle detcted through yollow
        self.min_distance_lidar = min_distance_lidar # meters, tune to remove ego reflections from lidar points
        self.collision_penalty = -100.0 # penalty for collision, tune as needed
        self.min_dist_threshold = 4.0 # meters, threshold for near collision penalty, tune as needed
        self.goal_radius = goal_radius
        self.lidar_max_range = lidar_max_range
        self.eps = 1e-6 
        self.clip_norm = 1.0
        #get max limits, used for data normallization
        self.max_L, self.max_W = self.get_max_LW()
    
    def reset(self):
        """        
        clean all vehicles
        spawn traffic vehicles at random spawn points
        get start point
        get goal point - find goal 
        traj - generate traj from start to goal - A* algorithm
        interpld_traj - interpolate traj to get waypoints with fixed distance
        spawn ego vehicle at start point
        calculate state - 
        return state 

        """
        self.cleanup_vehicles() 
        #self.world = self.client.reload_world(False)    
        self.setup_traffic_manager(tm_port=self.traffic_manager_port, synchronous=True)
        npc_ids = self.spawn_npc_traffic(num_vehicles=self.traffic_size, tm_port=self.traffic_manager_port)
        
        self.start_point = self.get_random_free_spawn_point()
        self.ref_velocity = self.get_ref_velocity()
        self.ego_vehicle = self.spawn_ego_vehicle(self.start_point)
        ego_state = self.get_ego_state()
        self.goal_point = self.get_goal_point(self.start_point)
        # if self.is_test_mode:
        #     print(f"Start point: {self.start_point}, Goal point: {self.goal_point}")

        grid_map_generator = Grid_map(self.world, 1.0, 10.0)
        self.grid_map, self.offset, self.grid_resolution = grid_map_generator.get_grid_map()
        self.a_star_planner = a_star(self.grid_map, self.offset, self.grid_resolution, self.goal_radius)
        self.path = self.a_star_planner.find_path((self.start_point.location.x, self.start_point.location.y), (self.goal_point.location.x, self.goal_point.location.y))

        self.traj_obj = Trajectory(self.v_min,self.v_max, self.a_min, self.a_min , self.lateral_accel, self.N, self.tf, self.traj_resolution)
        self.traj_obj.create_path_funs(self.path)
        
        traj_waypoints = self.traj_obj.get_traj_wps(ego_state, self.ref_velocity)
        traj_waypoints_ego = self.traj_obj.get_traj_wps_ego(ego_state, self.ref_velocity)

        self.sensor_fusion = SensorFusion(self.world, self.ego_vehicle, self.min_distance_lidar, self.yollow_model_path,self.max_obs_detections)
        self.step_count = 0
        self.sensor_fusion._refresh_vehicle_cache() # cache the initial state of the world for faster access during state computation
        
        state = self.sensor_fusion.get_current_state(traj_waypoints_ego, ego_state)
        return state

    def cleanup_vehicles(self):
        """
        Destroy all vehicles, sensors, walkers, and controllers
        currently present in the CARLA world.
        Safe to call during reset().
        """

        print("Cleaning up CARLA actors...")

        actors = self.world.get_actors()
    
        # 1️⃣ Stop all sensors FIRST (critical)
        # for actor in actors:
        #     if actor.type_id.startswith("sensor."):
        #         try:
        #             actor.stop()
        #         except:
        #             pass

        # 2️⃣ Destroy sensors first
        # for actor in actors:
        #     if actor.type_id.startswith("sensor."):
        #         try:
        #             actor.destroy()
        #         except:
        #             pass

        # 3️⃣ Stop walker controllers before destroying walkers
        for actor in actors:
            if actor.type_id.startswith("controller.ai.walker"):
                try:
                    actor.stop()
                    actor.destroy()
                except:
                    pass

        # 4️⃣ Destroy walkers
        for actor in actors:
            if actor.type_id.startswith("walker."):
                try:
                    actor.destroy()
                except:
                    pass

        # 5️⃣ Destroy vehicles (traffic + ego)
        for actor in actors:
            if actor.type_id.startswith("vehicle."):
                try:
                    actor.destroy()
                except:
                    pass

        # 6️⃣ Small world tick to flush destruction
        try:
            self.world.tick()
        except:
            pass

        print("Cleanup complete.")
  
    def destroy(self):
        self.sensor_fusion.destroy()
        self.cleanup_vehicles()

    def setup_traffic_manager(self, tm_port=8000, synchronous=True):
        self.tm = self.client.get_trafficmanager(tm_port)
        # Optional global behavior knobs
        self.tm.set_global_distance_to_leading_vehicle(2.5)
        self.tm.set_synchronous_mode(synchronous)

    def spawn_npc_traffic(self, num_vehicles=30, min_dist=8.0, max_spawn_tries=200, tm_port=8000):
        """
        Spawns NPC vehicles and enables autopilot via Traffic Manager.
        Call this BEFORE spawning ego vehicle.
        """
        world = self.world
        carla_map = world.get_map()
        spawn_points = carla_map.get_spawn_points()
        if not spawn_points:
            raise RuntimeError("No spawn points available on this map.")

        blueprints = world.get_blueprint_library().filter("vehicle.*")
        vehicles_existing = world.get_actors().filter("vehicle.*")

        def is_free(transform):
            loc = transform.location
            for v in vehicles_existing:
                if v.get_location().distance(loc) < min_dist:
                    return False
            return True

        spawned_ids = []
        tries = 0

        random.shuffle(spawn_points)  # helps reduce clustering

        while len(spawned_ids) < num_vehicles and tries < max_spawn_tries:
            tries += 1
            sp = random.choice(spawn_points)
            if not is_free(sp):
                continue

            bp = random.choice(blueprints)

            # Optional: avoid weird vehicles
            # if bp.id.endswith("microlino") or "carlamotors" in bp.id: continue

            npc = world.try_spawn_actor(bp, sp)
            if npc is None:
                continue

            # Hand over control to Traffic Manager
            npc.set_autopilot(True, tm_port)

            spawned_ids.append(npc.id)
            vehicles_existing = world.get_actors().filter("vehicle.*")  # refresh

        #if len(spawned_ids) < num_vehicles:
            #print(f"[WARN] Spawned {len(spawned_ids)}/{num_vehicles} NPC vehicles (spawn limits/collisions).")

        return spawned_ids

    def get_random_free_spawn_point(self, min_dist=8.0, max_tries=50):
        """
        Returns a random free spawn point on the road.

        Args:
            min_dist (float): minimum distance (meters) from other vehicles
            max_tries (int): how many random attempts before fallback

        Returns:
            carla.Transform
        """
        carla_map = self.world.get_map()
        spawn_points = carla_map.get_spawn_points()

        if not spawn_points:
            raise RuntimeError("No spawn points found in CARLA map")

        vehicles = self.world.get_actors().filter('vehicle.*')

        def is_free(transform):
                loc = transform.location
                for v in vehicles:
                    if v.get_location().distance(loc) < min_dist:
                        return False
                return True

        # Try random sampling first
        for _ in range(max_tries):
            sp = random.choice(spawn_points)
            if is_free(sp):
                return sp

        # Fallback: return any spawn point (better than crashing)
        print("[WARN] No free spawn point found, using random fallback")
        return random.choice(spawn_points)

    def get_goal_point(self, start_point):
        ref_vel = self.get_ref_velocity()
        tp = np.random.uniform(3.0, 10.0) # time horizon for planning
        distance = ref_vel * tp # look tp seconds ahead
        map = self.world.get_map()
        current_waypoint = map.get_waypoint(start_point.location)
        goal_waypoints = current_waypoint.next(distance)
        return goal_waypoints[0].transform if goal_waypoints else None

    def get_ref_velocity(self):
        """
        returns reference velocity for the trajectory for current episode. This can be a fixed value or can be calculated based on the traffic conditions or other factors. For now, we are returning a fixed value.
        """
        ref_vel = self.v_max # m/s 
        return ref_vel
    
    def spawn_ego_vehicle(self, ego_transform):
        """
        Spawns the ego Mini Cooper at the given CARLA transform.

        Args:
            ego_transform (carla.Transform)

        Returns:
            carla.Vehicle
        """ 
        try:
            blueprint_library = self.world.get_blueprint_library()
            ego_bp = blueprint_library.find("vehicle.mini.cooper")
            ego_bp.set_attribute("role_name", "hero")
            ego_bp.set_attribute("ros_name", "ego_vehicle")

            #print("ego_transform: ", ego_transform)
            hero_vehicle = self.world.spawn_actor(ego_bp, ego_transform)
            hero_vehicle.set_autopilot(False)
            # if self.is_test_mode:
            #     print("[INFO] Ego vehicle spawned")
           
            return hero_vehicle

        except RuntimeError as e:
            #print(f"[ERROR] Failed to spawn ego vehicle: {e}")
            self.vehicle = None
            return None 

    def get_ego_location(self):
        tf = self.ego_vehicle.get_transform()
        ego_location = (tf.location.x, tf.location.y, np.deg2rad(tf.rotation.yaw))       
        return ego_location
    
    def get_ego_state(self):
        """
        Returns ego state in WORLD frame:
          (x_world, y_world, yaw_rad, vx_world, vy_world)

        yaw_rad: radians
        vx_world, vy_world: m/s from CARLA get_velocity() (world frame)
        """
        if self.ego_vehicle is None:
            return None

        tf = self.ego_vehicle.get_transform()
        vel = self.ego_vehicle.get_velocity()

        x = float(tf.location.x)
        y = float(tf.location.y)
        yaw_rad = float(np.deg2rad(tf.rotation.yaw))

        vx_w = float(vel.x)
        vy_w = float(vel.y)

        #get width and length of the ego vehicle
        bb = self.ego_vehicle.bounding_box
        extent = bb.extent  # half-dimensions

        length = 2.0 * extent.x
        width  = 2.0 * extent.y

        return (x, y, yaw_rad, vx_w, vy_w, length, width) 

    # -----------------------------
    # Helpers
    # -----------------------------
    def _wrap_to_pi(angle_rad: float) -> float:
        """Wrap angle to [-pi, pi]."""
        while angle_rad > math.pi:
            angle_rad -= 2.0 * math.pi
        while angle_rad < -math.pi:
            angle_rad += 2.0 * math.pi
        return angle_rad

    # -----------------------------
    # Reward functions (drop into your Env class)
    # -----------------------------
    def calculate_reward(
        self,
        *,
        done_reason: str | None = None,
        ego_state=None,
        traj_waypoints=None,   # WORLD-frame waypoints from get_traj_wps()
        state=None,            # full RL state from sensor_fusion.get_current_state()
        action=None,
    ):
        """
        Total reward = terminal + collision + near-collision + trajectory-follow + lane + speed

        Expects:
          ego_state = (x, y, yaw_rad, vx_w, vy_w, ... optional)
          traj_waypoints: array/list where each row begins with [x_world, y_world, ...]
          state: shape (1 + max_objects + N, 8) with obstacle rows in ego frame:
                 [x,y,yaw_rel,L,W,v_rel_x,v_rel_y,flag]
        """

        # Use current ego_state if not provided
        if ego_state is None:
            ego_state = self.get_ego_state()

        r = 0.0

        # Terminal should dominate when done
        r += self.terminal_reward(done_reason)

        # Collision penalty (can still apply even if terminal already did it; usually keep one)
        # If you use terminal_reward(collision=-100), then set collision_penalty=0 or keep only one.
        r += self.collision_reward()

        # Near-collision shaping (only if we have a state)
        if state is not None:
            r += self.near_collision_reward(state)

        # Trajectory following (WORLD frame)
        if traj_waypoints is not None and len(traj_waypoints) >= 2:
            r += self.trajectory_following_reward(ego_state, traj_waypoints)

        # Lane keeping (needs current transform)
        if getattr(self, "ego_vehicle", None) is not None:
            r += self.lane_following_reward(self.ego_vehicle.get_transform())

        # Speed tracking
        r += self.speed_reward(ego_state)

        r += self.progressive_reward(ego_state)

        self.reward = float(r)
        return float(r)

    def collision_reward(self) -> float:
        """One-step collision penalty (shaping)."""
        if getattr(self.sensor_fusion, "collision_happened", False):
            return float(getattr(self, "collision_penalty", -100.0))
        return 0.0

    def terminal_reward(self, done_reason: str | None) -> float:
        """Terminal reward/penalty based on done_reason."""
        if done_reason is None:
            return 0.0
        if done_reason == "collision":
            return float(getattr(self, "terminal_collision_penalty", -100.0))
        if done_reason == "goal_reached":
            return float(getattr(self, "terminal_success_reward", 100.0))
        if done_reason == "timeout":
            return float(getattr(self, "terminal_timeout_penalty", -10.0))
        return 0.0

    def trajectory_following_reward(self, ego_state, traj_waypoints) -> float:
        """
        Penalize distance to next waypoint (WORLD frame).
        traj_waypoints from get_traj_wps() should be in world coordinates.
        """
        x_ego, y_ego = float(ego_state[0]), float(ego_state[1])

        # Use waypoint 1 (next) if available
        next_wp = traj_waypoints[1]
        x_wp, y_wp = float(next_wp[0]), float(next_wp[1])

        err = math.hypot(x_ego - x_wp, y_ego - y_wp)
        w = float(getattr(self, "w_traj", 1.0))
        return -w * err

    def speed_reward(self, ego_state) -> float:
        """Penalize deviation from reference speed (m/s)."""
        vx_w, vy_w = float(ego_state[3]), float(ego_state[4])
        speed = math.hypot(vx_w, vy_w)

        v_ref = float(getattr(self, "ref_velocity", 0.0))
        err = abs(speed - v_ref)

        w = float(getattr(self, "w_speed", 0.2))
        return -w * err

    def lane_following_reward(
        self,
        ego_transform,
        *,
        lane_width_scale: float = 0.5,
        w_cte: float = 1.0,
        w_heading: float = 0.5,
        offroad_penalty: float = -5.0,
        wrong_lane_penalty: float = -2.0,
        expected_lane_id: int | None = None,
        expected_road_id: int | None = None,
    ) -> float:
        """
        Lane reward based on cross-track error to lane center + heading alignment to lane tangent.
        Uses CARLA map waypoint projection.
        """
        if ego_transform is None:
            return 0.0
        if getattr(self, "carla_map", None) is None:
            return 0.0

        ego_loc = ego_transform.location
        ego_yaw_rad = math.radians(ego_transform.rotation.yaw)

        # NOTE: set this somewhere in __init__: self._carla_lane_type_driving = carla.LaneType.Driving
        lane_type = getattr(self, "_carla_lane_type_driving", None)
        wp = self.carla_map.get_waypoint(
            ego_loc,
            project_to_road=True,
            lane_type=lane_type,
        )

        if wp is None:
            return float(offroad_penalty)

        if expected_road_id is not None and wp.road_id != expected_road_id:
            return float(wrong_lane_penalty)
        if expected_lane_id is not None and wp.lane_id != expected_lane_id:
            return float(wrong_lane_penalty)

        # Cross-track error
        dx = ego_loc.x - wp.transform.location.x
        dy = ego_loc.y - wp.transform.location.y
        cte = math.hypot(dx, dy)

        lane_width = max(float(wp.lane_width), 0.1)
        denom = max(lane_width * lane_width_scale, 0.1)
        cte_norm = cte / denom

        # Heading error vs lane tangent
        lane_yaw_rad = math.radians(wp.transform.rotation.yaw)
        heading_err = abs(_wrap_to_pi(ego_yaw_rad - lane_yaw_rad))
        heading_norm = heading_err / math.pi

        return float(-(w_cte * cte_norm + w_heading * heading_norm))

    def near_collision_reward(self, state, threshold: float | None = None) -> float:
        """
        Shaping penalty if closest valid obstacle is within threshold (meters).
        state obstacle rows are ego frame: [x,y,yaw_rel,L,W,v_rel_x,v_rel_y,flag]
        """
        if state is None:
            return 0.0

        max_objects = int(getattr(self, "max_objects", 10))
        thr = float(threshold if threshold is not None else getattr(self, "min_dist_threshold", 5.0))

        obs = state[1:1 + max_objects, :]      # (max_objects, 8)
        if obs.shape[1] < 8:
            return 0.0

        valid = obs[:, 7] > 0.5
        if not np.any(valid):
            return 0.0

        dists = np.linalg.norm(obs[valid, 0:2], axis=1)
        min_dist = float(np.min(dists))

        if min_dist < thr:
            # Smooth penalty: closer => more negative, bounded in [-near_collision_penalty, 0]
            base = float(getattr(self, "near_collision_penalty", -5.0))  # negative number
            scale = 1.0 - (min_dist / thr)                               # in (0,1]
            return base * scale
        return 0.0

    def progressive_reward(self, ego_state):
        """
        Reward based on reduction in distance to goal.
        ego_state: (x, y, yaw, vx, vy, ...)
        """

        x, y = ego_state[0], ego_state[1]
        xg = self.goal_point.location.x
        yg = self.goal_point.location.y

        # current distance
        dist = np.linalg.norm([x - xg, y - yg])

        # initialize previous distance if first step
        if not hasattr(self, "_prev_goal_dist"):
            self._prev_goal_dist = dist
            return 0.0

        # reward = positive if distance decreased
        reward = self._prev_goal_dist - dist

        # update memory
        self._prev_goal_dist = dist

        return reward

    def check_done(self):
        """
        Returns:
            done (bool)
            reason (str|None): one of {"collision","goal_reached","timeout","offroad","stuck"} or None
        Assumes:
            self.sensor_fusion.collision_happened (bool)
            self.get_ego_state() -> (x, y, yaw, vx, vy, ...)
            self.goal_point.location.(x,y) and self.goal_radius (float)
            self.step_count and self.max_episode_steps
        Optional (if you have them):
            self.ego_vehicle (carla.Vehicle)
            self.carla_map (carla.Map)
            self._carla_lane_type_driving = carla.LaneType.Driving
            self.stuck_speed_thresh, self.stuck_steps_limit, self._stuck_counter
            self.offroad_terminate (bool)
        """

        # 1) Collision (highest priority)
        if getattr(self.sensor_fusion, "collision_happened", False):
            return True, "collision"

        # 2) Goal reached
        ego_state = self.get_ego_state()
        x, y = float(ego_state[0]), float(ego_state[1])
        gx = float(self.goal_point.location.x)
        gy = float(self.goal_point.location.y)

        if math.hypot(x - gx, y - gy) <= float(getattr(self, "goal_radius", 3.0)):
            return True, "goal_reached"

        # 3) Timeout
        max_steps = int(getattr(self, "max_episode_steps", 0))
        if max_steps > 0 and int(getattr(self, "step_count", 0)) >= max_steps:
            return True, "timeout"

        # 4) Offroad / not on driving lane (optional)
        if getattr(self, "offroad_terminate", False):
            if getattr(self, "carla_map", None) is not None and getattr(self, "ego_vehicle", None) is not None:
                ego_loc = self.ego_vehicle.get_transform().location
                lane_type = getattr(self, "_carla_lane_type_driving", None)
                wp = self.carla_map.get_waypoint(ego_loc, project_to_road=True, lane_type=lane_type)
                # If CARLA cannot project to a driving waypoint, treat as offroad
                if wp is None:
                    return True, "offroad"

        # 5) Stuck (optional)
        # If speed stays below threshold for N consecutive steps, terminate.
        stuck_speed_thresh = float(getattr(self, "stuck_speed_thresh", 0.3))   # m/s
        stuck_steps_limit = int(getattr(self, "stuck_steps_limit", 80))        # steps
        if stuck_steps_limit > 0:
            vx, vy = float(ego_state[3]), float(ego_state[4])
            speed = math.hypot(vx, vy)

            if not hasattr(self, "_stuck_counter"):
                self._stuck_counter = 0

            if speed < stuck_speed_thresh:
                self._stuck_counter += 1
            else:
                self._stuck_counter = 0

            if self._stuck_counter >= stuck_steps_limit:
                return True, "stuck"

        return False, None

    def step(self, action):
        # Publish waypoints to controller
        self.ros_publisher.publish_waypoints(action, self.ref_velocity)

        self.world.tick()
        self.step_count += 1

        # keep actor cache fresh
        self.sensor_fusion.maybe_refresh_cache(self.step_count, refresh_every=20)

        ego_state = self.get_ego_state()  # (x,y,yaw,vx,vy,...)

        traj_w_world = self.traj_obj.get_traj_wps(ego_state, self.ref_velocity)          # world
        traj_w_ego   = self.traj_obj.get_traj_wps_ego(ego_state, self.ref_velocity)      # ego

        state = self.sensor_fusion.get_current_state(traj_waypoints=traj_w_ego, ego_state=ego_state)

        done, reason = self.check_done()

        reward = self.calculate_reward(
            state=state,
            done_reason=reason,
            ego_state=ego_state,
            traj_waypoints=traj_w_world,
            action=action,
        )

        obs = state
        info = {"done_reason": reason}

        return obs, reward, done, info

    def set_max_values(self):
        self.max_L = 12
        self.max_w = 5   
        self.horizon_dist = self.tf * self.v_max

    def _wrap_to_pi(self, ang: float) -> float:
        """Stable wrap to [-pi, pi]."""
        return (ang + math.pi) % (2.0 * math.pi) - math.pi

    def normalize_state(self, state: np.ndarray) -> np.ndarray:
        """
        Normalize state using unified spatial scale.

        Input:  (N, 8)
          [x, y, yaw, L, W, vx, vy, flag]

        Output: (N, 9)
          [x_n, y_n, sin(yaw), cos(yaw),
           L_n, W_n, vx_n, vy_n, flag]
        """

        if state is None:
            return None

        s = np.asarray(state, dtype=np.float32)
        if s.ndim != 2 or s.shape[1] != 8:
            raise ValueError(f"Expected (N,8), got {s.shape}")

        # ----------- scales -----------
        eps = 1e-6

        pos_scale = float(max(self.lidar_max_range, self.horizon_dist))
        pos_scale = max(pos_scale, eps)

        vmax = float(max(self.v_max, eps))
        maxL = float(max(self.max_L, eps))
        maxW = float(max(self.max_w, eps))

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
        x = np.clip(x, -pos_scale, pos_scale)
        y = np.clip(y, -pos_scale, pos_scale)

        L = np.clip(L, 0.0, maxL)
        W = np.clip(W, 0.0, maxW)

        vx = np.clip(vx, -vmax, vmax)
        vy = np.clip(vy, -vmax, vmax)

        flag = np.clip(flag, 0.0, 1.0)

        # ----------- normalization -----------
        x_n = x / pos_scale
        y_n = y / pos_scale

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

        return out

    def get_max_LW(self):
        max_L = 12
        max_W = 5
        return max_L, max_W

if __name__ == "__main__":
   env = Env(traffic_manager_port=8000, traffic_size=40, v_min=0.0, v_max=10.0, a_min=-3.0, a_max=3.0, lateral_accel=2.0)
   env.reset()


