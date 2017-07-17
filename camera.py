import cv2
import imutils
import multiprocessing
import time

from datetime import datetime, timedelta

from utils import VideoWriter


class VideoCamera(object):
    """Capture and process frame by frame data from camera device 0"""

    def __init__(self):
        # capture from device 0
        self.video = None
        self.recording = False
        self.file_output = None
        self.movement_detected = False
        self.video_writer = None

    def initialize(self):
        """Set up initial variables for camera"""
        # capture from device 0
        self.video = cv2.VideoCapture(0)
        self.initial_frame = None
        time.sleep(1)
        self.last_movement = datetime.now()
        self.video_writer = VideoWriter()

    def release(self):
        """Try to release camera handle"""

        try:
            self.recording.release()
        except AttributeError:
            pass

    def __del__(self):
        self.release()

    def record(self, status):
        """Manually set recording status"""

        self.recording = status

    def encode_jpeg(self, frame):
        """Encode raw image data to JPEG"""
        return cv2.imencode('.jpg', frame)[1]

    def get_frame(self):
        """Process single frame of data from camera device"""

        self.movement_detected = False
        current_time = datetime.now()

        _, image = self.video.read()

        frame = imutils.resize(image, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.initial_frame is None:
            self.initial_frame = gray

        # make a new initial frame every minute if no motion has been detected.
        # (this is a way to combat subtle changes that can happen over time)
        if current_time > self.last_movement + timedelta(minutes=1):
            print('{} new initial frame issued'.format(datetime.now()))
            self.initial_frame = gray
            self.last_movement = datetime.now()

        frame_delta = cv2.absdiff(self.initial_frame, gray)
        threshold = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        dilated_threshold = cv2.dilate(threshold, None, iterations=2)
        (_, contours, _) = cv2.findContours(dilated_threshold.copy(),
                                         cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            contour_area = cv2.contourArea(contour)

            if contour_area >= 500:
                self.last_movement = current_time
                self.movement_detected = True

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

        jpeg = None

        if self.movement_detected or self.recording:
            cv2.putText(frame,
                "Recording {}".format(
                    current_time.strftime('%Y/%m/%d %H:%M:%S')),
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                1
            )
            jpeg = self.encode_jpeg(frame)
            self.video_writer.start_recording(jpeg.tostring())

        else:
            self.video_writer.finish_recording()
            jpeg = self.encode_jpeg(frame)

        return jpeg.tobytes()
