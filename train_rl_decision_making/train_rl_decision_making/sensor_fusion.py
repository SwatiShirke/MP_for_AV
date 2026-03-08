import carla
import numpy as np
import cv2
import math
import threading
from ultralytics import YOLO
import random
import time


class SensorFusion:
    """
    Camera (YOLOv8) + LiDAR + Fusion
    In-process CARLA perception module for RL
    """

    def __init__(
        self,
        world,        
        min_distance,
        yolo_model,
        max_objects=10,
        ego_vehicle=None
    ):
        self.world = world        
        self.max_objects = max_objects
        self.min_distance = min_distance  # meters, tune to remove ego reflections from lidar points
        self.yolo = yolo_model
        self.ego_vehicle = ego_vehicle
        # -----------------------
        # Camera parameters
        # -----------------------
        self.image_w = 1280
        self.image_h = 720
        self.fov = 90.0

        self.cam_tf = carla.Transform(
            carla.Location(x=0.0, y=0.0, z=2.4),
            carla.Rotation()
        )

        # -----------------------
        # LiDAR parameters
        # -----------------------
        self.lidar_tf = carla.Transform(
            carla.Location(x=1.2, y=0.0, z=2.8)
        )
        

        # -----------------------
        # YOLO
        
        self.conf_thres = 0.25
        self.iou_thres = 0.45
        self.vehicle_class_ids = {2, 3, 5, 7}

        # -----------------------
        # Camera intrinsics
        # -----------------------
        self.fx = (self.image_w / 2.0) / math.tan(math.radians(self.fov) / 2.0)
        self.fy = self.fx
        self.cx = self.image_w / 2.0
        self.cy = self.image_h / 2.0

        # -----------------------
        # Fusion parameters
        # -----------------------
        self.min_points_in_bbox = 5
        self.bbox_margin = 16.0
        self.depth_lo = 5.0
        self.depth_hi = 95.0

        # -----------------------
        # Internal buffers
        # -----------------------
        self._latest_rgb = None
        self._latest_detections = None
        self._latest_lidar = None
        self._latest_fused = None

        # -----------------------
        # Vehicle cache (GT association)
        # -----------------------
        self._vehicle_cache = []
        self._vehicle_cache_ts = 0.0
        self._cache_period_s = 1.0   # refresh actor list every 1 second
        self._gate_radius = 6.0      # meters, tune (4-8 typical)
        
        # -----------------------
        # Stable slot assignment (track ID -> fixed row)
        # -----------------------
        self._id_to_slot = {}                         # dict: actor_id -> slot index
        self._slot_to_id = [None] * self.max_objects  # list: slot index -> actor_id
        self._slot_last_seen = [-10**9] * self.max_objects  # last seen step per slot (int)
        self._track_ttl_steps = 15    # free slot if not seen for this many steps
        
        # --- track persistence (hold) ---
        self.hold_k = 10                 # frames to hold last value after a miss (at 20Hz: 10 = 0.5s)
        self.decay_flag = True           # optionally decay confidence/flag while holding

        # Per-track memory:
        # track_id -> dict(slot=int, row=np.ndarray(8,), last_seen=int)
        self._track_mem = {}


        self._lock = threading.Lock()

        self.camera = None
        self.lidar = None
        self.setup()

        
    # =========================================================
    # Setup
    # =========================================================
    def setup(self):        
        self._spawn_camera()
        self._spawn_lidar()
        self.spawn_collision_sensor()

    def _spawn_camera(self):
        bp = self.world.get_blueprint_library().find('sensor.camera.rgb')
        bp.set_attribute("role_name", "rl_sensor_camera")
        bp.set_attribute('image_size_x', str(self.image_w))
        bp.set_attribute('image_size_y', str(self.image_h))
        bp.set_attribute('fov', str(self.fov))
        bp.set_attribute("sensor_tick", "0.0")  # 10 Hz
        self.camera = self.world.spawn_actor(bp, self.cam_tf, attach_to=self.ego_vehicle)
        self.camera.listen(self._camera_callback)

    def _spawn_lidar(self):
        bp = self.world.get_blueprint_library().find('sensor.lidar.ray_cast')
        bp.set_attribute("role_name", "rl_sensor_lidar")
        bp.set_attribute('range', '50')
        bp.set_attribute('channels', '32')
        bp.set_attribute('points_per_second', '50000')
        bp.set_attribute('rotation_frequency', '20')
        bp.set_attribute('upper_fov', '10')
        bp.set_attribute('lower_fov', '-30')
        bp.set_attribute("sensor_tick", "0.0")  # 10 Hz

        self.lidar = self.world.spawn_actor(bp, self.lidar_tf, attach_to=self.ego_vehicle)
        self.lidar.listen(self._lidar_callback)

    def spawn_collision_sensor(self):
        bp = self.world.get_blueprint_library().find("sensor.other.collision")
        transform = carla.Transform(carla.Location(x=0.0, z=1.0))
        self.collision_sensor = self.world.spawn_actor(bp, transform, attach_to=self.ego_vehicle)
    
        self.collision_happened = False          
        self.collision_sensor.listen(self._on_collision)


    # =========================================================
    # Callbacks
    # =========================================================
    def _camera_callback(self, img):
        arr = np.frombuffer(img.raw_data, dtype=np.uint8).reshape(
            (img.height, img.width, 4)
        )[:, :, :3]

        rgb = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)

        #cv2.imwrite("camera_debug.jpg", rgb)

        results = self.yolo(
            rgb,
            imgsz=896,
            conf=self.conf_thres,
            iou=self.iou_thres,
            device='cpu',
            verbose=False
        )[0]

        detections = []
        if results.boxes is not None:
            for b in results.boxes:
                cls_id = int(b.cls[0])
                if cls_id not in self.vehicle_class_ids:
                    continue

                x1, y1, x2, y2 = b.xyxy[0].cpu().numpy()
                conf = float(b.conf[0])

                detections.append({
                    "cls": cls_id,
                    "conf": conf,
                    "bbox": [(x1+x2)/2, (y1+y2)/2, x2-x1, y2-y1]
                })

        with self._lock:
            self._latest_detections = detections

    def _lidar_callback(self, data):
        # Raw CARLA LiDAR: (x, y, z, intensity)
        pts = np.frombuffer(
            data.raw_data, dtype=np.float32
        ).reshape(-1, 4)[:, :3]

        if pts.shape[0] == 0:
            return

        # 1) Keep points in front of ego vehicle
        pts = pts[pts[:, 0] > 0.0]

        if pts.shape[0] == 0:
            return

        # 2) Lane-width filter (remove far left/right clutter)
        pts = pts[np.abs(pts[:, 1]) < 5.0]

        if pts.shape[0] == 0:
            return

        # 3) Ground / deep returns removal
        pts = pts[pts[:, 2] > -2.0]

        if pts.shape[0] == 0:
            return

        # 4) Ignore extremely close points (ego reflections / hood)
        dist = np.linalg.norm(pts, axis=1)
        pts = pts[dist > self.min_distance]

        if pts.shape[0] == 0:
            return

        # -------------------------------------------------
        # Store filtered LiDAR points
        # -------------------------------------------------
        with self._lock:
            self._latest_lidar = pts

    def _on_collision(self, event):
        self.collision_happened = True
        self.actor_collided = event.other_actor.type_id 

    # =========================================================
    # Vehicle cache helpers
    # =========================================================
    def _refresh_vehicle_cache(self):
        actors = self.world.get_actors().filter("vehicle.*")
        self._vehicle_cache = [a for a in actors if a.id != self.ego_vehicle.id]

        snap = self.world.get_snapshot()
        self._vehicle_cache_ts = snap.timestamp.elapsed_seconds if snap else time.time()

    @staticmethod
    def _wrap_to_pi(angle_rad: float) -> float:
        return (angle_rad + np.pi) % (2.0 * np.pi) - np.pi

    def _match_vehicle_gt(self, pred_world_xy, gate_radius=None):
        """
        pred_world_xy: (xw, yw) predicted obstacle center in world frame
        returns: matched carla.Vehicle or None
        """
        if gate_radius is None:
            gate_radius = self._gate_radius
       
    
        px, py = float(pred_world_xy[0]), float(pred_world_xy[1])
        r2 = gate_radius * gate_radius

        best = None
        best_d2 = float("inf")

        for v in self._vehicle_cache:
            loc = v.get_location()  # current location (changes every tick)
            dx = loc.x - px
            dy = loc.y - py
            d2 = dx * dx + dy * dy
            if d2 < r2 and d2 < best_d2:
                best = v
                best_d2 = d2

        return best

    def _get_vehicle_yaw_LW(self, vehicle: carla.Vehicle):
        """
        returns (yaw_world_rad, length_m, width_m)
        """
        tf = vehicle.get_transform()
        yaw_world_rad = np.deg2rad(tf.rotation.yaw)

        bb = vehicle.bounding_box
        length_m = 2.0 * bb.extent.x
        width_m  = 2.0 * bb.extent.y
        return yaw_world_rad, length_m, width_m


    # =========================================================
    # =========================================================
    # Fusion + State API
    # =========================================================
    
    def compute_sensor_state(self, ego_state=None, step_count=0):
        """
        Returns obs: (max_objects, 8)
          [x_ego, y_ego, yaw_rel, L, W, v_rel_x_ego, v_rel_y_ego, flag]

        step_count: int, monotonically increasing env step. Used for TTL slot cleanup.
        """        
        #print("Computing sensor state...")
        # ---- Expire old tracks (free slots)
        # Safe to run every call; O(max_objects)
        for slot in range(self.max_objects):
            track_id = self._slot_to_id[slot]
            if track_id is None:
                continue
            if (int(step_count) - int(self._slot_last_seen[slot])) > int(self._track_ttl_steps):
                # free slot
                self._id_to_slot.pop(track_id, None)
                self._slot_to_id[slot] = None
                self._slot_last_seen[slot] = -10**9

        with self._lock:
            dets = self._latest_detections
            pts = self._latest_lidar

        obs = np.zeros((self.max_objects, 8), dtype=np.float32)
        #print("dets", dets)
        if dets is None or pts is None:
            return obs

        # Need ego pose + ego world velocity
        # ego_state: (x_world, y_world, yaw_rad, vx_world, vy_world)
        if ego_state is None:
            tf = self.ego_vehicle.get_transform()
            vel = self.ego_vehicle.get_velocity()
            ego_state = (
                float(tf.location.x),
                float(tf.location.y),
                float(np.deg2rad(tf.rotation.yaw)),
                float(vel.x),
                float(vel.y),
            )

        x0, y0, ego_yaw, ego_vx_w, ego_vy_w, ego_L, ego_W,  = ego_state

        # -----------------------------
        # Existing LiDAR -> ego -> camera projection
        # -----------------------------
        xp, yp, zp = self.lidar_tf.location.x, self.lidar_tf.location.y, self.lidar_tf.location.z
        xc, yc, zc = self.cam_tf.location.x, self.cam_tf.location.y, self.cam_tf.location.z

        pts_ego = pts + np.array([xp, yp, zp], dtype=np.float32)
        pts_cam = pts_ego - np.array([xc, yc, zc], dtype=np.float32)

        Xc = pts_cam[:, 1]
        Yc = -pts_cam[:, 2]
        Zc = pts_cam[:, 0]

        mask = Zc > 0.1
        Xc, Yc, Zc = Xc[mask], Yc[mask], Zc[mask]
        pts_ego = pts_ego[mask]

        u = self.fx * (Xc / Zc) + self.cx
        v = self.fy * (Yc / Zc) + self.cy

        valid = (u >= 0) & (u < self.image_w) & (v >= 0) & (v < self.image_h)
        u, v, Zc, pts_ego = u[valid], v[valid], Zc[valid], pts_ego[valid]

        # print("dets", dets)
        # NOTE: We no longer use idx to place rows; slot is determined by track_id
        for d in dets:
            cx, cy, sx, sy = d["bbox"]
            x1, y1 = cx - sx / 2 - self.bbox_margin, cy - sy / 2 - self.bbox_margin
            x2, y2 = cx + sx / 2 + self.bbox_margin, cy + sy / 2 + self.bbox_margin

            inside = (u >= x1) & (u <= x2) & (v >= y1) & (v <= y2)
            if np.count_nonzero(inside) < self.min_points_in_bbox:
                continue

            pts_sel = pts_ego[inside]
            z_sel = Zc[inside]

            lo, hi = np.percentile(z_sel, [self.depth_lo, self.depth_hi])
            keep = (z_sel >= lo) & (z_sel <= hi)
            if np.count_nonzero(keep) < 3:
                continue

            pos_ego = np.median(pts_sel[keep], axis=0)  # [x,y,z] in ego frame
            x_e, y_e = float(pos_ego[0]), float(pos_ego[1])

            # Predict world xy for GT association
            pred_world_xy = self._ego_to_world((x0, y0, ego_yaw), (x_e, y_e))

            matched = self._match_vehicle_gt(pred_world_xy)
            if matched is None:
                continue
            
            # print("###############################################")
            # print(f"[MATCH] step={step_count}  "
            #       f"track_id={matched.id}  "
            #       f"pred_world=({pred_world_xy[0]:.2f},{pred_world_xy[1]:.2f})  "
            #       f"gt_world=({matched.get_location().x:.2f},{matched.get_location().y:.2f})")
              

            track_id = int(matched.id)

            # Get or allocate stable slot
            slot = self._id_to_slot.get(track_id, None)
            if slot is None:
                slot = self._alloc_slot_for(track_id)

            # yaw, length, width (world yaw, L/W in meters)
            yaw_w, L, W = self._get_vehicle_yaw_LW(matched)
            yaw_rel = self._wrap_to_pi(yaw_w - ego_yaw)

            # relative velocity in ego frame
            v_obj = matched.get_velocity()  # world frame
            v_rel_wx = float(v_obj.x) - float(ego_vx_w)
            v_rel_wy = float(v_obj.y) - float(ego_vy_w)
            v_rel_ex, v_rel_ey = self._world_to_ego_vec2(ego_yaw, v_rel_wx, v_rel_wy)

            obs[slot] = [
                x_e, y_e,
                float(yaw_rel),
                float(L), float(W),
                float(v_rel_ex), float(v_rel_ey),
                1.0
            ]

            # update last seen for this slot
            self._slot_last_seen[slot] = int(step_count)
        # print("obs shape", obs.shape)
        # print("here npw######################3")
        #print("obs", obs) 
        return obs


        # Helper to allocate a slot for a new track_id
    
    def _alloc_slot_for(self, track_id: int) -> int:
        # 1) any completely free slot?
        for s in range(self.max_objects):
            if self._slot_to_id[s] is None:
                self._slot_to_id[s] = track_id
                self._id_to_slot[track_id] = s
                return s

        # 2) evict the stalest slot (oldest last_seen)
        stalest_slot = int(np.argmin(np.array(self._slot_last_seen, dtype=np.int64)))
        old_id = self._slot_to_id[stalest_slot]
        if old_id is not None:
            self._id_to_slot.pop(old_id, None)
        self._slot_to_id[stalest_slot] = track_id
        self._id_to_slot[track_id] = stalest_slot
        return stalest_slot
    
    # =========================================================
    # get_current_state() --- 
    #==========================================================

    def get_current_state(self, traj_waypoints=None, ego_state=None, step_count=0):
        """
        traj_waypoints: (N,2) in ego frame
        ego_state: (x, y, yaw, vx, vy, L, W) in world frame (yaw radians)
        step_count: int step index (used for stable ID slot TTL in compute_sensor_state)

        Returns:
          state_arr: (1 + max_objects + N, 8)
          Rows:
            ego row:       [0,0,0, ego_L, ego_W, ego_vx_ego, ego_vy_ego, 1]
            obstacle rows: [x,y,yaw_rel, L, W, v_rel_x, v_rel_y, flag]   (stable slots)
            traj rows:     [x,y,0,0,0,0,0,1]
        """
        N_traj = 10 if traj_waypoints is None else int(traj_waypoints.shape[0])

        if ego_state is None or traj_waypoints is None:
            return np.zeros((1 + self.max_objects + N_traj, 8), dtype=np.float32)

        # ---- obstacles in stable slots (max_objects, 8) in ego frame
        obs_array = self.compute_sensor_state(ego_state=ego_state, step_count=step_count)
        
        
        _, _, ego_yaw, ego_vx_w, ego_vy_w, ego_L, ego_W  = ego_state 
        ego_vx_e, ego_vy_e = self._world_to_ego_vec2(float(ego_yaw), float(ego_vx_w), float(ego_vy_w))

        ego_row = np.array([[0.0, 0.0, 0.0,
                             float(ego_L), float(ego_W),
                             float(ego_vx_e), float(ego_vy_e),
                             1.0]], dtype=np.float32)

        # ---- trajectory rows (N,8)
        traj_array = np.zeros((traj_waypoints.shape[0], 8), dtype=np.float32)
        traj_array[:, 0:2] = traj_waypoints[:, 0:2]
        traj_array[:, 7] = 1.0

        # print("ego_row shape", ego_row.shape)
        # print("obs_array shape", obs_array.shape)
        # print("traj_array shape", traj_array.shape)
        state_arr = np.vstack((ego_row, obs_array, traj_array)).astype(np.float32)
        # print("state_arr shape", state_arr.shape)

        # print(" ")
        # print("state", state_arr)
        return state_arr


    #========================================================
    # Coordinate transformation helper (point from ego to world frame)
    #========================================================
    def _ego_to_world(self, ego_location, obs_xy_ego):
        x0, y0, yaw = ego_location  # yaw in radians    
        xe, ye = float(obs_xy_ego[0]), float(obs_xy_ego[1])

        c = np.cos(yaw)
        s = np.sin(yaw)

        xw = x0 + xe * c - ye * s
        yw = y0 + xe * s + ye * c

        return xw, yw



    #==========================================================
    # refresh_cache() --- public method to allow manual cache refresh from env.py
    #=========================================================
    def maybe_refresh_cache(self, step_count: int, refresh_every: int = 20):
        if step_count % refresh_every == 0:
            self._refresh_vehicle_cache()


    def _world_to_ego_vec2(self, ego_yaw, vx_w, vy_w):
        """
        Rotate a 2D vector from world frame into ego frame.
        Ego frame: x forward, y left.

        v_ego = R(-ego_yaw) * v_world
        """
        c = float(np.cos(ego_yaw))
        s = float(np.sin(ego_yaw))
        vx_e =  c * vx_w + s * vy_w
        vy_e = -s * vx_w + c * vy_w
        return vx_e, vy_e
    
    # =========================================================
    # test code
    # =========================================================


    def spawn_vehicle_in_front(
        self,     
        distance=15.0,
        lateral_offset=0.0,
        vehicle_filter="vehicle.*",
        autopilot=False
    ):
        """
        Spawns a vehicle in front of ego vehicle.

        Args:
            distance (float): meters ahead of ego
            lateral_offset (float): meters to the right (+) or left (-)
            vehicle_filter (str): CARLA blueprint filter
            autopilot (bool): enable autopilot on spawned vehicle

        Returns:
            carla.Vehicle or None
        """

        blueprint_library = self.world.get_blueprint_library()
        vehicle_bps = blueprint_library.filter(vehicle_filter)
        if not vehicle_bps:
            raise RuntimeError("No vehicle blueprints found")

        bp = random.choice(vehicle_bps)

        # Get ego transform
        ego_tf = self.ego_vehicle.get_transform()
        ego_loc = ego_tf.location
        ego_rot = ego_tf.rotation

        # Ego forward & right vectors
        yaw_rad = math.radians(ego_rot.yaw)
        forward = carla.Vector3D(
            x=math.cos(yaw_rad),
            y=math.sin(yaw_rad),
            z=0.0
        )
        right = carla.Vector3D(
            x=-math.sin(yaw_rad),
            y=math.cos(yaw_rad),
            z=0.0
        )

        # Compute spawn location
        spawn_loc = ego_loc + forward * distance + right * lateral_offset
        spawn_loc.z += 0.1  # avoid ground collision

        print("spawned location for obstacle vehicle", spawn_loc)

        spawn_tf = carla.Transform(
            spawn_loc,
            carla.Rotation(yaw=ego_rot.yaw)
        )

        vehicle = self.world.try_spawn_actor(bp, spawn_tf)
        if vehicle is None:
            print("[TEST] Failed to spawn vehicle (collision)")
            return None

        if autopilot:
            vehicle.set_autopilot(True)

        print(
            f"[TEST] Spawned vehicle id={vehicle.id} "
            f"at {distance:.1f} m ahead, lateral {lateral_offset:.1f} m"
        )

        return vehicle

    def test_fusion(self, num_vehicles=5):
        # Protect against empty cache at start
        self._refresh_vehicle_cache()  # ensure cache is fresh for test
        step_count = 0
        for _ in range(70):
            self.world.tick()

            tf = self.ego_vehicle.get_transform()
            vel = self.ego_vehicle.get_velocity()

            ego_state = (
                float(tf.location.x),
                float(tf.location.y),
                float(np.deg2rad(tf.rotation.yaw)),
                float(vel.x),
                float(vel.y),
                float(self.ego_vehicle.bounding_box.extent.x * 2.0),  # length
                float(self.ego_vehicle.bounding_box.extent.y * 2.0)   # width
            )

            traj_waypoints = np.zeros((10, 2), dtype=np.float32)

            state = self.get_current_state(traj_waypoints=traj_waypoints, ego_state=ego_state)
            step_count += 1 
            time.sleep(0.02)
            self.maybe_refresh_cache(step_count, refresh_every=20)
            #print("\n", state)

    # =========================================================
    # Cleanup
    # =========================================================
    def destroy(self):
        if self.camera:
            self.camera.stop()
            self.camera.destroy()
        if self.lidar:
            self.lidar.stop()
            self.lidar.destroy()

        if self.collision_sensor:
            self.collision_sensor.stop()
            self.collision_sensor.destroy()
    # =========================================================
    # main
    # =========================================================

