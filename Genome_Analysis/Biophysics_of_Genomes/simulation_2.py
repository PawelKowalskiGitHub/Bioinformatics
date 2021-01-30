from __future__ import print_function
from simtk.openmm import app
import simtk.openmm as mm
import simtk.unit as unitt
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout
import matplotlib.pyplot as plt
import numpy as np
import mdtraj as md
from math import sqrt
from scipy.ndimage.measurements import center_of_mass


pdb = app.PDBFile('polymer.pdb')			# load a file with molecular topology
forcefield = ForceField('force_field.xml')	# load a force field


system = forcefield.createSystem(pdb.topology, nonbondedMethod=CutoffNonPeriodic, nonbondedCutoff=1*nanometer, constraints=None)

# system = forcefield.createSystem(pdb.topology, nonbondedMethod=PME, nonbondedCutoff=1*nanometer, ewaldErrorTolerance=0.00001, vdwCutoff=1.2*nanometer)


integrator = LangevinIntegrator(310*kelvin, 0.5, 1.0*femtoseconds)

simulation = app.Simulation(pdb.topology, system, integrator)
simulation.context.setPositions(pdb.positions)

print('Energy minimization...')
simulation.minimizeEnergy()

simulation.reporters.append(StateDataReporter('potencial_energy.txt', 500, potentialEnergy=True))

simulation.context.setVelocitiesToTemperature(310*kelvin)
simulation.step(100)

# saving pdb file after energy minimization
#simulation.reporters.append(app.PDBReporter('sym2_mini.pdb', 1000))
#print('sym2_mini.pdb saved...')


print('Molecular dynamics...')
simulation.reporters.append(PDBReporter('sim2_dyn.pdb', 20))	# save the result to a new PDB file
simulation.reporters.append(StateDataReporter(stdout, 1000, step=True, potentialEnergy=True, temperature=True))
simulation.step(20000)
print('sim2_dyn.pdb saved...')

# save the coordinates of the last simulation frame to a new PDB file
state = simulation.context.getState(getPositions=True)
out_file = open('sim2_last_frame.pdb', 'w')
PDBFile.writeFile(pdb.topology, state.getPositions(), out_file)
print('sim2_last_frame.pdb saved...')


# Generating graphs
print('Generating graphs...')
# Graph: Potential energy - time
print("Graph: Potential energy - time")
x=[]
y=[]
file = open("potencial_energy.txt","r")
lines = file.readlines()
step = 1
for line in lines[1:]:
	x.append(step*500)
	step += 1
	y.append(float(line[:-2]))

plot = plt.plot(x, y, c='r')
plt.xlabel("Time [fs]")
plt.xticks(rotation='horizontal')
plt.ylabel("Potential energy [kJ/mol]")
plt.grid(True)
plt.savefig("potential_energy(time).png")
plt.show()
print("potential_energy(time).png saved...")


# Graph: Distance distance between ends - time
print("Graph: Distance distance between ends - time")

t = md.load('sim2_dyn.pdb')

def distance(coord_from, coord_to):					# distance calculating function
	return sqrt((coord_from[0]-coord_to[0])**2 + (coord_from[1]-coord_to[1])**2 +(coord_from[2]-coord_to[2])**2)

firsts = [list(t.xyz[n][0]) for n in range(1000)]	# list of lists with coordinates of the first end in each simulation frame
lasts = [list(t.xyz[n][499]) for n in range(1000)]	# list of lists with coordinates of the second end in each simulation frame
for n in range(1000):								# multiplication of each coordinate x 10,
	for m in range(3): 								# because mdtraj reads the values as 10 times smaller
		firsts[n][m] *= 10
		lasts[n][m] *= 10
dists = [distance(lasts[n],firsts[n]) for n in range(1000)] # distances between the first and second end in a given simulation frame
times = [20*n for n in range(1000)] # saving the simulation time; simulation duration: 20000, number of simulation frames: 1000

'''
# Alternatively
t = md.load('sim2_dyn.pdb')
dists = []
for i in range(1000): # frame number
    coord_from = list(t.xyz[i, 0,:])
    coord_to = list(t.xyz[i, 499,:])
    d = sqrt((coord_from[0]-coord_to[0])**2 + (coord_from[1]-coord_to[1])**2 +(coord_from[2]-coord_to[2])**2)
    dists.append(d)
times = [20*n for n in range(1000)]
'''

plt.plot(times,dists) 
plt.xlabel("Time [fs]")
plt.xticks(rotation='horizontal')
plt.ylabel("Distance between ends  [A]")
plt.savefig("distance_between_ends(time).png")
plt.show()
print("distance_between_ends(time).png saved...")


# Graph: Radius of gyration - time
print("Graph: Radius of gyration - time")

t = md.load('sim2_dyn.pdb')
coors = t.xyz	# loading the coordinates as a matrices of lists. 1000 matrices, 500 lists with coordinates in each matrix

# compute the geometric center of the structure in each simulation frame
centers = []	# a list of lists containing the geometric centers in each simulation frame
for n in range(1000):					# for each simulation frame
	avg = [0,0,0] 						# average values for x, y, z
	for m in range(500): 				# for each point
		for l in range(3):				# x, y, z
			avg[l] += coors[n][m][l]*10 # adding up coordinates
	for l in range(3):
		avg[l] /= 500 					# division to get average values
	centers.append(avg) 				# geometric center

# Radius of gyration
# gr = sqrt((1/N)*(sum(r_k - r_avg)) --> Radius of gyration is the root of the mean of the sum of the squares of the differences of the distance of the k-th atom from the geometric center from the mean distance from the geometric center. I think, it's clear.
rgs = [] 							# list of radius of gyration
for frame_idx in range(1000): 		# 1000 simulation frames
	distances = [] 					# list of distance to geometric center for each point
	geo_cent = centers[frame_idx] 	# geometric center for a relevant frame
	avg_r, square, sum_of_squares, rg = 0, 0, 0, 0 # variables
	for point in range(500):
		coord_from = np.array(t.xyz[frame_idx, point,:])*10
		dist = sqrt((coord_from[0]-geo_cent[0])**2 + (coord_from[1]-geo_cent[1])**2 +(coord_from[2]-geo_cent[2])**2)
		distances.append(dist)
	r_avg = sum(distances) / 500
	for r_k in range(len(distances)):
		square = (distances[r_k] - r_avg)**2
		sum_of_squares += square
	rg = sqrt(sum_of_squares / 500)
	rgs.append(rg)

times=[20*n for n in range(1000)] 	# saving the simulation time; simulation duration: 20000, number of simulation frames: 1000

plt.plot(times,rgs)
plt.xlabel("Time [fs]")
plt.xticks(rotation='horizontal')
plt.ylabel("Radius of gyration [A]")
plt.savefig("radius_of_gyration(time).png")
print("radius_of_gyration(time).png saved...")
plt.show()