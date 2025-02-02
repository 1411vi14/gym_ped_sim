#!/usr/bin/env python3
# coding=utf-8
'''
Author:Tai Lei
Date:Thu 09 Feb 2017 04:08:17 PM CST
Info:
    '''

#!/usr/bin/env python
import rclpy
import tf2_ros
from rclpy.node import Node
import numpy as np
from gazebo_msgs.msg import ModelStates


class MountTB2Ped(Node):

    def __init__(self):
        super().__init__('tf2defaultworld')
        self.br = tf2_ros.TransformBroadcaster(self)
        self.actor_name = self.declare_parameter("TB3_WITH_ACTOR").value
        self.actor_number = self.declare_parameter("ACTOR_NUMBER").value
        self.robot_pose = None
        self.robot_quat = None
        self.model_sub = self.create_subscription(
            ModelStates,
            "/gazebo/model_states",
            self.callback,
            1)

    def callback(self, data):
        for item in range(self.actor_number):
            actor_idx_ = data.name.index(self.actor_name[:-1]+str(item))
            actor_pose_ = data.pose[actor_idx_].position
            actor_quat_ = self.quat_trans(data.pose[actor_idx_].orientation)
            self.br.sendTransform((actor_pose_.x, actor_pose_.y, 0),
                                  (actor_quat_.x, actor_quat_.y,
                                   actor_quat_.z, actor_quat_.w),
                                  rclpy.Time.now(),
                                  self.actor_name[:-1]+str(item),
                                  "default_world")
            print(self.actor_name[:-1])+str(item)
            # if item == str(self.actor_name[-1]):
            #self.robot_pose = actor_pose_
            #self.robot_quat = actor_quat_

        #actor_idx = data.name.index(self.actor_name)
        #actor_pose = data.pose[actor_idx].position
        #actor_orien = data.pose[actor_idx].orientation
        #actor_pose.z = 0.0
        #quat_ = self.quat_trans(actor_orien)
        #x = actor_orien.y
        #z = actor_orien.x
        #y = actor_orien.z
        #actor_orien.y = actor_orien.x
        #actor_orien.x = x
        #actor_orien.y = y
        #actor_orien.z = z

        #self.tb3modelstate.pose.position = self.robot_pose
        #self.tb3modelstate.pose.orientation = self.robot_quat
        # self.model_set(self.tb3modelstate)
        # self.model_set.publish(self.tb3modelstate)
        # self.br.sendTransform((0,0,0),
            #(0, 0, 0, 1),
            # rclpy.Time.now(),
            # "odom",
            # self.actor_name)

    def quat_trans(self, quat):
        euler = tf2_ros.transformations.euler_from_quaternion(
            (quat.x, quat.y, quat.z, quat.w))
        quat_ = tf2_ros.transformations.quaternion_from_euler(
            euler[0]-0.5*np.pi, euler[1], euler[2]-0.5*np.pi)
        quat.x = quat_[0]
        quat.y = quat_[1]
        quat.z = quat_[2]
        quat.w = quat_[3]
        return quat


def main(args=None):
    rclpy.init(args=args)
    tf2defaultworld = MountTB2Ped()

    tf2defaultworld.get_logger().info('Created node')

    rclpy.spin(tf2defaultworld)
    #target_x = -0.5
    #target_y = -5

    #br = tf2_ros.TransformBroadcaster()
    #rate = rclpy.Rate(100)
    # while not rclpy.is_shutdown():
    #target_x = rclpy.get_param("TARGET_X")
    #target_y = rclpy.get_param("TARGET_Y")
    # br.sendTransform((target_x, target_y, 0.0),
    #(0.0, 0.0, 0.0, 1.0),
    # rclpy.Time.now(),
    # "target_pose",
    # "default_world")
    # rate.sleep()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    tf2defaultworld.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
