Chromatin is a linear polymer that takes on a specific spatial structure depending on the force system in which it is located. The adopted structure is critical to the biological function of the genome because, as is well known, genes close together are either all "on" or all "off" at the same time.

The main task of the project was to generate a globule (polymer) in 3D space, then to conduct energy minimization and molecular dynamics. The structure and process of globule formation in the defined force field were analyzed. In order to understand the influence of the interaction of the nearby chromatin regions (contacts), a comparison of the probabilities of contacts versus genomic distance from both simulationswas was performed. For the second simulation only, graphs of energy, radius of gyration and distance between ends versus time had to be created.


---File description---

The first file to execute is **random_walk.py**. This script allows us to generate a random-positioned polymer in 3D space. It is imposed that new points are generated at a distance greater than 1 A from any previously generated point and it does not allow the intersection of connections between the points. Contains the definition of the *RandomWalk* class, which is used in subsequent files. 
File **polymer.py** generates a random polymer with a given number of segments, uses the *RandomWalk* class, creates a **polymer.pdb** file and a PNG graphic file. 
File **polymer.pdb** - randomly generated globule, the basic structure used in the first and second simulations, has 500 atoms. 
The **points_io.py** file allows us to save files in the PDB format, which is necessary to simulate and visualize the structure of the generated polymer.





To execute scripts, you have to type "python3 <filename.py>" in the console.
