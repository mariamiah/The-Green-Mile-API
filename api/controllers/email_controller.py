import smtplib
import os


class EmailController:
    def send_email(self, data, userDetails):
        # username = data.split('@')[0]
        gmail_user = os.environ["SENDER_MAIL"]
        gmail_password = os.environ["SENDER_PASSWORD"]
        sent_from = gmail_user
        to = data
        subject = "(GreenMile) Details On your Package"
        body = f'Hello {userDetails[0]["username"]}\n Please Login to http://localhost:8080/ with Details\n username: {userDetails[0]["username"]} \n password: {userDetails[0]["password"]}'

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
        print(userDetails, 'userDetails')
