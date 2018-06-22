#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$1")" ; pwd -P )"

if [ -e $SCRIPTPATH/result.txt ]; then
  rm $SCRIPTPATH/result.txt
fi

dirNum="$( ls -lR | grep ^d | wc -l )"
fileNum=1

while test "$fileNum" -le "$dirNum"
do
  if  [ -d "$SCRIPTPATH/$fileNum" ] ; then
        cd $SCRIPTPATH/$fileNum
        echo $fileNum
        if [ -e *out ]; then
          sh /home/x2sun/bin/adfsummary.sh *out                >> $SCRIPTPATH/result.txt
        else
          printf "\n\n jobs for $f has not started \n\n"      >> $SCRIPTPATH/result.txt
        fi
        cd $SCRIPTPATH
  fi
fileNum=`expr $fileNum + 1`
done


