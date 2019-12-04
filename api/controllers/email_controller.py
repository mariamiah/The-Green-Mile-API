import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class EmailController:
    def send_email(self, data, userDetails):
        sender_email = os.environ["SENDER_MAIL"]
        receiver_email = data
        password = os.environ["SENDER_PASSWORD"]

        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Package Details"
        message["From"] = sender_email
        message["To"] = receiver_email
        username = f'{userDetails[0]["username"]}'
        recipient_password = f'{userDetails[0]["password"]}'
        
        # Create the plain-text and HTML version of your message
        text = """\
        Hello %s,
        Please Login to:
        https://he with details
        username: %s,
        password: %s """ %(username, username, recipient_password)
        html = """\
        <html>
        <body>
            <p>Hello %s,<br>
            Please Login to <a href="https://heroku"> GreenMile </a> to track your package <br>
            <br>
            username: %s <br>
            password: %s
            </p>
        </body>
        </html>
        """ %(username, username, recipient_password)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )