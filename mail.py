import os
import smtplib
import ssl

from email.mime.text import MIMEText
import os


class Mail:

    def __init__(self):
        print("Initialized mail")

    def send(self, receiver, subject, body):
        sender = os.getenv('user_email')
        # example - smtp.gmail.com
        mail_server = os.getenv('mail_server')
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        port = 465

        # https://support.google.com/a/answer/6180220?hl=en
        context = ssl.create_default_context()
        context.load_verify_locations(os.getenv('ssl_cert'))

        with smtplib.SMTP_SSL(mail_server, port, context=context) as server:
            server.login(sender, os.getenv('user_password'))
            server.sendmail(sender, [receiver], msg.as_string())
            server.quit()
