from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout

pdb = PDBFile('polymer.pdb')                # load a file with molecular topology
forcefield = ForceField('force_field.xml')    # load a force field

'''
The line below combinescombine the force field with the molecular topology loaded from the PDB file to create a complete mathematical description of the system we want to simulate. We have:
    - Nonbonded interactions beyond the cutoff distance are ignored (nonbondedMethod=CutoffNonPeriodic)
    - 1 nm cutoff for the direct space interactions (nonbondedCutoff=1*nanometer)
    - the length of all bonds that involve a hydrogen atom is not constrained (constraints=None)
'''
system = forcefield.createSystem(pdb.topology, nonbondedMethod=CutoffNonPeriodic, nonbondedCutoff=1*nanometer, constraints=None)

'''
CustomExternalForce applies a force to all of the particles in the system, where the potential energy is a mathematical expression of each particle’s (x, y, z) coordinates. 
The loop ensures that the function applies force to all atoms.
'''
force = CustomExternalForce('30000*max(0, r-0.7)^2; r=sqrt(x*x+y*y+z*z+0.001)') # r is the distance of the particle from the origin, measured in nm
system.addForce(force)
for i in range(system.getNumParticles()):
    force.addParticle(i, [])


'''
Integrator is used for advancing the equations of motion. It specifies a LangevinIntegrator, which performs Langevin dynamics, and assigns it to a variable called integrator. 
It also specifies the values of three parameters to Langevin dynamics: the simulation temperature, the friction coefficient, and the step size.
'''
integrator=LangevinIntegrator(300*kelvin, 0.5, 1.0*femtoseconds)
#platform = Platform.getPlatformByName('OpenCL')
simulation = Simulation(pdb.topology, system, integrator)   # combines the molecular topology, system, and integrator to begin a new simulation
simulation.context.setPositions(pdb.positions)              # specifies the initial atom positions for the simulation: in this case, the positions that were loaded from the PDB file.

print('Energy minimization...')
simulation.minimizeEnergy()                                 #  local energy minimization
simulation.step(10)

# save the result to a new PDB file
state = simulation.context.getState(getPositions=True)
out_file = open('sim1.pdb', 'w')
PDBFile.writeFile(pdb.topology, state.getPositions(), out_file)

print('sym1.pdb saved...')
