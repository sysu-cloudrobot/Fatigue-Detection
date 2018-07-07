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

from .ImgWindow import ImgWindow

class Fatigue_detection:
    MOUTH_AR_THRESH = 0.2
    MOUTH_AR_CONSEC_FRAMES = 48

    EYE_AR_THRESH = 0.2
    EYE_AR_CONSEC_FRAMES = 48

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mStart, mEnd) = (60, 68)

    def __init__(self):
        self.eye_counter = 0
        self.mouth_counter = 0
        self.alarm_on = False
        self.ear = 0.0
        self.mar = 0.0


    def sound_alarm(self, path):
    # play an alarm sound
        music = pyglet.resource.media('alarm.wav')
        music.play()
        pyglet.app.run()

    def mouth_aspect_ratio(self, mouth):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(mouth[1], mouth[7])
        B = dist.euclidean(mouth[2], mouth[6])
        C = dist.euclidean(mouth[3], mouth[5])

        # compute the euclidean distance between the horizon
        # eye landmark (x, y)-coordinates
        D = dist.euclidean(mouth[0], mouth[4])

        # compute the eye aspect ratio
        mar = (A + B + C) / (3 * D)

        # return the eye aspect ratio
        return mar

    def eye_aspect_ratio(self, eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizon
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear

    def mouth_fatigue_detection(self, shape):
        mouth = shape[Fatigue_detection.mStart:Fatigue_detection.mEnd]
        self.mar = self.mouth_aspect_ratio(mouth)

        if self.mar > Fatigue_detection.MOUTH_AR_THRESH:
            return True
        else:
            return False

    def eye_fatigue_detection(self, shape):
        leftEye = shape[Fatigue_detection.lStart:Fatigue_detection.lEnd]
        rightEye = shape[Fatigue_detection.rStart:Fatigue_detection.rEnd]
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        self.ear = (leftEAR + rightEAR) / 2.0

        # check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        if self.ear < Fatigue_detection.EYE_AR_THRESH:
            return True
        else:
            return False

    def fatigue_detection(self, shape):
        if self.eye_fatigue_detection(shape):
            self.eye_counter += 1
        else:
            self.eye_counter = 0
            self.alarm_on = False
        
        if self.mouth_fatigue_detection(shape):
            self.mouth_counter += 1
        else:
            self.mouth_counter = 0
            self.alarm_on = False

        if self.eye_counter > Fatigue_detection.EYE_AR_CONSEC_FRAMES or self.mouth_counter > Fatigue_detection.MOUTH_AR_CONSEC_FRAMES:
            self.alarm_on = True
    
    def is_fatigue(self):
        return self.alarm_on

