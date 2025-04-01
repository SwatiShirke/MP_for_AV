import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from vd_msgs.srv import PlannerSrv
import carla
from vd_global_planner.a_star import a_star

class GlobalPlanner(Node):
    def __init__(self):
        super().__init__('global_planner')
        #Connect to CARLA
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()
        self.map = self.world.get_map()
        self.graph = {}
        self.get_graph()        
        self.T_pred = 0.02 
        self.start = (0,0)
        self.goal = (100,100,0)
        self.path = None
        self.path_pub = self.create_publisher(Path, "global_path", 10)
        self.srv = self.create_service(PlannerSrv, "global_plan_srv", self.service_callback)
        self.planner = a_star(self.graph, self.map)

    def get_graph(self):
        """generate map from carla"""    
              
        node_list = self.map.get_topology()
        #create undirected graph
        graph = {}
        for node1, node2 in node_list:
            tuple1 = (round(node1.transform.location.x, 2), round(node1.transform.location.y, 2) )
            tuple2 = (round(node2.transform.location.x, 2), round(node2.transform.location.y, 2) )
            distance = node1.transform.location.distance(node2.transform.location)
            graph.setdefault(tuple1, [])
            if tuple2 not in graph[tuple1]:
                graph[tuple1].append((tuple2,distance))           
        
        self.graph = graph
        print("graph**********************")
        print(graph)
            
         

    def service_callback(self, request, response):
        self.get_logger().info('started generating global path')
        self.goal = (request.x, request.y) 
        self.path = self.planner.a_star(self.start, self.goal)
        response.message = "Global Path generated!"
        return response
        
def main(args=None):
    rclpy.init(args=args)
    planner_node = GlobalPlanner()
    rclpy.spin(planner_node)

    planner_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



    



