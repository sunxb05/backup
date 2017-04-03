import sys
from scm.plams import *
init()


# Create the molecule:
mol = Molecule()
mol.add_atom(Atom(symbol='O', coords=(0,0,0)))
mol.add_atom(Atom(symbol='H', coords=(1,0,0)))
mol.add_atom(Atom(symbol='H', coords=(0,1,0)))

complexList = []
complexList.append(Molecule())
complexList.add_atom(mol)
for i in complexList:
    print(i)
print(complexList)

sys.exit()


# Initialize the settings for the ADF calculation:
sett = Settings()
sett.input.basis.type = 'DZ'
sett.input.basis.core = 'None'
sett.input.NumericalQuality = 'Basic'
sett.input.XC.GGA = 'PBE'
sett.input.geometry
print(sett) 

# Create and run the job:
job = ADFJob(molecule=mol, settings=sett, name='water_GO')
job.run()

# Fetch and print some results:
energy = job.results.readkf('Energy', 'Bond Energy')
opt_mol = job.results.get_molecule('Geometry', 'xyz')
bond_angle = opt_mol.atoms[0].angle(opt_mol.atoms[1], opt_mol.atoms[2])

print ('== Water optimization Results ==')
print ('Bonding energy: %f kcal/mol' % Units.convert(energy, 'au', 'kcal/mol'))
print ('Bond angle: %f degree' % Units.convert(bond_angle, 'rad', 'degree'))
