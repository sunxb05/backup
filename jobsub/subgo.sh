#!/bin/bash

script=/home/x2sun/bin/inputsample/GO
coordinates=$1
coordinate=$(<$coordinates)
awk -v r="$coordinate" '{sub("PLACEHOLDERATOM",r,$0); print}' $script > input

filename=$(basename "$(cd "$(dirname "$1")" ; pwd -P )")
oldjobname=$(grep  "#SBATCH.*-J.*"  input)
jobname=${oldjobname##* }

awk -v r=$jobname  '{sub(r, "jobName"); print}' input > tmp
awk -v r=$filename '{sub("jobName", r); print}' tmp   > inputfile

#sbatch inputfile
rm tmp input
