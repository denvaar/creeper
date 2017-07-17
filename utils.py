import os
from glob import glob
from subprocess import Popen, PIPE
from datetime import datetime
from threading import Thread

from notifications import send_sms


def delete_files():
    """Remove files matching OUTPUT_FILE_PREFIX"""

    files = glob(os.environ['OUTPUT_FILE_PREFIX'] + '*')
    for f in files:
        os.remove(f)

class VideoWriter(object):
    def __init__(self, *args, **kwargs):
        self.ffmpeg_process = None

    def initialize_ffmpeg(self):
        """Create a process to run ffmpeg"""

        self.video_filename = '{}_{}.mp4'.format(
            os.environ['OUTPUT_FILE_PREFIX'],
            datetime.now().strftime('%Y-%m-%d-%H-%M-%s')
        )
        self.ffmpeg_process = Popen([
            'ffmpeg',
            '-y',
            '-f',
            'image2pipe',
            '-vcodec', 'mjpeg',
            '-r', '24',
            '-i',
            '-',
            '-vcodec', 'mpeg4',
            '-q', '5',
            '-fs', '590000',
            '-r', '24',
            self.video_filename
        ],
        stdin=PIPE,
        stdout=PIPE)

    def start_recording(self, frame):
        """Write image frame to stdin of subprocess"""

        if not self.ffmpeg_process:
            self.initialize_ffmpeg()

        try:
            # write the frame to ffmpeg process' stdin
            self.ffmpeg_process.stdin.write(frame)
            self.ffmpeg_process.stdin.flush()
        except BrokenPipeError:
            self.finish_recording()

    def finish_recording(self):
        """Close subprocess stdin"""

        if self.ffmpeg_process and not self.ffmpeg_process.stdin.closed:
            self.ffmpeg_process.stdin.close()
            self.ffmpeg_process = None
            Thread(target=send_sms, args=(self.video_filename,)).start()
