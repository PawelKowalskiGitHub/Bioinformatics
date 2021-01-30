from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from random_walk import RandomWalk
from points_io import save_points_as_pdb


def draw_graph():

    # creating objects
    polymer = RandomWalk(499,100) # 500 atoms (points) and radius of sampling limiting sphere equal to 10

    # drawing charts
    draw_polymer(polymer)

    # save points for the first simulation
    save_coordinates(polymer)


def draw_polymer(polymer):
    ax = draw()
    ax.plot(polymer.get_x_val(), polymer.get_y_val(), polymer.get_z_val(), color='blue', linewidth=3)
    ax.scatter((0),(0),(0),c="red")
    plt.savefig("polymer")
    plt.show()

def draw():
    # graph features
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return ax

def save_coordinates(sim, filename='polymer.pdb'):
    save_points_as_pdb(sim.coord, filename)

draw_graph()
