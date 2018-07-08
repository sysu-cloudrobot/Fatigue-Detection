import numpy as np
import cv2
from imutils.video import VideoStream
from imutils import face_utils
import imutils

class ImgWindow:

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mStart, mEnd) = (60, 68)

    def __init__(self, args=None, in_local=False):
        if in_local:
            self.vs = VideoStream(src=args["webcam"]).start()
        self.in_local = in_local
        self.frame = None
        
    
    def read(self, file_path=''):
        if self.in_local:
            self.frame = self.vs.read()
            self.frame = imutils.resize(self.frame, width=450)
        else:
            self.frame = cv2.imread(file_path)

        return self.frame

    def draw(self, shape, flag, mar, ear):
        mouth = shape[ImgWindow.mStart:ImgWindow.mEnd]
        leftEye = shape[ImgWindow.lStart:ImgWindow.lEnd]
        rightEye = shape[ImgWindow.rStart:ImgWindow.rEnd]

        mouthHull = cv2.convexHull(mouth)
        cv2.drawContours(self.frame, [mouthHull], -1, (0, 255, 0), 1)

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(self.frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(self.frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if flag:
            cv2.putText(self.frame, "DROWSINESS ALERT!", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(self.frame, "MAR: {:.2f}".format(mar), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(self.frame, "EAR: {:.2f}".format(ear), (300, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
    def show(self):
        cv2.imshow("Frame", self.frame)
        self.key = cv2.waitKey(1) & 0xFF
    
    def is_close(self):
        return self.key == ord("q")

    def close(self):
        cv2.destroyAllWindows()
        # self.vs.stop()

