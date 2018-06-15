#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$1")" ; pwd -P )"

if [ -e $SCRIPTPATH/result.txt ]; then
  rm $SCRIPTPATH/result.txt
fi

squeue -u x2sun                                                >> $SCRIPTPATH/result.txt

for f in $SCRIPTPATH/*
do
  if  [ -d "$f" ] ; then
      cd $f
        echo $f
        grep -v ' constrained' *txt |awk '{print }'            >> $SCRIPTPATH/result.txt
        if [ -e *out ]; then
          printf "\n\n jobs for $f has finished \n\n"          >> $SCRIPTPATH/result.txt
          sh /home/x2sun/bin/adfsummary.sh *out                >> $SCRIPTPATH/result.txt
        else
          printf "\n\n jobs for $f has not finished \n\n"      >> $SCRIPTPATH/result.txt
        fi
  fi
done
