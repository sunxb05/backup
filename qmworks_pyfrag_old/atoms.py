from qmworks import rdkitTools
from rdkit import Chem
from qmworks.utils import dict2Setting
import json
from os.path import join
import os, string, re, math, sys
script="/scistor/tc/xsn800/miniconda3/envs/qmworks/lib/python3.5/site-packages/qmworks/data/templates/pf.json"
script_1="/scistor/tc/xsn800/miniconda3/envs/qmworks/lib/python3.5/site-packages/qmworks/data/templates/pyf.json"
class atom:
    def __init__(self):
        self.dict_1 = {}
        self.dict_2 = {}


    def getjson(self,template):
        mol = rdkitTools.smiles2plams(template)
        rdmol = rdkitTools.plams2rdkit(mol)
        frags = Chem.GetMolFrags(rdmol, asMols=True)
        frag1 = rdkitTools.rdkit2plams(frags[0])
        frag2 = rdkitTools.rdkit2plams(frags[1])
        frag_1 = Chem.GetMolFrags(rdmol)[0]
        frag_2 = Chem.GetMolFrags(rdmol)[1]
        self.dict_1 = {str(i+1):"."+a.symbol for i,a in zip(frag_1,frag1.atoms)}
        self.dict_1["end"] = "frag1"
        json_1 = json.dumps(self.dict_1)
        self.dict_2 = {str(i+1):"."+a.symbol for i,a in zip(frag_2,frag2.atoms)}
        self.dict_2["end"] = "frag2"
        json_2 = json.dumps(self.dict_2)
#        return json_1, json_2
        replace_1="\"atom1\""
        replace_2="\"atom2\""
        with open(script,"r") as f:
            data=f.read()
        f.close()
        data_1=re.compile(r'%s' % replace_1, re.DOTALL).sub(json_1, data)
        data_2=re.compile(r'%s' % replace_2, re.DOTALL).sub(json_2, data_1)
        with open(script_1,"w") as f:
            f.write(data_2)
        f.close()
