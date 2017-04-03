from qmworks import Settings, templates, run, molkit
from noodles import gather
from qmworks.packages.SCM import dftb, adf, pyfrag
from qmworks.components import Distance, select_max
from qmworks.packages.PyFragModules import GetFragmentList
import plams


ircCoordfile ="/scistor/tc/xsn800/escience/py_1/mole.xyz"
fragDefinitions = [{'frag1': [2], 'frag2': [1, 3, 4, 5, 6]}, {'frag1': [2], 'frag2': [1, 3, 4, 5, 6]}]
bondDefinitions = [{'bond1': Distance(2, 1) , 'bond2': Distance(2, 6)}, {'bond1': Distance(2, 1) , 'bond2': Distance(2, 6)}]
inputkeys = [ {'fragment': [[2], [1, 3, 4, 5, 6]],  'strain': [[1.0], [2.0]]}, {'fragment': [[2], [1, 3, 4, 5, 6]],  'strain': [[1.0], [2.0]]}]

# User define Settings
settings = Settings()
settings.functional = "opbe"
settings.basis = "TZP"
settings.specific.dftb.dftb.scc.ndiis = 4
settings.specific.dftb.dftb.scc.Mixing = 0.1
settings.specific.dftb.dftb.scc.iterations = 300

job_list = []

for ircIndex, ircFrags in enumerate(GetFragmentList(ircCoordfile, fragDefinitions)):
   ircTag  = str(ircIndex+1).zfill(3)
   name  =  ircTag
   r1_mol = ircFrags['frag1']
   r2_mol = ircFrags['frag2']
   p_mol = ircFrags['complex']
   bond1 = bondDefinitions[ircIndex]['bond1']
   bond2 = bondDefinitions[ircIndex]['bond2']

  # Prepare reactant1 job
   r1_dftb = dftb(templates.geometry.overlay(settings), r1_mol, job_name=name + "_r1_DFTB")
   r1 =      adf(templates.geometry.overlay(settings), r1_dftb.molecule, job_name=name + "_r1")
   r1_freq = adf(templates.freq.overlay(settings), r1.molecule, job_name=name + "_r1_freq")

  # Prepare reactant2 job
   r2_dftb = dftb(templates.geometry.overlay(settings), r2_mol, job_name=name + "_r2_DFTB")
   r2 =      adf(templates.geometry.overlay(settings), r2_dftb.molecule, job_name=name + "_r2")
   r2_freq = adf(templates.freq.overlay(settings), r2.molecule, job_name=name + "_r2_freq")
# repare product job
   p_mol.properties.name = name
   p_dftb = dftb(templates.geometry.overlay(settings), p_mol, job_name=name + "_p_DFTB")
   p =      adf(templates.geometry.overlay(settings), p_dftb.molecule, job_name=name + "_p")
   p_freq = adf(templates.freq.overlay(settings), p.molecule, job_name=name + "_p_freq")

# Prepare scan
   pes_jobs = []
   for d in range(8):
      consset = Settings()
      consset.constraint.update(bond1.get_settings(2 + d * 0.1))
      consset.constraint.update(bond2.get_settings(1.52 + d * 0.1))

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
   TSfreq = adf(templates.freq.overlay(settings), TS.molecule, job_name=name + "_freq")
   irc = adf(templates.irc.overlay(settings), TS.molecule, job_name=name + "_irc")
   pyfrag = pyfrag(templates.frag.overlay(settings), settings_2 = templates.fa.overlay(settings), inputArgues= irc.kf.path, other = inputkeys[ircIndex],  job_name=name + "_pyfrag" )
 # Add the jobs to the job list
   job_list.append(gather(r1_freq, r2_freq, p_freq, TS, TSfreq, irc, pyfrag))

# Finalize and draw workflow
wf = gather(*job_list)
#draw_workflow("wf.svg", wf._workflow)

# Actual execution of the jobs
results = run(wf, n_processes=4)
