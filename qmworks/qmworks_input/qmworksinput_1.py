# Default imports
from qmworks import Settings, templates, run, molkit
#from qmworks.draw_workflow import draw_workflow
from noodles import gather

# User Defined imports
from qmworks.packages.SCM import dftb, adf
#from qmworks.packages.orca import orca as adf
# from qmworks.packages.SCM import dftb as adf  # This is for testing purposes
from qmworks.components import Distance, select_max

import plams
# ========== =============

hartree2kcal = 627.5095

# List of reactions, defined by name, reactants and products (as smiles strings)
reactions = [
    ["et01", "C=C", "[CH]#[N+][CH2-]", "C1C=NCC1"],
    ["et02", "C=C", "[CH]#[N+][NH-]", "C1C=NNC1"],
    ["et03", "C=C", "[CH]#[N+][O-]", "C1C=NOC1"],
    ["et04", "C=C", "[N]#[N+][CH2-]", "C1N=NCC1"],
    ["et05", "C=C", "[N]#[N+][NH-]", "C1N=NNC1"],
    ["et06", "C=C", "[N]#[N+][O-]", "C1N=NOC1"],
    ["et07", "C=C", "[CH2]=[NH+][CH2-]", "C1CNCC1"],
    ["et08", "C=C", "[CH2]=[NH+][NH-]", "C1CNNC1"],
    ["et09", "C=C", "[CH2]=[NH+][O-]", "C1CNOC1"],
    ["et10", "C=C", "[NH]=[NH+][NH-]", "C1NNNC1"],
    ["et11", "C=C", "[NH]=[NH+][O-]", "C1NNOC1"],
    ["et12", "C=C", "O=[NH+][O-]", "C1ONOC1"]]


# Bonds to be formed (based on atom numbers in de product)
bond1 = Distance(0, 1)
bond2 = Distance(3, 4)

# User define Settings
settings = Settings()
settings.functional = "bp86"
settings.basis = "TZ2P"
#settings.specific.adf.dependency = "bas = 5e-3"
#settings.specific.adf.AddDiffuseFit = " "
settings.specific.dftb.dftb.scc.ndiis = 4
settings.specific.dftb.dftb.scc.Mixing = 0.1
settings.specific.dftb.dftb.scc.iterations = 300


job_list = []
# Loop over all reactions
for name, r1_smiles, r2_smiles, p_smiles in reactions:

  # Prepare reactant1 job
    r1_mol =  molkit.from_smiles(r1_smiles)
    r1_dftb = dftb(templates.geometry.overlay(settings), r1_mol, job_name=name + "_r1_DFTB")
    r1 =      adf(templates.geometry.overlay(settings), r1_dftb.molecule, job_name=name + "_r1")
    r1_freq = adf(templates.freq.overlay(settings), r1.molecule, job_name=name + "_r1_freq")

  # Prepare reactant2 job
    r2_mol =  molkit.from_smiles(r2_smiles)
    r2_dftb = dftb(templates.geometry.overlay(settings), r2_mol, job_name=name + "_r2_DFTB")
    r2 =      adf(templates.geometry.overlay(settings), r2_dftb.molecule, job_name=name + "_r2")
    r2_freq = adf(templates.freq.overlay(settings), r2.molecule, job_name=name + "_r2_freq")

# Prepare product job
    p_mol =  molkit.from_smiles(p_smiles)
    p_mol.properties.name = name
    p_dftb = dftb(templates.geometry.overlay(settings), p_mol, job_name=name + "_p_DFTB")
    p =      adf(templates.geometry.overlay(settings), p_dftb.molecule, job_name=name + "_p")
    p_freq = adf(templates.freq.overlay(settings), p.molecule, job_name=name + "_p_freq")

# Prepare scan
    pes_jobs = []
    for d in range(8):
        consset = Settings()
        consset.constraint.update(bond1.get_settings(1.8 + d * 0.1))
        consset.constraint.update(bond2.get_settings(1.8 + d * 0.1))

        pes_name = name + "_pes_" + str(d)
        pes_dftb = dftb(templates.geometry.overlay(settings).overlay(consset), p_dftb.molecule, job_name=pes_name + "_DFTB")
        pes =      adf(templates.singlepoint.overlay(settings), pes_dftb.molecule, job_name=pes_name)
        pes_jobs.append(pes)

  # Get the result with the maximum energy
    apprTS = select_max(gather(*pes_jobs), 'energy')
  # Calculate the DFTB hessian
    DFTBfreq = dftb(templates.freq.overlay(settings), apprTS.molecule, job_name=name + "_freq_DFTB")
  # Run the TS optimization, using the initial hession from DFTB
    t = Settings()
    t.inithess = DFTBfreq.hessian
    TS = adf(templates.ts.overlay(settings).overlay(t), DFTBfreq.molecule, job_name=name + "_TS")
   
  # Perform a freq calculation
  #   freq_setting = Settings()
  #   freq_setting.specific.adf.geometry.frequencies = ""
  #   freq_setting.specific.adf.geometry.__block_replace = True
  #   TSfreq = adf(templates.geometry.overlay(settings).overlay(freq_setting), TS.molecule, job_name=name + "_freq")
    TSfreq = adf(templates.freq.overlay(settings), TS.molecule, job_name=name + "_freq")

  # Add the jobs to the job list
    job_list.append(gather(r1_freq, r2_freq, p_freq, TS, TSfreq))

# Finalize and draw workflow
wf = gather(*job_list)
#draw_workflow("wf.svg", wf._workflow)

# Actual execution of the jobs
results = run(wf, n_processes=1)

# Extract table from results
table = {}
for r1_result, r2_result, p_result, ts_opt, ts_result in results:
    if all( any(r.status == x for x in ['successful', 'copied']) for  r in [r1_result, r2_result, p_result, ts_opt, ts_result]):
        # Retrieve the molecular coordinates
        mol = ts_opt.molecule
        d1 = bond1.get_current_value(mol)
        d2 = bond2.get_current_value(mol)

        Eact = (ts_result.enthalpy - r1_result.enthalpy - r2_result.enthalpy) * hartree2kcal
        Ereact = (p_result.enthalpy - r1_result.enthalpy - r2_result.enthalpy) * hartree2kcal
        name = p_result.molecule.properties.name
        smiles = p_result.molecule.properties.smiles
        nimfreq = sum([f < 0 for f in ts_result.frequencies])
        table[name] = [smiles, Eact, Ereact, d1, d2, nimfreq, ts_opt.optcycles, ts_opt.runtime]

# Print table
print("Reaction Productsmiles    Eact  Ereact   Bond1   Bond2 NNegFreq TSoptCycles TSoptTime")
for name in sorted(table):
    print("{0:8s} {1:13s} {2:7.1f} {3:7.1f} {4:7.2f} {5:7.2f} {6:8d} {7:10d} {8:10.2f}".format(
        name, *table[name]))
