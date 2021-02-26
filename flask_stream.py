from flask import Flask, render_template, Response
import opencv2
import time
import cv2
import os

videostream = opencv2.VideoStream(resolution=(1280,720),framerate=30).start()
time.sleep(1)

app = Flask(__name__,template_folder=os.getcwd())

@app.route('/')
def index():
    return render_template('index.html')

def gen(opencv2):
    while True:
        if cv2.waitKey(1) == ord('q'):
            break
        
        frame1=opencv2.cvprocess()
        ret,buffer = cv2.imencode('.jpg',frame1)
        frame1 = buffer.tobytes()

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' +frame1+b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(opencv2.VideoStream),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run(host='0.0.0.0',port='5000', debug=False)

cv2.destroyAllWindows()
videostream.stop()


        

