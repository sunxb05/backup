#Common input options for all ADF runs
common = Settings()
common.input.Basis.Type = 'DZ'
common.input.Basis.Core = 'None'
common.input.Symmetry = 'NOSYM'
common.input.XC.GGA = 'PBE'


#################### GEOMETRY PREPARATION #################################

#Read substrate and product geometries
substrate = Molecule('substrate.xyz')
product = Molecule('product.xyz')

#Calculate linear transit constraints. This part is highly dependent on the system used and needs to be adjusted for each substrate-product pair independently. In our case we study simple Diels-Alder reaction (ethene + 1,3-butadiene) and use the distance between ethene carbon and butadiene terminal carbon as constraint.

atom_numbers = [(1,11), (4,12)] #list of atom pairs that form constraints (note: atom orderings in product and substrate must be the same). Linear transit will follow both atom-atom distances proportionally. More/less atom pairs can be supplied here. Also, this part of the script can be modified to use angles/dihedrals


constr = []
for at1, at2 in atom_numbers:
    start = substrate[at1].distance_to(substrate[at2])
    end = product[at1].distance_to(product[at2])
    constr.append('%i %i start=%f end=%f' % (at1, at2, start, end))


frag1_atoms = {1,2,3,4,5,6,7,8,9,10} # list of atoms belonging to fragment1. All other atoms are fragment2
frag2_atoms = {i for i in range(1, len(substrate)+1) if i not in frag1_atoms}


#################### ADF Fragment Job definition ############################
#this can be removed in future, since ADFFragmentJob is going to be soon included in PLAMS by default


class ADFFragmentResults(Results):
    def get_energy_decomposition(self, unit='au'):
        return self.job.full.results.get_energy_decomposition(unit)


class ADFFragmentJob(MultiJob):
    _result_type = ADFFragmentResults

    def __init__(self, fragment1=None, fragment2=None, name1='frag1', name2='frag2', **kwargs):
        MultiJob.__init__(self, **kwargs)
        self.fragment1 = fragment1.copy() if isinstance(fragment1, Molecule) else fragment1
        self.fragment2 = fragment2.copy() if isinstance(fragment2, Molecule) else fragment2
        self.name1 = name1
        self.name2 = name2

    def prerun(self):
        self.f1 = ADFJob(name=self.name+'_f1', molecule=self.fragment1, settings=self.settings)
        self.f2 = ADFJob(name=self.name+'_f2', molecule=self.fragment2, settings=self.settings)

        for at in self.fragment1:
            at.properties.adf.fragment = self.name1
        for at in self.fragment2:
            at.properties.adf.fragment = self.name2

        self.full = ADFJob(name=self.name+'_all', molecule=self.fragment1+self.fragment2, settings=self.settings)
        self.full.settings.input.fragments[self.name1] = self.f1
        self.full.settings.input.fragments[self.name2] = self.f2

        self.children = [self.f1, self.f2, self.full]



#################### LINEAR TRANSIT #######################################

#Create linear transit job and adjust all the specific settings
LT = ADFJob(molecule=substrate, name='linear_transit', settings=common)
LT.settings.input.geometry.transit = 15
LT.settings.input.constraints.dist = constr
LT_results = LT.run()

#Get energies of all linear transit points, choose the highest energy and obtain geometry associated with it
LT_energies = LT_results.readkf('LT', 'Energies')
max_en_index = LT_energies.index(max(LT_energies))
LT_best_geometry = LT_results.get_molecule('LT', 'xyz', n=max_en_index+1)



#################### FREQUENCIES 1 ########################################

#Create frequencies run for highest energy geometry from linear transit. This job will serve as a "restart point" for transition state search, effectively supplying good guess for initial Hessian
Freq_1 = ADFJob(molecule=LT_best_geometry, name='frequencies_1', settings=common)
Freq_1.settings.input.geometry.frequencies = True
Freq_1.run()



#################### TRANSITION STATE SEARCH ##############################

#Create transition state search job using best geometry from linear transit and Hessian from frequencies job
TS = ADFJob(molecule=LT_best_geometry, name='transition_state', settings=common)
TS.settings.input.geometry.transitionstate = True
TS.settings.input.restart = Freq_1
TS_results = TS.run()
TS_molecule = TS_results.get_molecule('Geometry', 'xyz', internal=True)



#################### FREQUENCIES 2 ########################################

#Create frequencies run for transition state geometry. The goal of this job is to verify if the given geometry is indeed a transition state by looking at the number of imaginary frequencies

Freq_2  = ADFJob(molecule=TS_molecule, name='frequencies_2', settings=Freq_1)
Freq_2.settings.input.restart = TS
Freq_2_results = Freq_2.run()

freqs = Freq_2_results.readkf('Freq', 'Frequencies')
no_im_freqs = len([i for i in freqs if i < 0])
if no_im_freqs != 1:
    raise Exception('ERROR! %i imaginary frequencies found' % no_im_freqs)



#################### INTRINSIC REACTION COORDINATE ########################

#Intrinsic Reaction Coordinate calculation starts from transition state geometry and uses Hessian from Frequencies 2.

IRC = ADFJob(molecule=TS_molecule, name='irc', settings=common)
IRC.settings.input.geometry.IRC = True
IRC.settings.input.restart = TS
IRC_results = IRC.run()

#Extract geometries of each point of reaction path. Forward and backward path are stored separately. Combine them, together with transition state, into full reaction path.
fw_len = IRC_results.readkf('IRC_Forward','CurrentPoint')
forward = [IRC_results.get_molecule('IRC_Forward', 'xyz', n=i+1) for i in range(fw_len)]
bw_len = IRC_results.readkf('IRC_Backward','CurrentPoint')
backward = [IRC_results.get_molecule('IRC_Backward', 'xyz', n=i+1) for i in range(bw_len)]
fullpath = list(reversed(backward)) + [TS_molecule] + forward



#################### HIGH ACCURACY SINGLE POINT ###########################

#Create higher accuracy fragment jobs for each reaction path geometry.

SP_jobs = []
for mol in fullpath:
    fragmol1 = mol.copy(atoms=[mol[i] for i in frag1_atoms])
    fragmol2 = mol.copy(atoms=[mol[i] for i in frag2_atoms])
    newjob = ADFFragmentJob(fragment1=fragmol1, fragment2=fragmol2, name='fragment', settings=common)
    newjob.settings.input.Basis.Type = 'TZP' #overrides the default defined in 'common'
    newjob.settings.input.NumericalQuality = 'Good'
    SP_jobs.append(newjob)

SP_results = [j.run() for j in SP_jobs]
en_decomp = [r.get_energy_decomposition(unit='kcal/mol') for r in SP_results]

final_results = {}
for key in en_decomp[0]:
    final_results[key] = [d[key] for d in en_decomp]

print(final_results)




