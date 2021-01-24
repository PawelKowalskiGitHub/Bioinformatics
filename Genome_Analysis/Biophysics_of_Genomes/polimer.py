from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from random_walk import RandomWalk
from points_io import save_points_as_pdb


def draw_graph():

    # creating objects
    sim_one = RandomWalk(499,10) # 500 atoms (points) and radius of sampling limiting sphere equal to 10


    # drawing charts
    draw_one(sim_one)


    # zapisanie punktow dla pierwszej symulacji
    save_coordinates(sim_one)





def draw_one(sim_one):
    ax = draw()
    ax.plot(sim_one.get_x_val(), sim_one.get_y_val(), sim_one.get_z_val(), color='blue', linewidth=3)
    ax.scatter((0),(0),(0),c="red")
#    plt.savefig("PK-sim0-1")
    plt.show()


def draw():
    # cechy wspolne rysunków
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return ax


def save_coordinates(sim, filename='polimer.pdb'):
    save_points_as_pdb(sim.coord, filename)

draw_graph()
