#! /bin/bash
script=/scistor/tc/xsn800/bin/inputsample/GO
coordinates=$1
cp $coordinates coordinatefix
coordinatenew=coordinatefix

sed -i '1d' $coordinatenew
coordinate=$(<$coordinatenew)
awk -v r="$coordinate" '{sub("PLACEHOLDERATOM",r,$0); print}' $script > input

sbatch input


rm coordinatefix
