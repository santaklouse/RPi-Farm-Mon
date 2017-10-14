import os
import time
import datetime
import boto3

bucket_name = 'example_bucket_name'
folder_name = 'raspberrypi'
webcam_device = '/dev/video0'
smart_plug_ip_address = '192.168.100.51'
rightnow = datetime.datetime.now().strftime('%Y%m%d-%H%M')

command = ("pyhs100 --ip=%s on"
           % smart_plug_ip_address)
os.system(command)
time.sleep(3)

command = ("fswebcam -d %s -r 1280x960 --jpeg 95 /tmp/latest.jpg"
           % webcam_device)
os.system(command)
time.sleep(1)

command = ("pyhs100 --ip=%s off"
           % smart_plug_ip_address)
os.system(command)

s3 = boto3.resource('s3')
s3.meta.client.upload_file(
    "/tmp/latest.jpg",
    bucket_name,
    "%s/latest.jpg" % folder_name,
    ExtraArgs={'ContentType': "image/jpeg", 'ACL': "public-read"}
    )
s3.meta.client.upload_file(
    "/tmp/latest.jpg",
    bucket_name,
    "%s/%s.jpg" % (folder_name, rightnow),
    ExtraArgs={'ContentType': "image/jpeg", 'ACL': "public-read"}
    )

command = "rm /tmp/latest.jpg"
os.system(command)
