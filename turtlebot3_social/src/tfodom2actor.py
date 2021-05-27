#!/usr/bin/env python
# coding=utf-8
'''
Author:Tai Lei
Date:Thu 09 Feb 2017 04:08:17 PM CST
Info:
    '''

#!/usr/bin/env python  
import tf2_ros
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from gazebo_msgs.msg import ModelStates
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
import numpy as np

class MountTB2Ped(Node):

    def __init__(self):
        super().__init__('tf2defaultworld')
        self.model_sub = self.create_subscription(
            ModelStates,
            "/gazebo/model_states",
            self.callback,
            1)#1?
        self.br = tf2_ros.TransformBroadcaster()
        self.model_set = self.create_publisher(ModelState, "/gazebo/set_model_state", 1)

        self.tb3modelstate = ModelState()
        self.tb3modelstate.model_name="turtlebot3_burger"
        self.actor_name = rclpy.get_param("TB3_WITH_ACTOR")
    def callback(self, data):
        #tb3_idx = data.name.index("turtlebot3_burger")
        actor_idx = data.name.index(self.actor_name)
        #tb3_pose = data.pose[tb3_idx].position
        #tb3_orien = data.pose[tb3_idx].orientation
        #br.sendTransform((tb3_pose.x, tb3_pose.y, tb3_pose.z),
                #(tb3_orien.x, tb3_orien.y, tb3_orien.z, tb3_orien.w),
                #rclpy.Time.now(),
                #"tb3",
                #"default_world")
        actor_pose = data.pose[actor_idx].position
        actor_orien = data.pose[actor_idx].orientation
        actor_pose.z = 0.0
        quat_ = self.quat_trans(actor_orien)
        #x = actor_orien.y
        #z = actor_orien.x
        #y = actor_orien.z
        #actor_orien.y = actor_orien.x
        #actor_orien.x = x
        #actor_orien.y = y
        #actor_orien.z = z

        self.tb3modelstate.pose.position =  actor_pose
        self.tb3modelstate.pose.orientation = quat_
        #self.model_set(self.tb3modelstate)
        self.model_set.publish(self.tb3modelstate)
        self.br.sendTransform((0,0,0),
                (0, 0, 0, 1),
                rclpy.Time.now(),
                "odom",
                self.actor_name)

    def quat_trans(self, quat):
        euler = tf2_ros.transformations.euler_from_quaternion((quat.x,quat.y,quat.z,quat.w))
        quat_ = tf2_ros.transformations.quaternion_from_euler(euler[0]-0.5*np.pi, euler[1], euler[2]-0.5*np.pi)
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

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    tf2defaultworld.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()