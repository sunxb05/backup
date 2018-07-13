#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$1")" ; pwd -P )"

# coorNum="$( ls -lR | grep -v ^d | wc -l )"
coorNum="$( cd $SCRIPTPATH/$1 ; ls -1 | wc -l )"
echo $coorNum

fileNum=1
# adfinput ~/Desktop/test.adf&
cd $SCRIPTPATH/$1

while test "$fileNum" -le "$coorNum"
do
  echo $fileNum
  if [ -e $fileNum ]; then
    sublime $fileNum
    cliclick c:. kd:cmd t:a  kd:cmd t:c  w:500
    adfinput ../test.adf&
    cliclick w:5000
    cliclick c:320,400 c:. kd:cmd t:v w:1000 c:. w:2000
    python3 ../screen.py $fileNum &
    cliclick w:500 c:320,400 c:. kd:cmd t:a kp:delete w:500 c:. kd:cmd t:w kp:enter
    cliclick w:3000
  fi
  fileNum=`expr $fileNum + 1`
done