def spawn_ego_vehicle(
        world,
        blueprint_filter="vehicle.tesla.model3",
        spawn_point=None,
        role_name="hero",
        autopilot=False
    ):
        """
        Spawns ego vehicle in CARLA.

        Args:
            world (carla.World)
            blueprint_filter (str)
            spawn_point (carla.Transform or None)
            role_name (str)
            autopilot (bool)

        Returns:
            carla.Vehicle
        """

        bp_lib = world.get_blueprint_library()
        candidates = bp_lib.filter(blueprint_filter)
        if not candidates:
            raise RuntimeError(f"No vehicle blueprint matches '{blueprint_filter}'")

        bp = random.choice(candidates)
        bp.set_attribute("role_name", role_name)

        # Choose spawn point
        # if spawn_point is None:
        #     spawn_points = world.get_map().get_spawn_points()
        #     if not spawn_points:
        #     raise RuntimeError("No spawn points available on map")
        #     spawn_point = random.choice(spawn_points)



        vehicle = world.try_spawn_actor(bp, spawn_point)
        if vehicle is None:
            raise RuntimeError("Failed to spawn ego vehicle (collision at spawn point)")

        vehicle.set_autopilot(autopilot)
        print(f"[EGO] Spawned ego vehicle at {spawn_point.location}")
        return vehicle

