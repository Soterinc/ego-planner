#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import PointCloud2

class PointCloudRepublisher:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('point_cloud_republisher', anonymous=True)

        # Create a subscriber for the point cloud
        self.subscriber = rospy.Subscriber('/octomap_point_cloud_centers', PointCloud2, self.callback)

        # Create a publisher for the republished point cloud
        self.publisher = rospy.Publisher('/map_generator/global_cloud', PointCloud2, queue_size=10)

        # Set the publishing rate (1 Hz)
        self.rate = rospy.Rate(1)  # 1 Hz

        # Store the latest point cloud
        self.latest_point_cloud = None

    def callback(self, msg):
        # Update the latest point cloud with the received data
        self.latest_point_cloud = msg
        # self.latest_point_cloud.header.frame_id = 'world'
        # self.latest_point_cloud.header.stamp = rospy.Time.now()

    def start(self):
        # Keep republishing the point cloud at 1 Hz
        while not rospy.is_shutdown():
            if self.latest_point_cloud:
                # Publish the latest point cloud
                self.latest_point_cloud.header.frame_id = 'world'
                self.latest_point_cloud.header.stamp = rospy.Time.now()
                self.publisher.publish(self.latest_point_cloud)
                print(rospy.Time.now())
            self.rate.sleep()

if __name__ == '__main__':
    try:
        # Create an instance of the republisher and start it
        republisher = PointCloudRepublisher()
        republisher.start()
    except rospy.ROSInterruptException:
        pass
