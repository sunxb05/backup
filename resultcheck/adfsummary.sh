if test "$1" = ""
then
  echo Give output filenames
else
  outputs=$*
fi

for output in $outputs
do

geomconverged=false
igc=0

# printf "\n ADF summary for $output \n\n"

symms=`grep 'Symmetry  :' $output |grep -v ATOM|cut -d ':' -f 4`

newbranch=`grep -c 'Optimization code branch:                       NEW' $output`

if test "$newbranch" -eq "0"
then

  eners=`grep -En 'Geometry CONV|new :' $output| cut -d":" -f 1`
  gmaxs=`grep ' gradient max' $output | awk '{print $3}'`
  grmss=`grep ' gradient rms' $output | awk '{print $3}'`
  nlines=`echo $eners |wc -l`
  if test "$nlines" -eq '0'
  then
    eners=`grep '  Total Bond' $output | awk '{print $4}'`
  fi
  nlines=`echo $eners |wc -w`
  i=1
  printf "%15s %15s %15s %10s\n" Energy "Gmax,adf" "Grms,adf" "Sym"
  printf "%58s\n" '=========================================================='
  while test "$i" -le "$nlines"
  do
    enerline=`echo $eners |cut -d ' ' -f $i`
    line=`head -$enerline $output|tail -1`
    ener=`echo $line |awk '{printf"%14.6f",627.509541*$3}'`
    geomconv=`echo $line |awk '{print $1 $2}'`
    if test "$geomconv" = "GeometryCONVERGED"
    then
      geomconverged=true
      ener=`grep '  Total Bonding Energy' $output |tail -1|awk '{printf"%14.6f",627.509541*$4}'`
    fi
    gmax=`echo $gmaxs |cut -d ' ' -f $i`
    grms=`echo $grmss |cut -d ' ' -f $i`
    symm=`echo $symms|cut -d ' ' -f $i`
    if $geomconverged
    then
      igc=`expr $igc + 1`
      if test "$igc" -eq 1
      then
        printf "%58s\n" '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        printf " Geometry CONVERGED !!!\n"
        printf " Energy at optimized geometry : %15.4f (kcal/mol)\n" $ener
        cosmo=`grep -ci 'Post-SCF Solvation Energies' $output`
        if test "$cosmo" -gt "0"
        then
          ecosmopost=`grep 'Solvation Energy (cd):' $output |tail -1|awk '{printf"%14.6f",627.509541*$4}'`
          printf "%58s\n" '----------------------------------------------------------'
          printf          " Note that this final energy includes the post-SCF COSMO\n"
          printf          " Solvation energy, of %7.4f kcal/mol.\n" $ecosmopost
          printf          " This energy term was NOT included in the energies during\n"
          printf          " the Geometry Optimizations shown above.\n"
          printf "%58s\n" '----------------------------------------------------------'
        fi
        printf "%58s\n" '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
      fi
    elif test "$gmax" != ""
    then
      printf "%15.4f %15.6f %15.6f %10s\n" $ener $gmax $grms $symm
    fi
    i=`expr $i + 1`
  done
else

  eners=`grep -En 'GEOMETRY CONV|current energy' $output|grep -v ' current'| cut -d":" -f 1`
  gmaxs=`grep 'constrained gradient max' $output | grep -v ' constrained'|awk '{print $4}'`
  grmss=`grep 'constrained gradient rms' $output | grep -v ' constrained'|awk '{print $4}'`
  nlines=`echo $eners |wc -l`
  if test "$nlines" -eq '0'
  then
    eners=`grep '  Total Bond' $output | awk '{print $4}'`
  fi
  nlines=`echo $eners |wc -w`
  i=1

  printf "%15s %15s %15s %10s\n" Energy "Gmax,adf" "Grms,adf" "Sym"
  printf "%58s\n" '=========================================================='
  while test "$i" -le "$nlines"
  do
    enerline=`echo $eners |cut -d ' ' -f $i`
    line=`head -$enerline $output|tail -1`
    ener=`echo $line |awk '{printf"%14.6f",627.509541*$3}'`
    geomconv=`echo $line |grep -ci 'GEOMETRY CONVERGED'`
    if test "$geomconv" -gt "0"
    then
      geomconverged=true
      ener=`grep '  Total Bonding Energy' $output |tail -1|awk '{printf"%14.6f",627.509541*$4}'`
    fi
    gmax=`echo $gmaxs |cut -d ' ' -f $i`
    grms=`echo $grmss |cut -d ' ' -f $i`
    symm=`echo $symms|cut -d ' ' -f $i`
    if $geomconverged
    then
      igc=`expr $igc + 1`
      if test "$igc" -eq 1
      then
        printf "%58s\n" '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        printf " Geometry CONVERGED !!!\n"
        printf " Energy at optimized geometry : %15.4f (kcal/mol)\n" $ener
        printf "%58s\n" '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        grep -A 200 'Calculating Energy Terms for Final Geometry' $output | grep -B 200 '>>>> CORORT' | grep -v 'CORORT' | grep -v 'Coordinates'| grep -v 'Atom' | grep -v 'Calculating'
      fi
    elif test "$gmax" != ""
    then
      printf "%15.4f %15.6f %15.6f %10s\n" $ener $gmax $grms $symm
    fi
    i=`expr $i + 1`
  done
fi
done
