import cv2
import imutils
import time
from datetime import datetime, timedelta


class VideoCamera(object):
    def __init__(self):
        # capture from device 0
        self.video = cv2.VideoCapture(0)
        self.initial_frame = None
        time.sleep(1)
        self.last_movement = datetime.now()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        status_text = 'No movement right now'

        if not success:
            return b''
        
        frame = imutils.resize(image, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.initial_frame is None:
            self.initial_frame = gray
        
        if datetime.now() > self.last_movement + timedelta(minutes=1):
            print('new initial frame issued')
            self.initial_frame = gray
            self.last_movement = datetime.now()

        frame_delta = cv2.absdiff(self.initial_frame, gray)
        threshold = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        dilated_threshold = cv2.dilate(threshold, None, iterations=2)
        (_, contours, _) = cv2.findContours(dilated_threshold.copy(),
                                         cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) >= 500:
                self.last_movement = datetime.now()
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                status_text = 'Something is moving...'

        # encode raw images to motion JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
