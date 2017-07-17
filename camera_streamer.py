from threading import Thread


class CameraStream(object):
    """Stream image frames from a camera source"""
    thread = None
    stream = None
    video_camera = None

    def __init__(self, camera_source, *args, **kwargs):
        if self.thread is None:
            CameraStream.video_camera = camera_source
            CameraStream.thread = Thread(target=self.generate)
            CameraStream.thread.start()

    def request_stream(self):
        """Return current frame from stream"""

        return self.stream

    @classmethod
    def generate(cls):
        """Generate next frame from camera source continuously"""

        while True:
            cls.stream = cls.video_camera.get_frame()
        cls.video_camera = None
        cls.stream = None
        cls.thread = None
