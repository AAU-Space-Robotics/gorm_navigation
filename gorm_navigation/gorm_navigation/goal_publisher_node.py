#!/usr/bin/env python3

"""
Simple goal publisher node for testing RL navigation.

This node publishes goal poses for the RL navigation system to follow.
Useful for testing and demonstration purposes.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header
import math


class GoalPublisherNode(Node):
    """Node that publishes goal poses for navigation testing."""
    
    def __init__(self):
        super().__init__('goal_publisher_node')
        
        # Declare parameters
        self.declare_parameter('goal_x', 9.0)
        self.declare_parameter('goal_y', 9.0)
        self.declare_parameter('goal_z', 0.0)
        self.declare_parameter('publish_rate', 1.0)  # Hz
        
        # Get parameters
        self.goal_x = self.get_parameter('goal_x').get_parameter_value().double_value
        self.goal_y = self.get_parameter('goal_y').get_parameter_value().double_value
        self.goal_z = self.get_parameter('goal_z').get_parameter_value().double_value
        self.publish_rate = self.get_parameter('publish_rate').get_parameter_value().double_value
        
        # Create publisher
        self.goal_publisher = self.create_publisher(
            PoseStamped, '/goal_pose', 10)
        
        # Create timer
        timer_period = 1.0 / self.publish_rate
        self.timer = self.create_timer(timer_period, self.publish_goal)
        
        self.get_logger().info(f"Goal publisher started - publishing goal at ({self.goal_x}, {self.goal_y}, {self.goal_z})")
    
    def publish_goal(self):
        """Publish the goal pose."""
        msg = PoseStamped()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'  # or 'odom' depending on your setup
        
        msg.pose.position.x = self.goal_x
        msg.pose.position.y = self.goal_y
        msg.pose.position.z = self.goal_z
        
        # Set orientation (facing forward)
        msg.pose.orientation.w = 1.0
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0
        
        self.goal_publisher.publish(msg)


def main(args=None):
    """Main entry point."""
    rclpy.init(args=args)
    
    try:
        goal_publisher = GoalPublisherNode()
        rclpy.spin(goal_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        if 'goal_publisher' in locals():
            goal_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
