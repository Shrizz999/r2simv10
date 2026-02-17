import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class RelayClimber(Node):
    def __init__(self):
        super().__init__('relay_climber')
        self.get_logger().info('--- R2KRISHNA ONLINE: STABLE VISUAL + TOF ALIGN ---')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.cam_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.bridge = CvBridge()

    def image_callback(self, msg):
        # Convert and Show Image
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2.imshow("R2Krishna Visual Feed", frame)
        cv2.waitKey(1) # Necessary to refresh OpenCV window
        
        # Test Movement
        move = Twist()
        move.linear.x = 0.3
        self.cmd_pub.publish(move)

def main(args=None):
    rclpy.init(args=args)
    node = RelayClimber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
