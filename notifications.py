import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_sms(attachment_file):
    """Send text message using SMS gateway address"""

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()

    email = os.environ['EMAIL']
    password = os.environ['EMAIL_PASSWORD']
    sms_number = os.environ['SMS_PHONE_NUMBER']

    server.login(email, password)

    message = MIMEMultipart()
    message.attach(MIMEText('Motion detected!', 'plain'))

    f = open(attachment_file, 'rb')
    message.attach(MIMEApplication(f.read()))
    f.close()

    server.sendmail(email, sms_number, message.as_string())
    server.quit()