def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    # ---- Enable synchronous mode for deterministic ticks (recommended for RL/testing)
    original_settings = world.get_settings()
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05  # 20 Hz sim tick (choose what you want)
    world.apply_settings(settings)

    ego_vehicle = None
    obstacle_vehicle1 = None
    obstacle_vehicle2 = None
    obstacle_vehicle3 = None
    fusion = None

    try:
        # ------------------ Ego Vehicle ------------------
        ego_bp = blueprint_library.find("vehicle.mini.cooper")
        ego_bp.set_attribute("role_name", "hero")
        ego_bp.set_attribute("ros_name", "ego_vehicle")

        ego_transform = carla.Transform(
            carla.Location(x=-64.644844, y=24.471010, z=0.6),
            carla.Rotation(yaw=0)
        )

        ego_vehicle = world.try_spawn_actor(ego_bp, ego_transform)
        if ego_vehicle is None:
            raise RuntimeError("Failed to spawn ego vehicle (collision at spawn point).")

        ego_vehicle.set_autopilot(False)
        print("[INFO] Ego vehicle spawned")

        #------------------ Obstacle Vehicle 1 ------------------
        obs_bp = blueprint_library.find("vehicle.mini.cooper")
        obs_bp.set_attribute("role_name", "obstacle")

        obs_transform1 = carla.Transform(
            carla.Location(x=-54.644844, y=24.471010, z=0.6),
            carla.Rotation(yaw=180)
        )

        obstacle_vehicle1 = world.try_spawn_actor(obs_bp, obs_transform1)
        if obstacle_vehicle1 is None:
            print("[WARN] Failed to spawn obstacle vehicle 1 (collision).")
        else:
            obstacle_vehicle1.set_autopilot(False)
            print("[INFO] Obstacle vehicle 1 spawned")

        #------------------ Obstacle Vehicle 2 ------------------
        obs_bp2 = blueprint_library.find("vehicle.mini.cooper")
        obs_bp2.set_attribute("role_name", "obstacle")

        obs_transform2 = carla.Transform(
            carla.Location(x=-52.4844, y=28.471010, z=0.6),
            carla.Rotation(yaw=180)
        )

        obstacle_vehicle2 = world.try_spawn_actor(obs_bp2, obs_transform2)
        if obstacle_vehicle2 is None:
            print("[WARN] Failed to spawn obstacle vehicle 2 (collision).")
        else:
            obstacle_vehicle2.set_autopilot(False)
            print("[INFO] Obstacle vehicle 2 spawned")

        #------------------ Obstacle Vehicle 3 ------------------
        obs_bp3 = blueprint_library.find("vehicle.mini.cooper")
        obs_bp3.set_attribute("role_name", "obstacle")

        obs_transform3 = carla.Transform(
            carla.Location(x=-52.4844, y=20.471010, z=0.6),
            carla.Rotation(yaw=180)
        )

        obstacle_vehicle3 = world.try_spawn_actor(obs_bp3, obs_transform3)
        if obstacle_vehicle3 is None:
            print("[WARN] Failed to spawn obstacle vehicle 3 (collision).")
        else:
            obstacle_vehicle3.set_autopilot(False)
            print("[INFO] Obstacle vehicle 3 spawned")

        # Tick once so world state is consistent before sensors attach
        world.tick()

        # ------------------ SensorFusion ------------------
        fusion = SensorFusion(
            world=world,
            ego_vehicle=ego_vehicle,
            min_distance=2.0,
            yolo_model_path="yolov8n.pt"
        )

        fusion.test_fusion(num_vehicles=5)

    finally:
        # Cleanup fusion sensors first
        if fusion is not None:
            fusion.destroy()

        # Destroy spawned vehicles
        for v in [obstacle_vehicle1, obstacle_vehicle2, obstacle_vehicle3, ego_vehicle]:
            if v is not None:
                v.destroy()

        # Restore original world settings
        world.apply_settings(original_settings)

if __name__ == "__main__":
    #main()
    pass 