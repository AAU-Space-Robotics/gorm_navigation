#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

import threading


class GoalSequencer(Node):
    def __init__(self):
        super().__init__('goal_sequencer')

        # Publisher
        self.pub = self.create_publisher(PoseStamped, '/goal_pose', 10)

        # Define list of goal poses
        self.goals = self.create_goals()

        self.current_index = 0

        # Start user input thread
        self.input_thread = threading.Thread(target=self.wait_for_user_input)
        self.input_thread.daemon = True
        self.input_thread.start()

        self.get_logger().info("Goal Sequencer ready. Press ENTER to send next goal.")

    def create_goals(self):
        """Create a list of PoseStamped goals."""
        goals = []

        # Example goals (modify as needed)
        coords = [
            (-1.55, -1.08, 0.0),    #1
            (-5.58, 4.0, 0.0),      #7
            (-4.74, 8.81, 0.0),     #10
            (-4.02, -0.85, 0.0),    #2
            (-1.45, 4.31, 0.0),     #11
            (-4.87, 5.55, 0.0),     #8
            (0.05, 1.6, 0.0),       #4
            (-1.55, -1.08, 0.0),    #1
        ]

        for x, y, yaw in coords:
            pose = PoseStamped()
            pose.header.frame_id = "world"
            pose.pose.position.x = x
            pose.pose.position.y = y

            # Simple yaw → quaternion (z-only rotation)
            import math
            pose.pose.orientation.z = math.sin(yaw / 2.0)
            pose.pose.orientation.w = math.cos(yaw / 2.0)

            goals.append(pose)

        return goals

    def wait_for_user_input(self):
        """Thread function to wait for ENTER key."""
        while rclpy.ok():
            input("Press ENTER to send next goal...")

            if self.current_index < len(self.goals):
                goal = self.goals[self.current_index]

                # Update timestamp
                goal.header.stamp = self.get_clock().now().to_msg()

                self.pub.publish(goal)

                self.get_logger().info(
                    f"Published goal {self.current_index + 1}/{len(self.goals)}"
                )

                self.current_index += 1
            else:
                self.get_logger().info("All goals have been sent.")


def main():
    rclpy.init()
    node = GoalSequencer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
