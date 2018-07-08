#!/usr/bin/env python3
from flask import Flask
import time
from flask import render_template
from flask import request
import base64
from PIL import Image
from io import StringIO, BytesIO
import robo_talker
import cv2
import numpy as np
from sensor_msgs.msg import Image

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def webcam():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        image_b64 = request.form['img']
        print(type(image_b64))
        robo_talker.talker(image_b64)

        # 等待返回结果
        time.sleep(1)

        result = ''
        is_fatigue = ''
        mar = ''
        ear = ''

        if robo_talker.f_img != None:
            fat_result_path = robo_talker.f_img
            is_fatigue, mar, ear = fat_result_path.split(',')
            robo_talker.f_img = None

        if robo_talker.drive_state != None:
            result = robo_talker.drive_state
            robo_talker.drive_state = None
        

        return 'state: {0}, is_fatigue: {1}, mar: {2}, ear: {3}'.format(result, is_fatigue, mar, ear)
    # return render_template('tmp.html', state="result", img_path='static/ret_image.jpg')

# @app.route('/upload', methods=['POST','GET'])
# def upload():
#     print('getting data from web.')
#     if request.method == 'POST':

#         image_b64 = request.form['img']
#         print(type(image_b64))
#         robo_talker.talker(image_b64)

#         # 等待返回结果
#         time.sleep(3)
        
        
#         if robo_talker.f_img != None:
#             fat_result_path = robo_talker.f_img
#             robo_talker.f_img = None

#         if robo_talker.drive_state != None:
#             result = robo_talker.drive_state
#             robo_talker.drive_state = None 
        
#         return render_template('tmp.html', state=result, img_path=fat_result_path)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7779) #, ssl_context='adhoc'
