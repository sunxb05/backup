$ADFBIN/adf<<eor

TITLE  RC=H

XC
  GGA OPBE
END

RELATIVISTIC SCALAR ZORA

BECKEGRID
  Quality VeryGood
END

BASIS
TYPE TZ2P 
Core Small
END

SCF
ITERATIONS 199
CONVERGE 0.00001
MIXING 0.20
END

Geometry
 IRC Forward POINTS=10 STEP=0.5
ITERATIONS 300
CONVERGE 0.00001
End

GEOVAR
  angleone 94.99999985F  
End

SYMMETRY  AUTO
CHARGE    0 0 


ATOMS Zmatrix
    0 C     0     0     0                0.0                0.0                0.0
    1 Fe     1     0     0         1.77463533                0.0                0.0
    2 C     2     1     0        1.720739197        angleone                   0.0
    3 O     1     2     3        1.152997786        170.1375144       0.4414501074
    4 O     3     2     1        1.156840832        175.8157372       0.3252588425
    5 O     1     2     3        3.623768332        53.31172192        88.90262935
    6 O     1     2     6        3.627242213        53.22036559        182.1985887
    7 C     7     1     2        1.153020241        30.04810028        359.2832121
    8 C     6     1     2        1.153032188        30.11544823       0.7342620072
    9 C     1     2     3        4.298632419        14.62000636        179.8298864
   10 H    10     1     2        1.086196345        114.6755554         247.848927
   11 H    10     1    11        1.086197923         115.054752        224.4229847
   12 H    10     1    12        1.083582791        82.91372102        247.7838261
   13 Cl    10     1    13              2.161        47.94850007        179.6947265
END


END INPUT
eor

mv TAPE21 $HOME/feco4-s519/feco4-s519.t21
