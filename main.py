from flask import Flask, render_template, Response
from queue import Queue
from threading import Thread
from camera import VideoCamera


app = Flask(__name__)

video_camera = VideoCamera()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/record', methods=['GET'])
def record():
    video_camera.record(True)
    return Response('recording', status=200, mimetype='application/json')

@app.route('/api/v1/stop_recording', methods=['GET'])
def stop_recording():
    video_camera.record(False)
    return Response('not recording', status=200, mimetype='application/json')

def gen(camera):
    while True:
        frame = camera.get_frame()
        response_data = (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame +
            b'\r\n\r\n'
        )
        yield response_data

@app.route('/video_feed')
def video_feed():
    # video_camera.release()
    video_camera.initialize()
    return Response(gen(video_camera) or None,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', debug=True)
