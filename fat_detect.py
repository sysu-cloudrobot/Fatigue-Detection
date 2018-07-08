#!/usr/bin/env python

import rospy
from std_msgs.msg import String

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import pyglet
import argparse
import imutils
import time
import dlib
import cv2
from fatigue_detection.ImgWindow import ImgWindow
from fatigue_detection.detection import Fatigue_detection


if __name__ == '__main__':
    try:
        # construct the argument parse and parse the arguments
        rospy.init_node('talker', anonymous=True)
        rate = rospy.Rate(10) # 10hz

        ap = argparse.ArgumentParser()

        ap.add_argument("-w", "--webcam", type=int, default=0,
            help="index of webcam on system")
        args = vars(ap.parse_args())
        
        fd = Fatigue_detection()
        iwin = ImgWindow(args, True)
        

        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        print("[INFO] loading facial landmark predictor...")
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("68 face landmarks.dat")


        # start the video stream thread
        print("[INFO] starting video stream thread...")
        
        time.sleep(1.0)

        # loop over frames from the video stream
        while True:
            # grab the frame from the threaded video file stream, resize
            # it, and convert it to grayscale
            # channels)
            frame = iwin.read()
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
            
            iwin.show()
                
            if iwin.is_close():
                break

        iwin.close()

        # do a bit of cleanup
        
    except rospy.ROSInterruptException:
        pass