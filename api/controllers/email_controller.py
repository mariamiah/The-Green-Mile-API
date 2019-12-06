import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailController:
    def send_email(self, data, userDetails, package_order_number):
        sender_email = os.environ["SENDER_MAIL"]
        receiver_email = data["recipient_email"]
        password = os.environ["SENDER_PASSWORD"]

        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Green Mile Package"
        message["From"] = sender_email
        message["To"] = receiver_email
        username = f'{userDetails[0]["username"]}'
        recipient_password = f'{userDetails[0]["password"]}'
        package = data["package_name"]
        status = data["delivery_status"]
        address = data["recipient_address"]
        package_number = package_order_number
        recipient_name = data["recipient_name"]
        if status == "delivered":
            # Create the plain-text and HTML version of your message
            text = """\
            Dear %s,
            Thank you for shipping with Green Mile !! <br>
            This is to inform you that our delivery agent <br>
            has %s a package called %s with package number %s at address %s
            """ %(username, status, package, package_number, address )
            html = """\
            <html>
            <body>
                <p>Dear <b> %s </b>,<br>
                Thank you for shipping with Green Mile !!
                <br>
                This is to inform you that our delivery agent <br> has <b> %s </b>
                a package called <b> %s </b> with package number <b> %s <b> at address <b> %s </b>
                </p>
            </body>
            </html>
            """ %(recipient_name, status, package, package_number, address)
        elif status == "prepared for shipment":
            text = """\
            Dear <b> %s </b>,
            Thank you for shipping with Green Mile !! <br>
            This is to inform you that your package <b> %s </b> 
            with package_number <b> %s </b>
            <br>
            is being <b> %s </b> at address %s.
            """ %(recipient_name, package, package_number, status, address )
            html = """\
            <html>
            <body>
                <p>Dear <b> %s </b>,<br>
                Thank you for shipping with Green Mile !!
                <br>
                This is to inform you that your package <b> %s </b>
                with package number <b> %s </b> <br> is being %s
                at address <b> %s </b>.
                <p>Click on the button below and enter the package number provided to track this package</p>
                <br />
                <a href="https://the-green-mile-fe.herokuapp.com/track" target="_black">
                <button style="background-color:#2E8B57; color: white; border-radius: 1.5rem; height:40px;width:120px"> Track your package </button>
                </a>
            </body>
            </html>
            """ %(recipient_name, package, package_number, status, address)
        else:
            text = """\
            Dear %s,
            Thank you for shipping with Green Mile !! <br>
            This is to inform you that your package <b> %s </b> with 
            package number <b> %s </b> <br>
            has been %s to address %s.
            """ %(recipient_name, package, package_number,  status, address )
            html = """\
            <html>
            <body>
                <p>Dear <b> %s </b>,<br>
                Thank you for shipping with Green Mile !!
                <br>
                This is to inform you that your package <b> %s </b>
                with package number <b> %s </b>
                 <br> has been <b> %s </b>
                to address <b> %s </b>.
                <p>Click on the button below and enter the package number provided to track this package</p>
                <br />
                <a href="https://the-green-mile-fe.herokuapp.com/track" target="_blank">
                <button style="background-color:#2E8B57; color: white; border-radius: 1.5rem; height:40px;width:120px"> Track your package </button>
                </a>
            </body>
            </html>
            """ %(recipient_name, package, package_number, status, address)



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