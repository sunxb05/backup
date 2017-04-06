INPUT_SPECS
type = IRC

output file = pyfrag14.amv

fa = feco4

print bond   1 3    1.81
print strain frag1  -1236.41   
print strain frag2  -346.69 

frag1 = fe
1.Fe
4.O
5.O
6.O
7.C
8.C
9.C
end frag1

frag2 = co4
2.O
3.C
end frag2

make gnuplot

EXTRA frag1
  CHARGE 0  
  SYMMETRY AUTO

  OCCUPATIONS
  A 66 1 1
  END

END EXTRA frag1

EXTRA frag2
  CHARGE 0  
  SYMMETRY AUTO
END EXTRA frag2

EXTRA fa
  UNRESTRICTED
  CHARGE 0  2 
  SYMMETRY AUTO

  FRAGOCCUPATIONS
  frag1
  A 35//33
  SUBEND
  END

END EXTRA fa

END INPUT_SPECS


$ADFBIN/adf << eor 

ATOMS
END

XC
  GGA OPBE
END

RELATIVISTIC SCALAR ZORA

BECKEGRID
  Quality VeryGood
END

BASIS 
 type TZ2P
 core None
END

SCF
ITERATIONS 199
CONVERGE 0.00001
MIXING 0.20
END

GEOMETRY
  SP
END

END INPUT
eor
