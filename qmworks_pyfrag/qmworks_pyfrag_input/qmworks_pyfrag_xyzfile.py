# Default imports
from qmworks import Settings, templates, run, molkit
from noodles import gather
from plams import Molecule

# User Defined imports
from qmworks.packages.SCM import adf,pyfrag
from qmworks.components import PES, select_max
import plams
import sys
import os
import fnmatch
from os.path   import join

path = "/Users/xiaobo/Desktop/py/molecule.xyz"
mole = Molecule(path)

settings = Settings()
sett = settings

#inputkeys = {'irct21': [['geometry_forward.t21']], 'fragment': [[2], [1, 3, 4, 5, 6]], 'bondlength': [[1.0, 2.0, 1.09]], 'orbitalenergy': [['frag1', 'HOMO']], 'overlap': [['frag1', 'HOMO', 'frag2', 'LUMO']], 'hirshfeld': [['frag1'], ['frag2']], 'strain': [[1.0], [2.0], [3.0]],  'population': [['frag3', 'HOMO'], ['AA', 'frag2', '3']], 'irrepOI': [['AA']]}
inputkeys = {'fragment': [[2], [1, 3, 4, 5, 6]],'strain': [[1.0], [2.0]] }
job_list = []

irc = adf(templates.irc.overlay(sett), mole)
pyfrag_1 = pyfrag(templates.frag.overlay(sett),settings_2 = templates.fa.overlay(sett), inputArgues= irc.kf.path, other = inputkeys  )

job_list.append(irc)
job_list.append(pyfrag_1)


results = run(gather(*job_list), n_processes = 4)

