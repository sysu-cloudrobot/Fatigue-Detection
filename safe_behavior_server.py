#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import base64
from distracted_driver_detection.detect import detect
from distracted_driver_detection.detect import load_model


def callback(data):
    imgdata = data.data
    print(type(imgdata))
    imgdata = base64.b64decode(imgdata)
    

    upload_image_path = 'upload_img.jpg'
    with open(upload_image_path, 'wb') as f:
        f.write(imgdata)
    
    state = detect(upload_image_path)
    print(state)
    # res = facereco(upload_image_path)

    ret_message = state
    pub = rospy.Publisher('safe_behavior', String, queue_size=10) 
    pub.publish(ret_message)


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('safe_behavior_server', anonymous=True)

    rospy.Subscriber('to_processed_image', String, callback)

    # path_to_model = './models/inception_v3-07-acc-0.9934-loss-0.2515.hdf5'
    # global model
    # model = load_model(path_to_model=path_to_model, model_type='inception_v3', img_width=299)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
