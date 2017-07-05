import os
import smtplib

from glob import glob

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def gather_latest_images(pattern):
    """Return images from working directory matching given pattern"""
    return glob(pattern)

def send_sms():
    """Send text message using AT&T SMS gateway address"""

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()

    email = os.environ['EMAIL']
    password = os.environ['EMAIL_PASSWORD']
    sms_number = os.environ['SMS_PHONE_NUMBER']

    server.login(email, password)

    message = MIMEMultipart()
    message.attach(MIMEText('Motion detected!', 'plain'))

    pattern = 'snapshot-*'

    for filename in gather_latest_images(pattern):
        f = open(filename, 'rb')
        message_image = MIMEImage(f.read())
        f.close()
        message.attach(message_image)

    server.sendmail(email, sms_number, message.as_string())
    server.quit()

send_sms()
