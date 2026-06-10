#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# Inițializăm variabilele globale pentru distanțe cu o valoare sigură (ex: 2 metri)
front_dist = 2.0
left_dist = 2.0
right_dist = 2.0

def scan_callback(msg):
    global front_dist, left_dist, right_dist
    
    num_readings = len(msg.ranges)
    
    if num_readings > 0:
        # Presupunem un senzor LIDAR standard de 360 de grade (cum e cel de pe TurtleBot):
        # Indexul 0 -> direct în față (0°)
        # Indexul 90 -> în stânga (90°)
        # Indexul 270 -> în dreapta (270°)
        
        # Citirea pentru FAȚĂ
        front_dist = msg.ranges[0]
        
        # Citirea pentru STÂNGA (verificăm să nu depășească lungimea array-ului)
        if num_readings > 90:
            left_dist = msg.ranges[90]
        else:
            left_dist = msg.ranges[num_readings // 4]
            
        # Citirea pentru DREAPTA
        if num_readings > 270:
            right_dist = msg.ranges[270]
        else:
            right_dist = msg.ranges[(3 * num_readings) // 4]

def move_robot():
    global front_dist, left_dist, right_dist
    
    # Inițializăm nodul ROS
    rospy.init_node('wall_avoidance_quiz', anonymous=True)
    
    # Cerința 1: Create a Publisher that writes into the /cmd_vel topic
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    # Cerința 2: Create a Subscriber that reads from the /scan topic
    rospy.Subscriber('/scan', LaserScan, scan_callback)
    
    rate = rospy.Rate(10) # Frecvența de rulare (10 Hz)
    msg = Twist()

    rospy.loginfo("Nodul de evitare a obstacolelor a pornit conform cerințelor.")

    while not rospy.is_shutdown():
        # Logica din imagine pentru evitarea peretelui (Avoid the wall):
        
        # 1. Dacă citirea laser în FAȚĂ este mai mică de 1 metru -> Turn left
        if front_dist < 1.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.5  # În ROS, o valoare pozitivă înseamnă rotație la stânga
            rospy.loginfo("Obstacol în față (< 1m)! Viraj la stânga.")
            
        # 2. Dacă citirea laser în DREAPTA este mai mică de 1 metru -> Turn left
        elif right_dist < 1.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.5  # Viraj la stânga
            rospy.loginfo("Obstacol în dreapta (< 1m)! Viraj la stânga.")
            
        # 3. Dacă citirea laser în STÂNGA este mai mică de 1 metru -> Turn right
        elif left_dist < 1.0:
            msg.linear.x = 0.0
            msg.angular.z = -0.5 # În ROS, o valoare negativă înseamnă rotație la dreapta
            rospy.loginfo("Obstacol în stânga (< 1m)! Viraj la dreapta.")
            
        # 4. Dacă în față este liber (mai mare de 1 metru) și nu avem alte pericole laterale -> Move forward
        else:
            msg.linear.x = 0.2   # Viteza de înaintare
            msg.angular.z = 0.0
            rospy.loginfo("Drum liber în față. Robotul merge înainte.")

        # Publicăm mesajul de mișcare către robot
        pub.publish(msg)
        
        rate.sleep()

if __name__ == '__main__':
    try:
        move_robot()
    except rospy.ROSInterruptException:
        pass
