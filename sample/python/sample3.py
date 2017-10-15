import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate
from platform import python_version
import argparse

MAIL_FROM = 'example@gmail.com'
PASSWORD = 'exapmle'


def create_message(to_addr, subject):
    body = "test"
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg


def send_via_gmail(to_addr, msg):
    print "send via SSL..."
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(MAIL_FROM, PASSWORD)
    s.sendmail(MAIL_FROM, [to_addr], msg.as_string())
    s.close()
    print 'mail sent!'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send Gmail.')
    parser.add_argument('-t', '--to', dest='to_addr', type=str,
                        default='',
                        help='To address')
    parser.add_argument('-s', '--subject', dest='subject', type=str,
                        default='', 
                        help='Subject')
    args = parser.parse_args()

    to_addr = args.to_addr
    title = args.subject

    msg = create_message(to_addr, title)
    send_via_gmail(to_addr, msg)
