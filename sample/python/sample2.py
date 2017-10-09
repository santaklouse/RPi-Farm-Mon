import os
import boto3

filename = 'image.jpg'
bucket_name = 'monitor-u7wdtw9b'

command = 'fswebcam -r 640x480 --jpeg 95 /tmp/' + filename
os.system(command)
s3 = boto3.client('s3')
s3.upload_file('/tmp/' + filename, bucket_name, filename)
command = 'rm /tmp/' + filename
os.system(command)
