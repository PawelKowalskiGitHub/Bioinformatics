from random_walk import RandomWalk
from points_io import point_reader
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt


def simulate():
    points_sym1 = RandomWalk(1)							# assign a RandomWalk class to the object
    points_sym2 = RandomWalk(1)
    points_sym1.coord = point_reader("sim1.pdb")		# loading data about coordinates of points for a given file (simulation)
    points_sym2.coord = point_reader("sim2_last_frame.pdb")

    # storing information about points and the number of contacts in dictionaries
    intersects_sym1 = {}
    intersects_sym2 = {}

    # storing informations about all possible contacts
    all_possible = {}  # one dictionary for both files

    # filling in the dictionary with information about the maximum number of contacts for a given genomic distance
    fill_intersect_all(all_possible)

    # filling dictionaries for simulation with zeros to get the appropriate structure of the dictionaries
    fill_zeros(intersects_sym1)
    fill_zeros(intersects_sym2)

    # calculate contacts
    contacts(points_sym1, intersects_sym1)
    contacts(points_sym2, intersects_sym2)

    # calculating the probability of contact and adding to the list
    probs = []  # list for probabilities (outputs of calc_prob function)
    probs.append(calc_prob(intersects_sym1, all_possible))
    probs.append(calc_prob(intersects_sym2, all_possible))

    # drawing a graph
    draw_multi(probs)


# function to counting contacts for each point, saves the outputs in a dictionary {genomic distance : number of contacts}
def contacts(sim, intersects):  							# sim - RandomWalk class object, intersects - dictionary for storing the number of contact
    for i in range(0, len(sim.coord) - 1):  				# for each point except the last one
        for j in range(i + 1, len(sim.coord)): 				# checking with the next point and each subsequent
            dist = sim.distance(sim.coord[i], sim.coord[j])	# using the distance method to calculate distances
            if dist < 2:  									# check if there is contact - distance less than 2
                intersects[j - i] += 1  					# counting

# function to filling a dictionary with zeros
def fill_zeros(val_dict):
    for i in range(1, 501):
        val_dict[i] = 0

# function to filling a dictionary with all possible contacts
def fill_intersect_all(val_dict):
    for i in range(1, 501):
        val_dict[i] = (501 - i) * 1

# function to calculate probability of contact
def calc_prob(intersects, all):
    prob = {}
    for i in range(1, 501):
        prob[i] = intersects[i] / all[i]  # number of contacts / number of possible contacts for a given distance
    return prob

# function to generate a graph with fitting function
def draw_multi(probs):
    plt.figure()
    plt.ylim(0.001, 5)
    plt.xscale("log")
    plt.yscale("log")
    plt.ylabel("Probability of contact")
    plt.xlabel("Genomic distance")
    plt.grid(True)
    for i in range(len(probs)):
        x = list(probs[i].keys())		# genomic distance
        y = list(probs[i].values())		# probability of contact
        def test_func(d, a, alpha):  # Fitting function; a and alpha are fit parameters
            return a * d ** alpha

        params, params_covariance = opt.curve_fit(test_func, x, y)  # opt.curve_fit returns two matrices with parameter values
        params2 = params[0]  # parameter value a
        params_covariance2 = params_covariance[1]  # parameter value alpha

        filenames = ['sim1.pdb', 'sim2_last_frame.pdb']
        print("The value of the parameter a for", filenames[i], " =", params2)
        print("The value of the parameter alpha for", filenames[i], " =", params_covariance2)
        plt.plot(x, y, label='Data')
        plt.plot(x, test_func(x, params[0], params[1]), '--', label='Fitted function')

    plt.legend(("sim1.pdb", "Fitting to sim1.pdb", "sim2_last_frame", "Fitting to sim2_last_frame"))
    plt.savefig("contacts.png")

print("contacts.png saved...")

simulate()

plt.show("contacts.png")