#!/usr/bin/env python
from multiprocessing.connection import Listener
import rospy
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist

global distances 
arret = False
distanceMoy = 100
distance45Degres = 100
distances = []
global i 
i = 0

def listener(data):
    global distances
    distances = data.data

def send_cmd_vel():
    global distances
    
    pub = rospy.Publisher('/cmd_vel',Twist, queue_size=10)
    rospy.Subscriber("/cloud_a",Float32MultiArray,listener)
    rospy.init_node("Test",anonymous=True)
    rate = rospy.Rate(100)
    
    while not rospy.is_shutdown():
        move_cmd = Twist()
        if distances:
            distanceMoy = distances[0]
            distance45Degres = distances[3]
        else:
            distanceMoy = 0
            distance45Degres = 0
        if distanceMoy > 45.0:
            if distance45Degres > 25 and distance45Degres < 40:
                move_cmd.linear.x = 0.05
                move_cmd.angular.z = 0.5
                print ("Tourner gauche")
            elif distance45Degres < 20:
                move_cmd.linear.x = 0.05
                move_cmd.angular.z = -0.5
                print ("Tourner droite")
            elif distance45Degres >=20 and distance45Degres <= 25:
                move_cmd.linear.x = 0.08
                move_cmd.angular.z = 0
                print ("Avance")
            else:
                move_cmd.linear.x = 0.05
                move_cmd.angular.z = 0
                pub.publish(move_cmd)
                rate.sleep()
                move_cmd.linear.x = 0.1
                move_cmd.angular.z = 0.75
                print ("Tourner gauche car pas mur")
        else :
            #move_cmd.linear.x = -0.2
            #move_cmd.angular.z = 0
            #pub.publish(move_cmd)
            #rate.sleep()
            
            # if distances[i + 1] > distances[i]
            move_cmd.linear.x = -0
            move_cmd.angular.z = -0.5
            
            print ("mur en face")
                
            
            
        pub.publish(move_cmd)
        rate.sleep()

if __name__ == '__main__':
    try:
        i = 0
        send_cmd_vel()
    except rospy.ROSInterruptException:
        pass