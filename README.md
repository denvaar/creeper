# creeper
Makeshift Raspberry Pi Security Camera System

This also works with a Macbook camera, and probably anything with a camera device.

More details about this project can be found [here](https://denverpsmith.com/) on my blog.

## Features

- Captures video and detects motion using OpenCV library.
- Streams video to web page via motion JPEG.
- Allows clients to control camera from web page.
- Allows multiple clients to view live stream.
- Encodes and saves video files when motion is detected.
- Sends a text message with video attachment when motion is detected.

## Setup

Install [ffmpeg](https://ffmpeg.org/) and make sure it's in your `PATH`.

Install Python3

Install python dependencies (preferably inside a virtual environment.) Packages can be found in `requirements.txt`:
```
pip install -r requirements.txt
```

Set the following environment variables:
```
export EMAIL=youremail@gmail.com
export EMAIL_PASSWORD=youremailpassword
export SMS_PHONE_NUMBER=1111111111@mms.att.net
# this can be whatever you like:
export OUTPUT_FILE_PREFIX=motion
```

`SMS_PHONE_NUMBER` should use the appropriate SMS gateway address for your carrier.

Start the server:
```bash
python main.py
```

## License

MIT
