from email.mime import image
import carla
import random 
import numpy as np
from ultralytics import settings
from get_map import Grid_map
from a_star import a_star
from traj import Trajectory
from sensor_fusion import SensorFusion
import math
import cv2
import queue
import os 
from ultralytics import YOLO


class Env:
    """
    Class of the environment for training the RL decision making model. The environment should be able to reset and step according to the action taken by the agent.
    This class connects with Carla and provides the necessary functions for the agent to interact with the environment. The environment should also provide the necessary information for the agent to make decisions, such as the current state of the environment and the reward for taking a certain action.
    """
    
    def __init__(self, grid_resolution, min_distance_lidar, OdomPublisher,
                  waypoint_publisher, traffic_manager_port, traffic_size,
                    v_min, v_max, a_min, a_max, lateral_accel, max_obj, 
                    N, tf, traj_resolution, goal_radius, lidar_max_range,
                      delta_x_th, delta_y_th, delta_yaw_th, is_test_mode, max_episode_steps):
        self.grid_resolution = grid_resolution
        self.wp_publisher = waypoint_publisher
        self.odom_publisher = OdomPublisher
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()
        self.map = self.world.get_map()
        settings = self.world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05   # 20 FPS
        self.world.apply_settings(settings)
        self.vehicle = None 
        self.traj = None  
        self.interp_traj = None
        self.start_point = None
        self.goal_point = None
        self.traffic_manager_port = traffic_manager_port
        self.traffic_size = traffic_size 
        print("Connected to CARLA, world loaded, synchronous mode set")
        self.setup_traffic_manager(tm_port=self.traffic_manager_port, synchronous=True)        
        self.is_test_mode = is_test_mode 
        self.v_min = v_min
        self.v_max = v_max
        self.a_min = a_min
        self.a_max = a_max
        self.lateral_accel = lateral_accel 
        self.N = N
        self.tf = tf
        self.traj_resolution = traj_resolution
        self.yolo_model_path = "yolov8n.pt"
        self.yolo_model = YOLO(self.yolo_model_path)        
        self.max_obs_detections = max_obj #max obstacle detcted through yollow
        self.min_distance_lidar = min_distance_lidar # meters, tune to remove ego reflections from lidar points
        self.collision_penalty = -1000.0 # penalty for collision, tune as needed
        self.min_dist_threshold = 4.0 # meters, threshold for near collision penalty, tune as needed
        self.goal_radius = goal_radius
        self.lidar_max_range = lidar_max_range
        self.eps = 1e-6 
        self.clip_norm = 1.0
        #get max limits, used for data normallization
        self.max_L, self.max_W = self.get_max_LW()
        self.delta_x_th = delta_x_th
        self.delta_y_th = delta_y_th
        self.delta_yaw_th = delta_yaw_th
        self.err_sigma = 0.1 
        self.grid_map_generator = Grid_map(self.world, 1.0, 10.0)
        self.grid_map, self.offset, self.grid_resolution = self.grid_map_generator.get_grid_map()
        self.a_star_planner = a_star(self.grid_map, self.offset, self.grid_resolution, self.goal_radius) 
        self.traj_obj = Trajectory(self.v_min,self.v_max, self.a_min, self.a_min , self.lateral_accel, self.N, self.tf, self.traj_resolution)
        self.max_episode_steps = max_episode_steps
        print("Environment initialized")

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
        npc_ids = self.spawn_npc_traffic(num_vehicles=self.traffic_size, tm_port=self.traffic_manager_port)
        
        self.start_point = self.get_random_free_spawn_point()
        self.ref_velocity = self.get_ref_velocity()
        self.ego_vehicle = self.spawn_ego_vehicle(self.start_point)
        # near_vehicle =  np.random.choice([0,1])
        # self.spawn_vehicles_around_ego(num=near_vehicle, tm_port=self.traffic_manager_port)  # spawn a few vehicles around ego for interaction (optional)

        if self.ego_vehicle is None:
            print("[ERROR] Ego vehicle spawn failed during reset.")
            return None
        ego_state = self.get_ego_state()
        self.goal_point = self.get_goal_point(self.start_point)
       

        start = (self.start_point.location.x, self.start_point.location.y, np.deg2rad(self.start_point.rotation.yaw))
        goal = (self.goal_point.location.x, self.goal_point.location.y, np.deg2rad(self.goal_point.rotation.yaw))
        self.path = self.a_star_planner.find_path(start, goal)  
        self.centered_path = self.get_centered_path(self.path)
        is_traj = self.traj_obj.create_path_funs(self.centered_path) 
        if not is_traj:
            print("[ERROR] Trajectory generation failed during reset.")
            return None
        
        self.traj_waypoints_world = self.traj_obj.get_traj_wps(ego_state, self.ref_velocity)
        if self.traj_waypoints_world is None:
            print("[ERROR] Trajectory generation returned None during reset.")
            return None
        
        if (abs(self.traj_waypoints_world[0,2] - ego_state[2])) > math.pi/2:
            print("Trajecotry generated in opposite direction of ego yaw, flipping trajectory")
            return None        
        
        self.traj_waypoints_ego = self.traj_obj.get_traj_wps_ego(ego_state, self.ref_velocity)
                
        # print("traj generation in reset is done")
        if self.is_test_mode:
        #     print("Initial ego state and trajectory waypoints:")
        #     print("ego_state: ", ego_state)
        #     print("")
        #     print("traj_waypoints: ", self.traj_waypoints_world.shape)
        #     print("traj_waypoints: ", self.traj_waypoints_world)

        #     print("")
        #     print("traj_waypoints_ego: ", self.traj_waypoints_ego.shape)
        #     print("traj_waypoints_ego: ", self.traj_waypoints_ego) 

        #     self.spawn_test_vehicles_in_front(dist1=10.0, dist2=15.0, lateral_offset=0.5)

            self.grid_map_generator.plot_grid_map_world(start=(self.start_point.location.x, self.start_point.location.y), 
                                                          goal=(self.goal_point.location.x, self.goal_point.location.y), path=self.centered_path, show_path_points=True)
            
            self.save_topdown_snapshot_world_traj(ego_state, self.traj_waypoints_world)
          

        for _ in range(10):
            self.world.tick()
        # or, better: tick until you have at least 1 camera + 1 lidar frame in your queues)
        self.step_count = 0
        self.sensor_fusion = SensorFusion(self.world, self.min_distance_lidar, self.yolo_model,self.max_obs_detections, self.ego_vehicle)
        print("type", type(self.sensor_fusion), "sensor fusion: ", self.sensor_fusion)
        #self.sensor_fusion.setup()  
        self.sensor_fusion._refresh_vehicle_cache() # cache the initial state of the world for faster access during state computation
        state = self.sensor_fusion.get_current_state(self.traj_waypoints_ego, ego_state)
        print("reset completed")
        return state

    def cleanup_vehicles(self):
        if hasattr(self, "sensor_fusion") and self.sensor_fusion is not None:
            self.sensor_fusion.destroy()  # Clean up sensor fusion resources (threads, models)
            self.sensor_fusion = None            
        print("Cleaning up CARLA actors...")

        actors = self.world.get_actors()
    
        # 1️⃣ Stop all sensors FIRST (critical)
        for actor in actors:
            if actor.type_id.startswith("sensor."):
                try:
                    actor.stop()
                except:
                    pass

        # 2️⃣ Destroy sensors first
        for actor in actors:
            if actor.type_id.startswith("sensor."):
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
        #self.sensor_fusion.destroy()  # Clean up sensor fusion resources (threads, models)      
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
                print(f"Found free spawn point after {_+1} tries: {sp.location}")
                return sp

        # Fallback: return any spawn point (better than crashing)
        print("[WARN] No free spawn point found, using random fallback")
    
        return random.choice(spawn_points)

    def get_goal_point(self, start_point):
        ref_vel = self.get_ref_velocity()
        tp = np.random.uniform(10, 100) # time horizon for planning
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

    def spawn_ego_vehicle(
            self, 
            ego_transform,
            out_path="topdown_traj.png",
            img_w=1024,
            img_h=1024,
            cam_height=60.0,
            fov_deg=90.0,
            ):
        try:
            blueprint_library = self.world.get_blueprint_library()
            ego_bp = blueprint_library.find("vehicle.mini.cooper")
            ego_bp.set_attribute("role_name", "hero")
            ego_bp.set_attribute("ros_name", "ego_vehicle")

            hero_vehicle = self.world.spawn_actor(ego_bp, ego_transform)
            hero_vehicle.set_autopilot(False)
            self.world.tick()

        
            if self.is_test_mode:
                print("[INFO] Ego vehicle spawned")
                # -----------------------------
                # Top view camera (store on self)
                # -----------------------------
                x_ego, y_ego = ego_transform.location.x, ego_transform.location.y
                yaw_ego = np.deg2rad(ego_transform.rotation.yaw)

                bp = blueprint_library.find("sensor.camera.rgb")
                bp.set_attribute("role_name", "rl_top_camera")
                bp.set_attribute("image_size_x", str(img_w))
                bp.set_attribute("image_size_y", str(img_h))
                bp.set_attribute("fov", str(fov_deg))
                bp.set_attribute("sensor_tick", "0.0")  # every tick in sync mode
                self.cam_height = cam_height
                cam_loc = carla.Location(x=x_ego, y=y_ego, z=self.cam_height)
                cam_rot = carla.Rotation(pitch=-90.0, yaw=np.rad2deg(yaw_ego), roll=0.0)
                cam_tf  = carla.Transform(cam_loc, cam_rot)

                cam = self.world.spawn_actor(bp, cam_tf, attachment_type=carla.AttachmentType.Rigid)

                # Store camera + queue + episode buffer on self
                self.top_cam = cam
                self.top_cam_q = queue.Queue(maxsize=5)
                self.top_cam_frames = []   # list of np arrays (HxWx3)
                self._top_cam_cb_count = 0


                cam.listen(self._cb)
                self.world.tick()  # wait for first frame   
                self.world.tick()  # ensure camera is fully ready


                print("[INFO] Top camera spawned & listening")

            return hero_vehicle

        except RuntimeError as e:
            print(f"[ERROR] Failed to spawn ego vehicle: {e}")
            return None

    def spawn_vehicles_around_ego(
        self,
        num=5,
        dist_candidates=(12.0, 18.0, 25.0, 35.0),
        min_dist=8.0,
        tm_port=None,
    ):
        """
        Spawn a small set (4-5) of NPC vehicles around ego using waypoints:
        - ahead in same lane
        - behind in same lane
        - left/right adjacent lane (if exists)
        Call AFTER ego spawn.
        Returns list of spawned actor IDs.
        """
        if self.ego_vehicle is None:
            return []

        if tm_port is None:
            tm_port = self.traffic_manager_port

        world = self.world
        m = self.map
        blueprints = world.get_blueprint_library().filter("vehicle.*")

        ego_tf = self.ego_vehicle.get_transform()
        ego_loc = ego_tf.location

        ego_wp = m.get_waypoint(ego_loc, project_to_road=True, lane_type=carla.LaneType.Driving)
        if ego_wp is None:
            return []

        vehicles_existing = world.get_actors().filter("vehicle.*")

        def is_free(loc: carla.Location) -> bool:
            for v in vehicles_existing:
                if v.id == self.ego_vehicle.id:
                    continue
                if v.get_location().distance(loc) < min_dist:
                    return False
            return True

        def try_spawn_at_wp(wp: carla.Waypoint):
            nonlocal vehicles_existing
            if wp is None:
                return None

            tf = wp.transform
            # slight lift to avoid ground collision on spawn
            tf.location.z += 0.5

            if not is_free(tf.location):
                return None

            bp = random.choice(blueprints)
            npc = world.try_spawn_actor(bp, tf)
            if npc is None:
                return None

            npc.set_autopilot(True, tm_port)
            vehicles_existing = world.get_actors().filter("vehicle.*")  # refresh
            return npc.id

        spawned = []

        # Build candidate waypoints around ego
        # 1) ahead + behind in same lane
        for d in dist_candidates:
            for wp in ego_wp.next(d):
                spawned_id = try_spawn_at_wp(wp)
                if spawned_id:
                    spawned.append(spawned_id)
                    break
            for wp in ego_wp.previous(d):
                spawned_id = try_spawn_at_wp(wp)
                if spawned_id:
                    spawned.append(spawned_id)
                    break

            if len(spawned) >= num:
                return spawned[:num]

        # 2) adjacent lanes near ego (left/right) then spawn ahead a bit
        left = ego_wp.get_left_lane()
        right = ego_wp.get_right_lane()

        adj_lanes = []
        if left and left.lane_type == carla.LaneType.Driving:
            adj_lanes.append(left)
        if right and right.lane_type == carla.LaneType.Driving:
            adj_lanes.append(right)

        for adj in adj_lanes:
            for d in dist_candidates:
                for wp in adj.next(d):
                    spawned_id = try_spawn_at_wp(wp)
                    if spawned_id:
                        spawned.append(spawned_id)
                        break
                if len(spawned) >= num:
                    return spawned[:num]

        return spawned[:num]

    def _cb(self, image):
        # Keep queue small: drop oldest if full (avoids lag)
        try:
            if self.top_cam_q.full():
                _ = self.top_cam_q.get_nowait()
            self.top_cam_q.put_nowait(image)
            self._top_cam_cb_count += 1
        except Exception:
            pass

    def get_ego_location(self):
        tf = self.ego_vehicle.get_transform()
        ego_location = (tf.location.x, tf.location.y, np.deg2rad(tf.rotation.yaw))       
        return ego_location
    
    def get_ego_control_cmd(self):
        if self.ego_vehicle is None:
            return None

        control = self.ego_vehicle.get_control()
        return control

    def get_ego_state(self):
        """
        Returns ego state in WORLD frame:
          (x_world, y_world, yaw_rad, vx_world, vy_world, L, W)

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
        #print("ego vehicle location: x=", x, "y=", y, "yaw=", yaw_rad)
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
        done_reason: str | None = None,
        ego_state=None,
        traj_waypoints=None,   # WORLD-frame waypoints from get_traj_wps()
        action = None          # WORLD-frame waypoints from RL output (same format as traj_waypoints)                  
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
        #r += self.terminal_reward(done_reason)
        #print("terminal reward: ", self.terminal_reward(done_reason))

        # Collision penalty (can still apply even if terminal already did it; usually keep one)
        # If you use terminal_reward(collision=-100), then set collision_penalty=0 or keep only one.
        r += self.collision_reward()
        #print("collision reward: ", self.collision_reward())

        # Near-collision shaping (only if we have a state)
        # if state is not None:
        #     r += self.near_collision_reward(state)
        #     print("near collision reward: ", self.near_collision_reward(state))

        # Trajectory following (WORLD frame)
        # if traj_waypoints is not None and len(traj_waypoints) >= 2:
        #     traj_r = self.trajectory_following_reward(ego_state, traj_waypoints)
        #     r += traj_r
        #     #print("trajectory following reward: ", traj_r)
        
        #reward for generating output trajectory that is close to the reference trajectory (WORLD frame)
        if traj_waypoints is not None and len(traj_waypoints) >= 2:
            r += self.deviation_penalty(traj_waypoints, action, sigma= 0.75, horizon_decay=3.0)
        
        # if done_reason == "stuck":
        #     r -= 50.0  # penalty for getting stuck (optional, tune as needed)
        # Lane keeping (needs current transform)
        # if getattr(self, "ego_vehicle", None) is not None:
        #     r += self.lane_following_reward(self.ego_vehicle.get_transform())
        #     print("lane following reward: ", self.lane_following_reward(self.ego_vehicle.get_transform()))

        # Speed tracking
        # r += self.speed_reward(ego_state)
        # print("speed reward: ", self.speed_reward(ego_state))

        # r += self.progressive_reward(ego_state)
        # print("progressive reward: ", self.progressive_reward(ego_state))

        # r += self.trajectory_reward(ego_state, traj_waypoints)
        # print("trajectory reward: ", self.trajectory_reward(ego_state, traj_waypoints))

        self.reward = r 
        #print("step count", self.step_count,"reward values: ", r)
        return r 

    def collision_reward(self) -> float:
        """One-step collision penalty (shaping)."""
        if self.sensor_fusion.collision_happened:
            type_id  = self.sensor_fusion.actor_collided
            if type_id.startswith("vehicle."):
                return self.collision_penalty
            else:
                return 0.0
        return 0.00

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
        #w = float(getattr(self, "w_traj", 1.0))
        reward = math.exp(-err)
        return reward 

    def deviation_penalty(self,
                          ref_xy,
                          gen_xy,
                          sigma=0.75,
                          horizon_decay=3.0):
        """
        ref_xy: (N,2) reference trajectory (input to RL)
        gen_xy: (N,2) generated trajectory (RL output)
        sigma: deviation tolerance (meters)
        horizon_decay: how fast weights decay for far waypoints
        
        Returns:
            R_dev in (-1, 1]
        """
    
        # ---- 1) Compute per-waypoint Euclidean deviation ----
        errors = np.linalg.norm(gen_xy[:,0:2] - ref_xy[:,0:2], axis=1)  # shape (N,)
    
        # ---- 2) Shifted Gaussian reward per waypoint ----
        # small deviation -> +1
        # large deviation -> approaches -1
        r_i = 2.0 * np.exp(-0.5 * (errors / sigma)**2) - 1.0
    
        # ---- 3) Horizon weighting (near-term matters more) ----
        N = len(errors)
        weights = np.exp(-np.arange(N) / horizon_decay)
        weights /= (weights.sum() + 1e-8)
    
        # ---- 4) Aggregate ----
        R_dev = 0.5 * float(np.sum(weights * r_i))
    
        return R_dev
    
    def speed_reward(self, ego_state) -> float:
            """Penalize deviation from reference speed (m/s)."""
            vx_w, vy_w = float(ego_state[3]), float(ego_state[4])
            speed = math.hypot(vx_w, vy_w)

            v_ref = float(getattr(self, "ref_velocity", 0.0))
            err = abs(speed - v_ref)
            w = 0.5 
            if err < 1.0:
                # Squared: Smooth and "quiet" near the target
                reward = -0.5 * (err ** 2)
            else:
                # Linear: Stable and won't explode at high speeds
                reward = -(err - 0.5) 
    
            return float(w * reward)


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

    def trajectory_reward(self, ego_state, traj_waypoints):
        """"
        traj_waypoints (10,3) in world frme, with rows [x_w, y_w, yaw_w]
        ego_state 
        """
        dx = np.diff(traj_waypoints[:, 0])
        dy = np.diff(traj_waypoints[:, 1])

        ref_velocity = self.get_ref_velocity()
        num_seg = len(traj_waypoints) - 1
        dist_th = (self.tf / max(num_seg, 1)) * ref_velocity

        dist = np.hypot(dx, dy)
        err = dist - dist_th

        r = 2.0 * np.exp(-0.5 * (err / self.err_sigma) ** 2) - 1.0
        r = np.clip(r, -1.0, 1.0)

        cons_points_reward = float(np.mean(r))
        x_progressive_r = float(np.mean(np.clip(dx, 0.0, None)))

        #delta_x <= th
        # x_diff = self.delta_x_th - delta_x
        # x_diff_r = np.sum(x_diff)

        # #delta_y <= th
        # delta_y = traj_waypoints[:,1] 
        # y_diff = self.delta_y_th - delta_y
        # y_diff_r = np.sum(y_diff)

        # #delta_yaw <= th 
        # delta_yaw = traj_waypoints[:,2]
        # yaw_diff = self.delta_yaw_th - delta_yaw
        # yaw_diff_r = np.sum(yaw_diff)
        #x_diff_r + y_diff_r + yaw_diff_r

        r =  cons_points_reward
        return r

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
        if self.sensor_fusion.collision_happened:
            return True, "collision"

        # 2) Goal reached
        ego_state = self.get_ego_state()
        x, y = float(ego_state[0]), float(ego_state[1])
        gx = float(self.goal_point.location.x)
        gy = float(self.goal_point.location.y)

        if math.hypot(x - gx, y - gy) <= self.goal_radius:
            return True, "goal_reached"

        # 3) Timeout
        
        if self.step_count >= self.max_episode_steps: 
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
        stuck_steps_limit = int(getattr(self, "stuck_steps_limit", 10))        # steps
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
        """
        action is (10,3) array of waypoints in ego frame: [x_w, y_w, yaw_w] - waypoints in worlf frame 
        """
        # Publish waypoints to controller
        ego_state = self.get_ego_state() 
        self.odom_publisher.publish_waypoints(ego_state)
        self.wp_publisher.publish_waypoints(action, self.ref_velocity)
         # (x,y,yaw,vx,vy,L, W)       
        
        self.world.tick()    
        self.step_count += 1

        done, reason = self.check_done()
        if self.traj_waypoints_world is None:
            print("[ERROR] traj_waypoints_world is None in step()")
            return None, None, True, {"done_reason": "traj_waypoints_none"}
        
        reward = self.calculate_reward(            
            done_reason=reason,
            ego_state=ego_state,
            traj_waypoints=self.traj_waypoints_world,   
            action=action         
        )


        if self.is_test_mode:
            self.update_top_cam_location(ego_state)
            self.capture_top_view_frame()
        #print("top cam que count: ", self._top_cam_cb_count, "queue size: ", self.top_cam_q.qsize())

        # keep actor cache fresh
        self.sensor_fusion.maybe_refresh_cache(self.step_count, refresh_every=20)       

        self.traj_waypoints_world = self.traj_obj.get_traj_wps(ego_state, self.ref_velocity)          # world
        if self.traj_waypoints_world is None:
            print("[ERROR] Trajectory generation returned None during reset.")
            return None, None, True, {"done_reason": "traj_generation_failed"}
        
        
        self.traj_waypoints_ego   = self.traj_obj.get_traj_wps_ego(ego_state, self.ref_velocity)      # ego
        state = self.sensor_fusion.get_current_state(traj_waypoints=self.traj_waypoints_ego, ego_state=ego_state, step_count=self.step_count)  # ego frame

        # if self.is_test_mode:
        #     print("Initial ego state and trajectory waypoints:")
        #     print("ego_state: ", ego_state)
        #     print("")
        #     print("traj_waypoints: ", self.traj_waypoints_world.shape)
        #     print("traj_waypoints: ", self.traj_waypoints_world)

        #     print("")
        #     print("traj_waypoints_ego: ", self.traj_waypoints_ego.shape)
        #     print("traj_waypoints_ego: ", self.traj_waypoints_ego)

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

    def preprocess_state(self, state: np.ndarray) -> np.ndarray:
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

    def get_centered_path(self, path):
        center_path = []
        for wp in path:
            location = carla.Location(x=wp[0], y=wp[1], z=0.0)
            center_wp = self.map.get_waypoint(location, project_to_road=True, lane_type=carla.LaneType.Driving)
            center = center_wp.transform.location
            center_path.append((center.x, center.y))        
        return np.array(center_path, dtype=np.float32)
    
    def spawn_test_vehicles_in_front(self, dist1=5.0, dist2=10.0, lateral_offset=0.5):
        """
        Spawns 2 vehicles in front of ego vehicle in ego frame.

        Args:
            dist1: distance of first vehicle ahead (meters)
            dist2: distance of second vehicle ahead (meters)
            lateral_offset: +left / -right offset (meters)

        Returns:
            list of spawned vehicle actors
        """

        if self.ego_vehicle is None:
            raise RuntimeError("Ego vehicle not initialized")

        world = self.world
        blueprint_library = world.get_blueprint_library()
        vehicle_bp = blueprint_library.filter("vehicle.*")[0]  # simple generic vehicle

        ego_tf = self.ego_vehicle.get_transform()
        ego_loc = ego_tf.location
        yaw_rad = np.deg2rad(ego_tf.rotation.yaw)

        cos_y = np.cos(yaw_rad)
        sin_y = np.sin(yaw_rad)

        spawned = []

        for dist in [dist1, dist2]:

            # Forward direction (ego frame x)
            dx = dist * cos_y
            dy = dist * sin_y

            # Lateral offset (ego frame y)
            lx = -lateral_offset * sin_y
            ly =  lateral_offset * cos_y

            spawn_loc = carla.Location(
                x=ego_loc.x + dx + lx,
                y=ego_loc.y + dy + ly,
                z=ego_loc.z + 0.5  # small lift to avoid ground collision
            )

            spawn_tf = carla.Transform(spawn_loc, ego_tf.rotation)

            npc = world.try_spawn_actor(vehicle_bp, spawn_tf)

            if npc is not None:
                npc.set_autopilot(False)
                spawned.append(npc)

        print(f"Spawned {len(spawned)} test vehicles")
        self.world.tick()  # ensure they are fully spawned
        return spawned

    def get_max_LW(self):
        max_L = 12
        max_W = 5
        return max_L, max_W

    def capture_top_view_frame(self, timeout_s: float = 0.2) -> bool:
        """
        Call AFTER self.world.tick() inside step().
        Grabs the latest camera image from the queue, converts to RGB numpy array,
        and appends to self.top_cam_frames.

        Returns True if a frame was captured, else False.
        """
        if not hasattr(self, "top_cam_q") or self.top_cam_q is None:
            return False

        # Block briefly to sync with the tick
        try:
            image = self.top_cam_q.get(timeout=timeout_s)
        except queue.Empty:
            print("[WARN] No top-down camera frame received in time")
            return False

        # Drain any extra frames, keep the most recent (prevents lag)
        while True:
            try:
                image = self.top_cam_q.get_nowait()
            except queue.Empty:
                #print("[INFO] Captured top-down frame, queue is now empty")
                break

        # CARLA image raw_data is BGRA
        arr = np.frombuffer(image.raw_data, dtype=np.uint8)
        arr = arr.reshape((image.height, image.width, 4))      # BGRA
        rgb = arr[:, :, :3][:, :, ::-1].copy()                 # -> RGB, detach memory

        self.top_cam_frames.append(rgb)
        return True

    def save_topdown_snapshot_world_traj(
        self,
        ego_state,
        traj_world,
        out_path="topdown_traj.png",
        img_w=1024,
        img_h=1024,
        cam_height=60.0,
        fov_deg=90.0,
        timeout_s=2.0,
        dot_radius=4,
        line_thickness=2,
    ):
        """
        Take a top-down RGB snapshot centered on ego and overlay a WORLD-frame trajectory.

        Args:
            ego_state: (x, y, yaw_rad, vx, vy, L, W) OR any sequence where [0]=x, [1]=y, [2]=yaw_rad
            traj_world: (N,2) or (N,3+) array-like with columns [x_world, y_world, ...]
            out_path: where to save PNG/JPG
        Returns:
            bgr image np.ndarray (H,W,3)
        """

        if ego_state is None:
            raise ValueError("ego_state is None")
        if traj_world is None:
            raise ValueError("traj_world is None")

        x_ego = float(ego_state[0])
        y_ego = float(ego_state[1])
        yaw_ego = float(ego_state[2])  # rad
        yaw_ego = (yaw_ego + np.pi) % (2*np.pi) - np.pi

        traj_world = np.asarray(traj_world, dtype=np.float32)
        if traj_world.ndim != 2 or traj_world.shape[1] < 2:
            raise ValueError(f"traj_world must be (N,2+) got {traj_world.shape}")

        # points to project (z a bit above ground)
        pts_world = np.zeros((traj_world.shape[0], 3), dtype=np.float32)
        pts_world[:, 0] = traj_world[:, 0]
        pts_world[:, 1] = traj_world[:, 1]
        pts_world[:, 2] = 0.3

        # -------------------------
        # Spawn temporary top-down RGB camera
        # -------------------------
        bp = self.world.get_blueprint_library().find("sensor.camera.rgb")
        bp.set_attribute("image_size_x", str(img_w))
        bp.set_attribute("image_size_y", str(img_h))
        bp.set_attribute("fov", str(fov_deg))

        cam_loc = carla.Location(x=x_ego, y=y_ego, z=cam_height)
        cam_rot = carla.Rotation(pitch=-90.0, yaw=np.rad2deg(yaw_ego), roll=0.0)
        cam_tf = carla.Transform(cam_loc, cam_rot)

        cam = self.world.spawn_actor(bp, cam_tf)
        q = queue.Queue()

        def _cb(image):
            q.put(image)

        cam.listen(_cb)

        try:
            # ensure a fresh frame
            self.world.tick()

            image = q.get(timeout=timeout_s)

            # BGRA -> BGR
            arr = np.frombuffer(image.raw_data, dtype=np.uint8).reshape((image.height, image.width, 4))
            bgr = arr[:, :, :3].copy()

            # -------------------------
            # Project WORLD -> IMAGE
            # -------------------------
            fov = np.deg2rad(fov_deg)
            fx = img_w / (2.0 * np.tan(fov / 2.0))
            fy = fx
            cx = img_w / 2.0
            cy = img_h / 2.0

            cam_to_world = np.array(cam_tf.get_matrix(), dtype=np.float32)
            world_to_cam = np.linalg.inv(cam_to_world).astype(np.float32)

            N = pts_world.shape[0]
            pts_h = np.ones((N, 4), dtype=np.float32)
            pts_h[:, :3] = pts_world

            pts_cam = (world_to_cam @ pts_h.T).T  # (N,4)
            X = pts_cam[:, 0]
            Y = pts_cam[:, 1]
            Z = pts_cam[:, 2]

            # In front of camera => X > 0 in CARLA camera frame
            valid = X > 0.1

            uv = np.full((N, 2), np.nan, dtype=np.float32)
            if np.any(valid):
                x = X[valid]
                y = Y[valid]
                z = Z[valid]
                u = fx * (y / x) + cx
                v = fy * (-z / x) + cy
                uv[valid, 0] = u
                uv[valid, 1] = v

            # Ego marker
            ego_pt = np.array([[x_ego, y_ego, 0.3]], dtype=np.float32)
            ego_h = np.ones((1, 4), dtype=np.float32)
            ego_h[:, :3] = ego_pt
            ego_cam = (world_to_cam @ ego_h.T).T
            if ego_cam[0, 0] > 0.1:
                ex = fx * (ego_cam[0, 1] / ego_cam[0, 0]) + cx
                ey = fy * (-ego_cam[0, 2] / ego_cam[0, 0]) + cy
                if np.isfinite(ex) and np.isfinite(ey):
                    exi, eyi = int(round(ex)), int(round(ey))
                    if 0 <= exi < img_w and 0 <= eyi < img_h:
                        cv2.drawMarker(
                            bgr, (exi, eyi), (0, 255, 255),
                            markerType=cv2.MARKER_CROSS, markerSize=22, thickness=2
                        )

            # Collect in-bounds pixels
            pts_px = []
            for i in range(N):
                u, v = uv[i]
                if not np.isfinite(u) or not np.isfinite(v):
                    continue
                ui, vi = int(round(u)), int(round(v))
                if 0 <= ui < img_w and 0 <= vi < img_h:
                    pts_px.append((ui, vi))

            # Draw trajectory polyline + dots
            if len(pts_px) >= 2:
                cv2.polylines(bgr, [np.array(pts_px, dtype=np.int32)], False, (0, 255, 0), line_thickness)
            for p in pts_px:
                cv2.circle(bgr, p, dot_radius, (0, 0, 255), -1)

            cv2.imwrite(out_path, bgr)
            #print(f"Saved top-down trajectory snapshot to {out_path}")
            return bgr

        finally:
            try:
                cam.stop()
            except Exception:
                pass
            try:
                cam.destroy()
            except Exception:
                pass

    def update_top_cam_location(self, ego_state):
        if self.is_test_mode and self.top_cam is not None:

            x_ego, y_ego, yaw_ego = ego_state[0:3]
            cam_loc = carla.Location(
                x=x_ego,
                y=y_ego,
                z=self.cam_height     # store cam_height as self.cam_height during spawn
            )
            cam_rot = carla.Rotation(
                pitch=-90.0,
                yaw=yaw_ego,
                roll=0.0
            )
            cam_tf = carla.Transform(cam_loc, cam_rot)    
            self.top_cam.set_transform(cam_tf)

    def save_top_view_video(self,
                            out_path: str,
                            fps: float = 20.0,
                            clear_buffer: bool = True) -> str:
        """
        Save the buffered top-view frames (self.top_cam_frames) to an MP4 file.

        Call this from Trainer when done=True.

        Requirements:
          - self.top_cam_frames is a list of RGB frames (HxWx3 uint8)

        Args:
            out_path: output path ending with .mp4
            fps: frames per second for the output video
            clear_buffer: if True, clears self.top_cam_frames after saving

        Returns:
            out_path

        Raises:
            ValueError / RuntimeError on invalid frames or writer issues
        """
        if not hasattr(self, "top_cam_frames") or self.top_cam_frames is None:
            raise ValueError("Env has no top_cam_frames buffer. Did you initialize it in spawn/reset?")

        frames = self.top_cam_frames
        if len(frames) == 0:
            raise ValueError("top_cam_frames is empty. Nothing to save.")

        f0 = frames[0]
        if not isinstance(f0, np.ndarray) or f0.ndim != 3 or f0.shape[2] != 3:
            raise ValueError("Frames must be numpy arrays of shape (H, W, 3).")
        if f0.dtype != np.uint8:
            raise ValueError("Frames must be dtype uint8 (RGB).")

        h, w = f0.shape[:2]
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(out_path, fourcc, float(fps), (w, h))
        if not writer.isOpened():
            raise RuntimeError(f"Failed to open VideoWriter for: {out_path}")

        try:
            for i, rgb in enumerate(frames):
                if rgb.shape[:2] != (h, w):
                    raise ValueError(f"Frame {i} shape mismatch: expected {(h, w)}, got {rgb.shape[:2]}")
                if rgb.dtype != np.uint8:
                    raise ValueError(f"Frame {i} dtype mismatch: expected uint8, got {rgb.dtype}")

                # cv2 wants BGR
                bgr = rgb[:, :, ::-1]
                writer.write(bgr)
                
        finally:
            writer.release()
        #print("saved video with frames ", len(frames))
        if clear_buffer:
            frames.clear()        
        return out_path

if __name__ == "__main__":
   env = Env(traffic_manager_port=8000, traffic_size=40, v_min=0.0, v_max=10.0, a_min=-3.0, a_max=3.0, lateral_accel=2.0)
   env.reset()


