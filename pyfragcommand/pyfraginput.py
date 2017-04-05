INPUT_SPECS
type = IRC

output file = feco4-s37.t21 

fa1_name = feco4-ch4

print bond   10 14    1.093
print strain frag1  -1655.7   
print strain frag2  -554.1 

frag1 = feco4
1.Fe
2.O
3.C
4.O
5.O
6.O
7.C
8.C
9.C
end frag1

frag2 = ch4
10.C  
11.H  
12.H  
13.H  
14.H  
end frag2


EXTRA frag1
  CHARGE 0
  SYMMETRY AUTO
END EXTRA frag1

EXTRA frag2
  CHARGE 0
  SYMMETRY AUTO
END EXTRA frag2

EXTRA fa
  CHARGE 0
  SYMMETRY AUTO
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
 core Small
END

SCF
ITERATIONS 99
CONVERGE 0.000001
MIXING 0.20
END


END INPUT
eor
