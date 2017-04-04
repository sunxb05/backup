The file with degenerate d orbitals:

CHARGE    0
SYMMETRY ATOM

OCCUPATIONS
S 6
P 12
D 8
END

ATOMS
Fe       0.00000000       0.00000000      -0.52148000
END


The EDA file:

FRAGOCCUPATIONS
f1
S 3//3
P 6//6
D 5//3
SUBEND
END

CHARGE    0 2
UNRESTRICTED

ATOMS
Fe       0.00000000       0.00000000      -0.52148000 f=f1
O      -2.92706000       0.00000000      -0.44214000 f=f2
C      -1.77698000       0.00000000      -0.49473000 f=f2
O       0.00000000       2.48236000       0.94078000 f=f2
O       2.92706000       0.00000000      -0.44214000 f=f2
O       0.00000000      -2.48236000       0.94078000 f=f2
C       0.00000000      -1.54742000       0.25683000 f=f2
C       1.77698000       0.00000000      -0.49473000 f=f2
C       0.00000000       1.54742000       0.25683000 f=f2
END


The file for Fe with non-degenerate d orbitals. One unpaired electron in A1 and one in B2. You should check the shape of the d orbitals and where the unpaired electrons are in the optimized full molecule:

CHARGE    0
SYMMETRY C(2V)

OCCUPATIONS
A1 13
A2 2
B1 6
B2 5
END

ATOMS
Fe       0.00000000       0.00000000      -0.52148000
END


The EDA file:

FRAGOCCUPATIONS
f1
A1 7//6
A2 1//1
B1 3//3
B2 3//2
SUBEND
END

CHARGE    0 2
UNRESTRICTED

ATOMS
Fe       0.00000000       0.00000000      -0.52148000 f=f1
O      -2.92706000       0.00000000      -0.44214000 f=f2
C      -1.77698000       0.00000000      -0.49473000 f=f2
O       0.00000000       2.48236000       0.94078000 f=f2
O       2.92706000       0.00000000      -0.44214000 f=f2
O       0.00000000      -2.48236000       0.94078000 f=f2
C       0.00000000      -1.54742000       0.25683000 f=f2
C       1.77698000       0.00000000      -0.49473000 f=f2
C       0.00000000       1.54742000       0.25683000 f=f2
END

