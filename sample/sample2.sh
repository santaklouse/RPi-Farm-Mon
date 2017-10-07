DATE=`date '+%Y/%m/%d %H:%M:%S'`
SUBJECT="Picture: ${DATE}"
MAILBODY=/tmp/content.txt
IMAGE=/tmp/image.jpg
DESTINATION="EXAMPLE@EXAMPLE.COM"    # < Change to your mail address.

echo "Date: $DATE" > $MAILBODY
fswebcam -r 640x480 --jpeg 95 $IMAGE

mutt -s "$SUBJECT" $DESTINATION -a $IMAGE < $MAILBODY

rm $MAILBODY
rm $IMAGE
