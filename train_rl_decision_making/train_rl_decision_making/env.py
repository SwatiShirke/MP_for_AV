import carla
import random 
import numpy as np
from get_map import Grid_map
from a_star import a_star
from traj import Trajectory
from sensor_fusion import SensorFusion

class Env:
    """
    Class of the environment for training the RL decision making model. The environment should be able to reset and step according to the action taken by the agent.
    This class connects with Carla and provides the necessary functions for the agent to interact with the environment. The environment should also provide the necessary information for the agent to make decisions, such as the current state of the environment and the reward for taking a certain action.
    """
    
    def __init__(self, traffic_manager_port, traffic_size, v_min, v_max, a_min, a_max, lateral_accel, max_obj):
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
        self.yollow_model_path = "/home/swati/Motion_Planning/MP_for_AV/src/MP_for_AV/train_rl_decision_making/train_rl_decision_making/yolo_weights/best.pt"
        self.max_obs_detections = max_obj #max obstacle detcted through yollow

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
        self.setup_traffic_manager(tm_port=self.traffic_manager_port, synchronous=True)
        npc_ids = self.spawn_npc_traffic(num_vehicles=self.traffic_size, tm_port=self.traffic_manager_port)
        
        self.start_point = self.get_random_free_spawn_point()
        self.ref_velocity = self.get_ref_velocity()
        self.ego_vehicle = self.spawn_ego_vehicle(self.start_point)
        self.goal_point = self.get_goal_point(self.start_point)
        if self.is_test_mode:
            print(f"Start point: {self.start_point}, Goal point: {self.goal_point}")

        grid_map_generator = Grid_map(self.world, 1.0, 10.0)
        self.grid_map, self.offset, self.grid_resolution = grid_map_generator.get_grid_map()
        self.a_star_planner = a_star(self.grid_map, self.offset, self.grid_resolution, self.vehicle_width)
        self.path = self.a_star_planner.find_path(self.start_point, self.goal_point)

        self.traj_obj = Trajectory(self.v_min,self.v_max, self.a_min, self.a_min , self.lateral_accel)
        self.traj_obj.create_path_funs(self.path)
        traj_waypoints = self.traj_obj.get_traj_wps((self.start_point[0], self.start_point[1], 0), self.ref_velocity)

        self.sensor_fusion = SensorFusion(self.world, self.ego_vehicle, self.yollow_model_path,self.max_obs_detections)
        self.step_count = 0
        self.sensor_fusion._refresh_vehicle_cache() # cache the initial state of the world for faster access during state computation
        ego_state = self.get_ego_state()
        state = self.sensor_fusion.get_current_state(traj_waypoints, ego_state)
        return state

    def cleanup_vehicles(self):
        """
        Destroy all vehicles currently present in the CARLA world.
        Safe to call during reset().
        """
        actors = self.world.get_actors()
        vehicles = actors.filter('vehicle.*')

        for vehicle in vehicles:
            try:
                vehicle.destroy()
            except RuntimeError as e:
                print(f"[WARN] Failed to destroy vehicle {vehicle.id}: {e}")

        self.vehicle = None    

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

        if len(spawned_ids) < num_vehicles:
            print(f"[WARN] Spawned {len(spawned_ids)}/{num_vehicles} NPC vehicles (spawn limits/collisions).")

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

            print("ego_transform: ", ego_transform)
            hero_vehicle = self.world.spawn_actor(ego_bp, ego_transform)
            hero_vehicle.set_autopilot(False)
            if self.is_test_mode:
                print("[INFO] Ego vehicle spawned")
           
            return hero_vehicle

        except RuntimeError as e:
            print(f"[ERROR] Failed to spawn ego vehicle: {e}")
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
        if self.vehicle is None:
            return None

        tf = self.vehicle.get_transform()
        vel = self.vehicle.get_velocity()

        x = float(tf.location.x)
        y = float(tf.location.y)
        yaw_rad = float(np.deg2rad(tf.rotation.yaw))

        vx_w = float(vel.x)
        vy_w = float(vel.y)

        return (x, y, yaw_rad, vx_w, vy_w)

    def step(self, action):
        self.world.tick()
        self.step_count += 1

        self.fusion.maybe_refresh_cache(self.step_count, refresh_every=20)

        tf = self.ego_vehicle.get_transform()
        ego_loc = (tf.location.x, tf.location.y, np.deg2rad(tf.rotation.yaw))
        state = self.fusion.compute_sensor_state(ego_location=ego_loc)

        ##other logic pending - reward calculation, done condition, etc.

        return state

if __name__ == "__main__":
   env = Env(traffic_manager_port=8000, traffic_size=40, v_min=0.0, v_max=10.0, a_min=-3.0, a_max=3.0, lateral_accel=2.0)
   env.reset()


