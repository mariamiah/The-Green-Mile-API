import smtplib
import os
class EmailController:
    def send_email(self, data):
        # username = data.split('@')[0]
        gmail_user=os.environ["SENDER_MAIL"]
        gmail_password=os.environ["SENDER_PASSWORD"]
        sent_from = gmail_user
        to = data
        subject = "(GreenMile) Details On your Package"
        body = 'Hey'

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
    
         
                    