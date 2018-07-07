#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image 

global subscr
def callback(data): 
    msg = data.data
    print(msg)
    global drive_state
    drive_state = msg
    subscr.unregister()

global fatigue_subscr
def fatigue_callback(data):
    print("fatigue_callback")
    msg = data.data
    print(msg)
    global f_img
    f_img = msg
    fatigue_subscr.unregister()

subscr = rospy.Subscriber('safe_behavior', String, callback)
drive_state = None

fatigue_subscr = rospy.Subscriber('fatigue', String, fatigue_callback)
f_img = None
#subscr = rospy.Subscriber('results', String, callback)
def talker(message):
    pub = rospy.Publisher('to_processed_image', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    if not rospy.is_shutdown():
        pub.publish(message)
        global subscr
        subscr = rospy.Subscriber('safe_behavior', String, callback)
        global fatigue_subscr
        fatigue_subscr = rospy.Subscriber('fatigue', String, fatigue_callback)
        #rospy.spin()



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
