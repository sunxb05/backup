#!/bin/bash
#SBATCH -J feco4-s21.pyfrag_input 
#SBATCH -N 1
#SBATCH -t 96:00:00
#SBATCH --ntasks-per-node=4
#SBATCH --partition=tc6
#SBATCH --output=feco4-s21.pyfrag_input.out
#SBATCH --error=feco4-s21.pyfrag_input.err

export NSCM=4
export SCM_TMPDIR=$TMPDIR
#export SCM_DEBUG=yes
cd $SCM_TMPDIR

rm -f runset
for b in SZ DZ DZP TZP TZ2P QZ4P
do
    "$ADFBIN/adfprep" -t "$ADFHOME/examples/adf/ConvergenceTestCH4/methane.adf" -b $b -j methane.$b>> runset
done

chmod +x runset
./runset

echo Results
echo Basis set convergence of Bonding Energy, SZ DZ DZP TZP TZ2P QZ4P
for b in SZ DZ DZP TZP TZ2P QZ4P
do
    "$ADFBIN/adfreport" "methane.$b.t21" BondingEnergy
done

rm -f runset
for i in 2 3 4 5
do
    "$ADFBIN/adfprep" -t "$ADFHOME/examples/adf/ConvergenceTestCH4/methane.adf" -b DZP -i $i -j methane.$i>> runset
done
"$ADFBIN/adfprep" -t "$ADFHOME/examples/adf/ConvergenceTestCH4/methane.adf" -b DZP -i Basic -j methane.bb>> runset
"$ADFBIN/adfprep" -t "$ADFHOME/examples/adf/ConvergenceTestCH4/methane.adf" -b DZP -i Normal -j methane.bn>> runset
"$ADFBIN/adfprep" -t "$ADFHOME/examples/adf/ConvergenceTestCH4/methane.adf" -b DZP -i Good -j methane.bg>> runset
"$ADFBIN/adfprep" -t "$ADFHOME/examples/adf/ConvergenceTestCH4/methane.adf" -b DZP -i VeryGood -j methane.bv>> runset
"$ADFBIN/adfprep" -t "$ADFHOME/examples/adf/ConvergenceTestCH4/methane.adf" -b DZP -i Excellent -j methane.be>> runset

chmod +x runset
./runset

echo Integration convergence of Bonding Energy, 2 3 4 5
for i in 2 3 4 5
do
    "$ADFBIN/adfreport" "methane.$i.t21" BondingEnergy
done

echo Integration Becke convergence of Bonding Energy, Basic, Normal, Good, VeryGood, Excellent
"$ADFBIN/adfreport" "methane.bb.t21" BondingEnergy
"$ADFBIN/adfreport" "methane.bn.t21" BondingEnergy
"$ADFBIN/adfreport" "methane.bg.t21" BondingEnergy
"$ADFBIN/adfreport" "methane.bv.t21" BondingEnergy
"$ADFBIN/adfreport" "methane.be.t21" BondingEnergy

echo Ready
