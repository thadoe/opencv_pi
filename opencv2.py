import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util
from multiprocessing import Process


class VideoStream:
    
    def __init__ (self, resolution=(640,480),framerate=30):
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
        (self.noerror, self.frame) = self.stream.read()
        self.stopped = False
        
    def start(self):
        self.streamThread= Thread(target=self.update,args=()).start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                self.stream.release()
                return
            (self.noerror, self.frame) = self.stream.read()
        
    def read(self):
        return self.frame
    
    def stop(self):
        self.stopped = True

#(grabbed, frame) = stream.read()

#print (f' read() frame size is {frame.shape}')
#print (f' error status read() from picam is {grabbed}')

#frame1 = frame.copy()
#frame_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
#frame_resized = cv2.resize(frame_rgb, (30, 30))
#input_data = np.expand_dims(frame_resized, axis=0)
#print (f' input_data frame size is {input_data.shape}')

frame_rate_calc = 1
freq = cv2.getTickFrequency()

def get():
    while True:
        if cv2.waitKey(1) == ord('q'):
            break
        
        t1 = cv2.getTickCount()

        global frame_rate_calc
        global freq
    
        frame = videostream.read()
    
        cv2.putText(frame,f'FPS: {frame_rate_calc}',(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
        
        ret,buffer = cv2.imencode('.jpg', frame)

        frame1 = buffer.tobytes() 
        
        t2  = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc= round(1/time1,0)

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame1 +b'\r\n') 
    
    #return frame

        

#*****DEBUG*****
# videostream = VideoStream(resolution=(1280,720),framerate=30).start()
# time.sleep(1)
# 
# while True:
#     
#         frame1=cvprocess()
# 
#         if cv2.waitKey(1) == ord('q'):
#             break
#         
#         cv2.imshow('PIcamera',frame1)
#         
# cv2.destroyAllWindows()
# videostream.stop()

from flask import Flask, render_template, Response

    
videostream = VideoStream(resolution=(1280,720),framerate=30).start()
time.sleep(1)

app = Flask(__name__,template_folder=os.getcwd())

@app.route('/')
def index():
    return render_template('index.html')

#def gen():
 #   while True:
  #      if cv2.waitKey(1) == ord('q'):
   #         break
    #    frame1=cvprocess()
     #   ret,buffer = cv2.imencode('.jpg',frame1)
      #  frame1 = buffer.tobytes()

       # yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' +frame1+b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(get(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run(host='0.0.0.0',port='5000', debug=False)

cv2.destroyAllWindows()
videostream.stop()
print ('\nResources are freed\n')
