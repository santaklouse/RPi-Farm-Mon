DATE=`date '+%Y/%m/%d %H:%M:%S'`
SUBJECT="Environment Data: ${DATE}"
MAILBODY=/tmp/status.txt
IMAGE=/tmp/image.jpg
DESTINATION="EXAMPLE@EXAMPLE.COM"    # < Change to your mail address.

echo "Date: $DATE" > $MAILBODY
python /home/pi/RPi-Farm-Mon/lib/sht31.py >> $MAILBODY
python /home/pi/RPi-Farm-Mon/lib/tsl2561.py >> $MAILBODY
fswebcam -r 640x480 --jpeg 95 $IMAGE
    
mutt -s "$SUBJECT" $DESTINATION -a $IMAGE < $MAILBODY
rm $MAILBODY
rm $IMAGE
