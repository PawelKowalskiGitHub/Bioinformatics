from points_io import point_reader
from math import sqrt
import matplotlib.pylab as plt

def distance(coord_from, coord_to):                         # function calculating the distance between points
	return sqrt((coord_from[0]-coord_to[0])**2 + (coord_from[1]-coord_to[1])**2 + (coord_from[2]-coord_to[2])**2)

points=point_reader("polymer.pdb")                          # load points from polymer.pdb

# calculate the distance between two consecutive points contained in the points list and returns a list of lengths
dists=[distance(point,points[counter+1]) for counter,point in enumerate(points[:-1],0)]


point_number=range(1,500)                                   # points on the x axis
mean=sum(dists)/len(dists)                                  # mean of length
variance=sum([(dist-mean)**2 for dist in dists])/len(dists) # variance
std=sqrt(variance)                                          # standard deviation
print("Average bond length = " , round(mean, 8))
print("Variance = " , round(variance, 8))
print("Standard deviation = " , round(std, 8))


plt.figure()
plt.plot(point_number,dists, "o", markersize=1.5)
#plt.xlim(100,120)
plt.ylim(0.998, 1.0025)
plt.errorbar(point_number, dists, yerr=std, linewidth=0.4, fmt='o', markersize=0.1, capsize=2.2, capthick=0.4)
plt.legend(("Mean of length","Standard deviation"))
table_vals=[['Average bond length',str(round(mean, 8))],['Standard deviation',str(round(std, 8))]]
the_table = plt.table(cellText=table_vals,
                  colWidths = [0.3]*3,
                  loc='lower right')
plt.xlabel("Bond number")
plt.ylabel("Length [A]")
plt.plot()
plt.savefig("bond_length.png")
plt.show()
print("bond_length.png saved...")
