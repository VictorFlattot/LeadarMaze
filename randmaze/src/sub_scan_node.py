#!/usr/bin/env python

from std_msgs.msg import Float32MultiArray
import sensor_msgs.point_cloud2 as pc2
import rospy
from sensor_msgs.msg import PointCloud2, LaserScan
import laser_geometry.laser_geometry as lg
import math
from numpy import mean

rospy.init_node("laserscan_to_pointcloud")

lp = lg.LaserProjection()
rate = rospy.Rate(100)
pub_ca = rospy.Publisher('/cloud_a',Float32MultiArray, queue_size=1)


def calcul_distance(x,y):
    return math.sqrt((x**2 + y**2))*100

def scan_cb(msg):
    # convert the message of type LaserScan to a PointCloud2
    pc2_msg = lp.projectLaser(msg)

    point_generator = pc2.read_points(pc2_msg)

    Distance = [[],[],[],[],[]]
    dataD=[]
    # nbPointc = 0
    
    for point in point_generator:
        i = 5
        a = point[4]
        if (a >= 0 and a <=15) or (a >= 345 and a <= 360): i=0
        if (a >= 15 and a <=35): i=1
        if (a >= 35 and a <=55): i=2
        if (a >= 55 and a <=75): i=3
        if (a >= 75 and a <=95): i=4
        
        if i!=5:
            Distance[i].append(calcul_distance(point[0],point[1]))
    for i in range(0,5): 
        if Distance[i] :
            dataD.append(mean(Distance[i]))
    
    arg = Float32MultiArray(data=dataD)
    pub_ca.publish(arg)       


rospy.Subscriber("/scan", LaserScan, scan_cb, queue_size=1)

rospy.spin()