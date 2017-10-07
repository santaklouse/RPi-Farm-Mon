DATE=`date '+%Y/%m/%d %H:%M:%S'`
SUBJECT="Sensor Data: ${DATE}"
MAILBODY=/tmp/status.txt
DESTINATION="EXAMPLE@EXAMPLE.COM"    # < Change to your mail address.

echo "Date: $DATE" > $MAILBODY
python /home/pi/RPi-Farm-Mon/lib/sht31.py >> $MAILBODY
python /home/pi/RPi-Farm-Mon/lib/tsl2561.py >> $MAILBODY
    
mutt -s "$SUBJECT" $DESTINATION < $MAILBODY
rm $MAILBODY
