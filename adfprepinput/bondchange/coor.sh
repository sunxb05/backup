rm -f bondchange.xyz
for bond in 1 2 3
    do
      "adfprep" -t "test.adf" -m "example.xyz" -dist "1 2 $bond" -j `basename $bond`> $bond.txt
      grep -A 200 'ATOMS' $bond.txt | grep -B 200 'GUIBONDS' | grep -v 'ATOMS' | grep -v 'GUIBONDS'| grep -v 'END' >> bondchange.xyz
      rm $bond.txt
    done
