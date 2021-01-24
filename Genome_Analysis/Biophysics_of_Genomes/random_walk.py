from random import uniform, choice
from math import sqrt


class RandomWalk:

	def __init__(self, num_points, radius=-1):

		self.coord = [(0, 0, 0)]		# list of tuples with atoms (points) coordinates
		self.current_points = 0 		# number of atoms (points) coordinates in coord list
		self.num_points = num_points	# number of atoms (points) we want to generated - this is the length of our polymer
		self.radius = radius			# radius of the sphere that limits the sampling space

		self.fill_walk()

	# A function that generates the coordinates of a new point provided that 3 conditions are met:
	# (A) the new point is not closer than 1 to any other point
	# (B) a sphere limits the sampling space (it may not be taken into account - if the parameter is not given when calling the function)
	# (C) The new point will not coincide with any other point on the coord list
	def fill_walk(self):

		while self.current_points < self.num_points:
			too_close = 1					# to_close variable informs whether the new-generated point is too close to any other point. 0 - appropriate distance, 1 - inappropriate distance
			next_x,next_y,next_z = 0,0,0 	# initial coordinate values of the new point

			# loop generates a new point until it satisfies all three conditions A, B, C
			while too_close==1 or (sqrt(next_x**2 + next_y**2 + next_z**2) >= self.radius and self.radius>0) or (next_x, next_y, next_z) in self.coord:
				x_step = uniform(-1, 1)
				y_step = uniform(-1, 1)
				z_step = uniform(-1, 1)

				# temporary coordinate values of the new point
				next_x, next_y, next_z = self.next_val(x_step, y_step, z_step)

				# normalize, to make segment length (distance between the new point and the last point in coord list) equal to 1
				dist = self.distance((next_x, next_y, next_z), self.coord[-1])
				x_step /= dist
				y_step /= dist
				z_step /= dist

				# final coordinates of the new point
				next_x, next_y, next_z = self.next_val(x_step, y_step, z_step)

				# checks that the new point is not closer than 1 to any existing point in the coord list
				too_close=0
				for x,y,z in self.coord:
					if self.distance2(next_x, next_y, next_z, x, y, z)<1:
						too_close=1
						break

			# adds the coordinates of a new point to the coord list
			self.coord.append((next_x, next_y, next_z))

			self.current_points += 1


	# function for calculating segment length (distance between last point in coord and new-generated point)
	def distance(self, coord_from, coord_to):
		return sqrt((coord_from[0]-coord_to[0])**2 + (coord_from[1]-coord_to[1])**2 +
					(coord_from[2]-coord_to[2])**2)

	# function for calculating distance between two points based on 6 arguments - x, y, z coordinates, from both points
	def distance2(self, x1, y1, z1, x2, y2, z2):
		roz_z = z1 - z2 
		roz_y = y1 - y2
		roz_x = x1 - x2
		return sqrt(roz_x * roz_x + roz_y * roz_y + roz_z * roz_z)

	# function for adding randomly generated new point values to the value of the last point included in coord
	def next_val(self, x_step, y_step, z_step):
		next_x = self.coord[-1][0] + x_step
		next_y = self.coord[-1][1] + y_step
		next_z = self.coord[-1][2] + z_step
		return next_x, next_y, next_z


	def get_x_val(self):
		return [x[0] for x in self.coord]

	def get_y_val(self):
		return [y[1] for y in self.coord]

	def get_z_val(self):
		return [z[2] for z in self.coord]

