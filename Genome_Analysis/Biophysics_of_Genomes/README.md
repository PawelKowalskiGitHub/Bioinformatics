# ---Introduction---

Chromatin is a linear polymer that takes on a specific spatial structure depending on the force system in which it is located. The adopted structure is critical to the biological function of the genome because, as is well known, genes close together are either all "on" or all "off" at the same time.

The main task of the project was to generate a globule (polymer) in 3D space, then to conduct energy minimization and molecular dynamics. The structure and process of globule formation in the defined force field were analyzed. In order to understand the influence of the interaction of the nearby chromatin regions (contacts), a comparison of the probabilities of contacts versus genomic distance from both simulationswas was performed. For the second simulation only, graphs of energy, radius of gyration and distance between ends versus time had to be created.


# ---File description---

The first file to execute is **random_walk.py**. This script allows us to generate a random-positioned polymer in 3D space. It is imposed that new points are generated at a distance greater than 1 A from any previously generated point and it does not allow the intersection of connections between the points. Contains the definition of the *RandomWalk* class, which is used in subsequent files.\
File **polymer.py** generates a random polymer with a given number of segments, uses the *RandomWalk* class, creates a **polymer.pdb** file and a PNG graphic file.\
File **polymer.pdb** - randomly generated globule, the basic structure used in the first and second simulations, has 500 atoms.\ 
The **points_io.py** file allows us to save files in the PDB format, which is necessary to simulate and visualize the structure of the generated polymer.\
The simulations are carried out according to the defined system of forces, which is contained in **force_field.xml**. It contains a force field that determines the nature of the system, there is a harmonic bond and Lennard-Jones potential.\
**simulation_1.py** - the first simulation - energy minimization. An additional force was used here, which is defined by the function imposing a change of the globule conformation to a sphere with a given radius. The radius value I chose is 7 A. This script creates the **sim1.pdb** file.\
**sim1.pdb** - the globule was created as a result of the first simulation - energy minimization.\
**simulation2.py** - the second simulation, i.e. energy minimization and molecular dynamics. The script first performs an energy minimization and then writes the data needed for the molecular dynamics in **sym2_dyn.pdb** file. The potential energy is saved in a separate file **potencial_energy.txt**, which is then used to create (also by simulation_1.py) a potential energy graph as **potencial_energy(time).png**. Then, based on the saved file **sym2_dyn.pdb**, a graph of the distance between the ends **distance_between_ends(time).png** and the graph of the radius of gyration  **radius_of_gyration(time).png** are created.\
The data for the last simulation frame is also saved in the **sym2_last_frame.pdb** file needed for the file calculating the contact probability in **contacts.py**.
**contacts.py** - a file that calculates and draws a plot of the probability of contacts in a genomic function with fitting. Creates a **contacts.png** file.\
**bond_length.py** - file calculating the average distance between consecutive points (polymer atoms) and standard deviation. Creates a **bond_length.png** plot. Calculates values for the polymer.pdb file, thus for the basic structure. We can also use the sym2_last_frame.pdb file to calculate the values for the structure after the second simulation.


# ---Setup---

To execute scripts, you have to type "python3 <filename.py>" in a console.
