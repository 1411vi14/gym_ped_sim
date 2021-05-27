#!/usr/bin/env python
# coding=utf-8
'''
Author:Tai Lei
Date:Thu 09 Feb 2017 04:08:17 PM CST
Info:
    '''

#!/usr/bin/env python  
import rclpy
import tf2_ros
import numpy as np

def main(args=None):
    rclpy.init(args=args)

    node = rclpy.create_node('tfodom2defaultworld')

    node.get_logger().info('Created node')

    br = tf2_ros.TransformBroadcaster()
    rate = rclpy.Rate(100)
    while rclpy.ok():
        br.sendTransform((0, 0, 0.0),
                (0.0, 0.0, 0.0, 1.0),
                rclpy.Time.now(),
                "odom",
                "default_world")
        rate.sleep()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    