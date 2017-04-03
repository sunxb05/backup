# Default imports
from qmworks import Settings, templates, run, rdkitTools
from noodles import gather
from plams import Molecule

# User Defined imports
from qmworks.packages.SCM import adf, dftb, pyfrag
from qmworks.components import PES, select_max
import plams
import sys
from qmworks.templates import get_template
from qmworks.templates.atoms import atom

plams.init()

template = "COc1ccc(cc1)[N-][N+]#Cc2ccccc2.C3NCC34C=C4"
templatess = ["COc1ccc(cc1)[N-][N+]#Cc2ccccc2.C3NCC34C=C4","CC.CC"]
mol = rdkitTools.smiles2plams(template)
HH = plams.Molecule("H_Mes2PCBH2_TS3series2.xyz")
newmol = HH
# User define Settings
sp= Settings()
pf=Settings()

job_list = []

for item in templatess:
    a = atom()
    a.getjson(item)
    templates.pyf = get_template('pyf.json')
    job_list.append(pyfrag(templates.pyf.overlay(sp), newmol, templates.singlepoint.overlay(pf)))


results = run(gather(*job_list), n_processes = 1)
