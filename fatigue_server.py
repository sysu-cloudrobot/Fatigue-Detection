#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import base64
from fatigue_detection.detection import Fatigue_detection

from imutils.video import VideoStream
from imutils import face_utils
import pyglet
import imutils
import time
import dlib
import cv2

from fatigue_detection.ImgWindow import ImgWindow


def callback(data):
    imgdata = data.data
    imgdata = base64.b64decode(imgdata)
    print(type(imgdata))

    upload_image_path = 'upload_img_fatigue.jpg'
    with open(upload_image_path, 'wb') as f:
        f.write(imgdata)
    
    frame = iwin.read(upload_image_path)
    #frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        fd.fatigue_detection(shape)

        iwin.draw(shape, fd.is_fatigue(), fd.mar, fd.ear)
    
    # iwin.close()

    # with open()
    # ret_message = base64.b64encode(iwin.frame)
    ret_image_path = './templates/images/ret_image.jpg'
    cv2.imwrite(ret_image_path, iwin.frame)
    
    # with open(ret_image_path, 'rb') as f:
    #     ret_message = base64.b64encode(f.read())
    global pub
    # pub.publish('static/ret_image.jpg')
    ret_result = str(fd.is_fatigue()) + ',' + str(fd.mar) + ',' + str(fd.ear)
    pub.publish(ret_result)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('fatigue_server', anonymous=True)

    global fd
    fd = Fatigue_detection()
    global iwin
    iwin = ImgWindow()

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    global detector
    detector = dlib.get_frontal_face_detector()
    global predictor
    predictor = dlib.shape_predictor("68 face landmarks.dat")

    rospy.Subscriber('to_processed_image', String, callback)
    global pub
    pub = rospy.Publisher('fatigue', String, queue_size=10) 


    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
