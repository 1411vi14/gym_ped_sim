#!/usr/bin/env python3
# coding=utf-8
'''
Author:Tai Lei
Date:Thu 09 Feb 2017 04:08:17 PM CST
Info:
    '''

import rclpy
import tf2_ros
import numpy as np
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Quaternion


def main(args=None):
    rclpy.init(args=args)

    node = rclpy.create_node('tfodom2defaultworld')

    node.get_logger().info('Created node')

    br = tf2_ros.TransformBroadcaster(node)
    #rate = rclpy.Rate(100)
    rate = node.create_rate(100, node.get_clock())
    while rclpy.ok():
        pose_tf = TransformStamped()
        pose_tf.header.stamp = node.get_clock().now().to_msg()
        pose_tf.header.frame_id = "default_world"
        pose_tf.child_frame_id = "odom"
        pose_tf.transform.translation.x = 0.0
        pose_tf.transform.translation.y = 0.0
        pose_tf.transform.translation.z = 0.0
        pose_tf.transform.rotation.x = 0.0
        pose_tf.transform.rotation.y = 0.0
        pose_tf.transform.rotation.z = 0.0
        pose_tf.transform.rotation.z = 1.0
        br.sendTransform(pose_tf)
        rate.sleep()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
