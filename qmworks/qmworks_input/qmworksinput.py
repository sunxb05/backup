# Default imports
from qmworks import Settings, templates, run
from noodles import gather
from plams import Molecule

# User Defined imports
from qmworks.packages.SCM import adf, dftb

import plams
# ========== =============

plams.init()

import os
import sys
import fnmatch
from os.path   import join

# Read the Molecule from file
path = "/home/xsun/test"
files     = os.listdir(path)
xyzFiles  = filter(lambda x: fnmatch.fnmatch(x,"*.xyz"), files)
pathsXYZ  = map(lambda x: join(path,x), xyzFiles)
molecules = [Molecule(name, 'xyz') for name in pathsXYZ]

# User define Settings
settings = Settings()
settings.functional = "pbe"
settings.basis = "TZ2P"
settings.specific.adf.charge = "0 2"
settings.specific.adf.unrestricted = ""

# Run the TS optimization, using the default TS template
job_list = []
for m in molecules:
    dftb_freq = dftb(templates.freq.overlay(settings),m)
    t = Settings()
    t.specific.adf.geometry.inithess = dftb_freq.archive.path
    ts = adf(templates.ts.overlay(settings).overlay(t), dftb_freq.molecule)
    job_list.append(adf(templates.freq.overlay(settings), ts.molecule))

wf = gather(*job_list)

results = run(wf, n_processes = 1)
