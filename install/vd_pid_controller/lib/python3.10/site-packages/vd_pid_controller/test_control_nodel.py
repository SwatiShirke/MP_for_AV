import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from vd_msgs.msg import VDControlCMD


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.cmd_publisher_ = self.create_publisher(VDControlCMD, 'vd_control_cmd', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        

    def timer_callback(self):
        msg = VDControlCMD()
        msg.velocity = 30
        msg.steering_angle = 0.01
        self.cmd_publisher(msg)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()