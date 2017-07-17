from flask import Flask, render_template, Response
from gevent.pywsgi import WSGIServer
from threading import Thread

from camera import VideoCamera
from camera_streamer import CameraStream
from utils import delete_files


app = Flask(__name__)
app.debug = False
app.threaded = False

def security_system_app():
    video_camera = None
    streamer = None

    def reset_camera(video_camera, streamer):
        delete_files()
        if video_camera:
            video_camera.release()
        video_camera = VideoCamera()
        video_camera.initialize()
        streamer = CameraStream(camera_source=video_camera)
        return (video_camera, streamer,)

    video_camera, streamer = reset_camera(video_camera, streamer)

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

    @app.route('/api/v1/reset', methods=['GET'])
    def reset():
        reset_camera(video_camera, streamer)
        return Response('reset', status=200, mimetype='application/json')

    def gen(stream_handle):
        while True:
            response = (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                stream_handle.request_stream() +
                b'\r\n\r\n'
            )
            yield response

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(streamer) or None,
                        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    """Start a server that can handle async streaming"""
    security_system_app()
    server = WSGIServer(('192.168.1.184', 5000), app)
    server.serve_forever()
