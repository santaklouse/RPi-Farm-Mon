import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
import argparse
import datetime
import sys
sys.path.append('/home/pi/RPi-Farm-Mon/lib')
import sht31
import tsl2561

MAIL_FROM = 'example@gmail.com'
PASSWORD = 'example'
SUBJECT = 'Status'
DEVICE = '/dev/video0'

# SHT31
SHT31_ADDRESS = 0x45
SHT31_CHANNEL = 1

# TSL2561
TSL2561_ADDRESS = 0x39
TSL2561_CHANNEL = 1


def create_message(mail_to, subject, device):
    now = datetime.datetime.now()
    body = "Date: %s \n" % now.strftime("%Y-%m-%d %H:%M:%S")
    sht31_result = sht31.SHT31(SHT31_ADDRESS, SHT31_CHANNEL).read()
    tsl2561_result = tsl2561.TSL2561(TSL2561_ADDRESS, TSL2561_CHANNEL).read()
    body += "Temperature(C): %s \n" % round(sht31_result[0], 2)
    body += "Humidity(%%): %s \n" % round(sht31_result[1], 2)
    body += "Luminosity(lx): %s \n" % round(tsl2561_result[0], 1)
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['To'] = mail_to
    return msg


def send_via_gmail(mail_to, msg):
    print "send via SSL..."
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(MAIL_FROM, PASSWORD)
    s.sendmail(MAIL_FROM, [mail_to], msg.as_string())
    s.close()
    print 'mail sent!'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send Gmail.')
    parser.add_argument('mail_to',
                        type=str,
                        default='',
                        help='To address')
    parser.add_argument('-s',
                        '--subject',
                        dest='subject',
                        type=str,
                        default=SUBJECT,
                        help='Subject')
    parser.add_argument('-d',
                        '--device',
                        dest='device',
                        type=str,
                        default=DEVICE,
                        help='Device')
    args = parser.parse_args()
    msg = create_message(args.mail_to, args.subject, args.device)
    send_via_gmail(args.mail_to, msg)
