import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


class ArmController(Node):

    def __init__(self):
        super().__init__('arm_controller')
        self.joints = ['base_to_turret', 'turret_to_upper_arm', 'upper_arm_to_forearm']
        self.poses = [
            [0.0, 0.0, 0.0],
            [1.57, 0.6, 1.2],
            [1.57, -0.4, 1.8],
            [-1.57, -0.6, -1.2],
            [0.0, 0.9, -1.5],
        ]
        self.pos = [0.0, 0.0, 0.0]
        self.goal = self.poses[0]
        self.i = 0
        self.wait = 0
        self.auto = True
        self.speed = 0.8
        self.dt = 0.02

        self.pub = self.create_publisher(JointState, 'joint_states', 10)
        self.sub = self.create_subscription(
            Float64MultiArray, 'target_position', self.goal_callback, 10)
        self.timer = self.create_timer(self.dt, self.timer_callback)

    def goal_callback(self, msg):
        if len(msg.data) != 3:
            self.get_logger().warn('need 3 joint values')
            return
        self.goal = list(msg.data)
        self.auto = False
        self.get_logger().info(f'new goal: {self.goal}')

    def timer_callback(self):
        diff = [g - p for g, p in zip(self.goal, self.pos)]
        max_diff = max(abs(d) for d in diff)
        step = self.speed * self.dt

        if max_diff > step:
            self.pos = [p + d * step / max_diff for p, d in zip(self.pos, diff)]
        else:
            self.pos = list(self.goal)
            if self.auto:
                self.wait += 1
                if self.wait > 50:
                    self.wait = 0
                    self.i = (self.i + 1) % len(self.poses)
                    self.goal = self.poses[self.i]
                    self.get_logger().info(f'pose {self.i}: {self.goal}')

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joints
        msg.position = self.pos
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ArmController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
