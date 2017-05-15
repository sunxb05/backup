This example illustrates usage of the bond energy decomposition scheme used in ADF. A proper decomposition of an electron-pair bond energy requires specifying opposite spins for the unpaired electrons of the respective radical fragments, which can be done with the input key FragOccupations. Please note that if one neglects explicitly specifying opposite spins for the unpaired electrons of the fragments, each of them is treated as being half an alpha and half a beta electron and consequently, they enter into a spurious Pauli repulsive interaction. This result, among others, into the Pauli repulsion term being too repulsive and the orbital interaction term being too much stabilizing.
The example consists of an analysis of the C-F single bond between CH3 radicals and F. The fragment calculations used to provide the TAPE21 for the overall CH3F calculation must be done, for technical reasons, in the restricted mode. The proper spins are then specified in the calculation of the overall molecule using the FragOccupations key. Note that in order to assign electrons to orbitals, the open-shell unrestricted single-point calculation for the two fragments is recommended. ADFlevel will show orbital occupations in these fragments, from which occupations for orbitals with different irreducible label of symmetry for the total complex can be derived.

1. Fragment1 calculation.

$ADFBIN/adf<<eor
TITLE  PIPI
XC
  GGA OPBE
END

BECKEGRID
  Quality VeryGood
END

BASIS
TYPE TZ2P
Core None
END

SCF
ITERATIONS 150
CONVERGE 0.00001
MIXING 0.20
END

SYMMETRY C(3V)
CHARGE    0 0

OCCUPATIONS
E1 4
A1 5

END

ATOMS
C      -3.23901900       0.98595595       0.02457008
H      -4.06379418       0.40883398      -0.44184657
H      -3.17153509       0.72946786       1.10184121
H      -3.43884872       2.07172920      -0.08512131
END

END INPUT
Eor



2. Fragment2 calculation.

$ADFBIN/adf<<eor
TITLE PIPI
XC
  GGA OPBE
END

BECKEGRID
  Quality VeryGood
END

BASIS
TYPE TZ2P
Core None
END

SCF
ITERATIONS 150
CONVERGE 0.00001
MIXING 0.20
END

SYMMETRY ATOM
CHARGE    0 0

OCCUPATIONS
S 4
P 5
END

ATOMS
F      -2.04710582       0.67190464      -0.59944404
END

END INPUT
eor




3. Fragment analysis calculation.


$ADFBIN/adf<<eor
TITLE  PIPI
XC
  GGA OPBE
END

BECKEGRID
  Quality VeryGood
END

BASIS
TYPE TZ2P
Core None
END

SCF
ITERATIONS 0
CONVERGE 0.00001
MIXING 0.20
END

FRAGOCCUPATIONS
f1
E1 2//2
A1 3//2
SUBEND
f2
S 2//2
P 2//3
SUBEND
END

SYMMETRY C(3V)
CHARGE    0 0

ATOMS
C      -3.23901900       0.98595595       0.02457008 f=f1
H      -4.06379418       0.40883398      -0.44184657 f=f1
H      -3.17153509       0.72946786       1.10184121 f=f1
H      -3.43884872       2.07172920      -0.08512131 f=f1
F      -2.04710582       0.67190464      -0.59944404 f=f2
END

Fragments
f1 /scistor/tc/xsn800/codetest/openshell/frag1.t21 
f2 /scistor/tc/xsn800/codetest/openshell/frag2.t21 
END
END INPUT
eor

