#! /bin/bash

script=/home/x2sun/bin/inputsample/TS

coordinates=$1
coordinate=$(<$coordinates)
tsrcset=$2
tsrc=$(<$tsrcset)
awk -v r="$coordinate" '{sub("PLACEHOLDERATOM",r,$0); print}' $script > tmp1
awk -v r="$tsrc" '{sub("PLACETSRC",r,$0); print}' tmp1 > input


filename=$(basename "$(cd "$(dirname "$1")" ; pwd -P )")

oldjobname=$(grep  "#SBATCH.*-J.*"  input)
jobname=${oldjobname##* }

awk -v r=$jobname  '{sub(r, "jobName"); print}' input > tmp2
awk -v r=$filename '{sub("jobName", r); print}' tmp2   > inputfile

#sbatch inputfile
rm tmp* input
