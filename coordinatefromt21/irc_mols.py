#usage: python irc_mols.py [some_t21_file]

import os, sys
from scm.plams import KFFile, PT, Molecule, Atom

if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
    print('Invalid file')
    sys.exit(1)

def int2inp(kf):
    aoi = kf[('Geometry', 'atom order index')]
    n = len(aoi)//2
    return aoi[:n]

def atomic_numbers(kf):
    mapping = int2inp(kf)
    n = kf[('Geometry', 'nr of atoms')]
    tmp = kf[('Geometry', 'atomtype')].split()
    atomtypes = {i+1 : PT.get_atomic_number(tmp[i]) for i in range(len(tmp))}
    atomtype_idx = kf[('Geometry', 'fragment and atomtype index')][-n:]
    atnums = [atomtypes[i] for i in atomtype_idx]
    return [atnums[mapping[i]-1] for i in range(len(atnums))]

def get_molecule(kf, section, variable, unit='bohr', internal=False, n=1):
    atnums = atomic_numbers(kf)
    natoms = len(atnums)
    coords = kf[(section, variable)]
    coords = [coords[i:i+3] for i in range(0,len(coords),3)]
    if len(coords) > natoms:
        if len(coords) < n*natoms:
           print('get_molecule() failed. Not enough data in {}%{} to extract geometry no {}'.format(section, variable, n))
           sys.exit(1)
        coords = coords[(n-1)*natoms : n*natoms]
    if internal:
        mapping = int2inp(kf)
        coords = [coords[mapping[i]-1] for i in range(len(coords))]
    ret = Molecule()
    for z,crd in zip(atnums,coords):
        ret.add_atom(Atom(atnum=z, coords=crd, unit=unit))
    return ret


tape21 = KFFile(sys.argv[1])


fw = tape21[('IRC_Forward','CurrentPoint')]
forward = [get_molecule(tape21, 'IRC_Forward', 'xyz', n=i+1) for i in range(fw)]
bw = tape21[('IRC_Backward','CurrentPoint')]
backward = [get_molecule(tape21, 'IRC_Backward', 'xyz', n=i+1) for i in range(bw)]

#So now 'forward' and 'backward' are simply lists of different Molecule instances. I don't know what do you need them for. The code below prints everything to the standard output AND saves each frame as a separate .xyz file. Feel free to comment out or modify whatever you don't need:

for i,mol in enumerate(forward):
    print('Forward {}'.format(i+1))
    print(mol)
    print('='*69)
    mol.write('forward_{}.xyz'.format(i+1))

for i,mol in enumerate(backward):
    print('Backward {}'.format(i+1))
    print(mol)
    print('='*69)
    mol.write('backward_{}.xyz'.format(i+1))
