# Default imports
from qmworks import Settings, templates, run, molkit
from noodles import gather
from plams import Molecule

# User Defined imports
from qmworks.packages.SCM import dftb,adf
#from qmworks.packages.SCM import dftb as adf  # This is for testing purposes
from qmworks.components import PES, select_max

import sys

import plams
# ========== =============

template = "COc1ccc(cc1)[N-][N+]#Cc2ccccc2.C3NCC34C=C4"
mol = molkit.from_smiles(template)

list_of_modifications = {"CHO": "[#0:1]>>C[C:1]=O"}
HH = plams.Molecule("mol.xyz")
HH.guess_bonds()
newmol = molkit.apply_template(HH,template)
# Change the one of the hydrogens to a dummy atoms 
temp = molkit.modify_atom(newmol, 41, '*')
# Put coordinates of dummy atoms to 0.0, this will force generating new coordinates for the new atoms
temp.atoms[41].move_to((0.0,0.0,0.0))
temp.writemol(open('tmp.mol', 'w'))

# Replace dummy atoms by new groups, generate coordinates only for new atoms
job_list = []
for mod,smirks in list_of_modifications.items():
    temp2, unchanged_atoms = molkit.apply_reaction_smarts(temp, smirks)
    temp2.writemol(open('tmp2.mol', 'w'))
    #generate job
    s = Settings()
    s.freeze = [a+1 for a in unchanged_atoms]
    partial_geometry = adf(templates.geometry.overlay(s), temp2, job_name="partial_opt_"+mod)
    job_list.append(adf(templates.ts, partial_geometry.molecule, job_name="ts_"+mod))

results = run(gather(*job_list), n_processes=1)
