import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay


class Point():
	"""
	Point Obejct 3 dimensions and id
	"""

	def __init__(self, x, y, z, id=None):
		"""

		:param x: value x of the point
		:type x: float
		:param y:value y of the point
		:type y: float
		:param z:value z of the point
		:type z: float
		:param id: The id of a point
		:type id: str
		"""
		self.x = x
		self.y = y
		self.z = z
		self.id = id

	def __str__(self):
		if self.id is None:
			return '(' + str(self.x) + ',' + str(self.y) + ')'
		else:
			return str(self.id)

	@staticmethod
	def npArrayToListOfPoints(points):
		"""
		Convert ndarray to list of Points
		:param points: array of points (x,y,z)
		:type points:  ndarray
		:return: list of Point objects
		:rtype: list
		"""
		id_index = 0
		temp_list = []
		if points is None:
			return
		if points.shape[1] == 2:
			for row in range(points.shape[0]):
				temp_list.append(Point(points[row, 0], points[row, 1], None, str(id_index)))
				id_index = id_index + 1
		if points.shape[1] == 3:
			for row in range(points.shape[0]):
				temp_list.append(Point(points[row, 0], points[row, 1], points[row, 2], str(id_index)))
				id_index = id_index + 1
		return temp_list

	@staticmethod
	def listOfPointsToNp(l):
		"""Convert list of points to numpy array

		:param l: list of points
		:type l: list
		:return: numpy array
		:rtype: ndarray
		"""
		temp_list = []
		for point in l:
			temp_list.append([point.x, point.y, point.z])

		return np.array(temp_list)


class Triangle():
	"""	Triangle class hold triangle data

	"""

	def __init__(self, p1, p2, p3,
	             tri_in_front1=None, tri_in_front2=None, tri_in_front3=None,
	             p_in_front1=None, p_in_front2=None, p_in_front3=None, id=None):
		"""

		:param p1: Corner 1 of a triangle
		:type p1: Point
		:param p2: Corner 2 of a triangle
		:type p2: Point
		:param p3: Corner 3 of a triangle
		:type p3: Point
		:param tri_in_front1: Triangle that in front of p1
		:type tri_in_front1: Triangle
		:param tri_in_front2: Triangle that in front of p1
		:type tri_in_front2: Triangle
		:param tri_in_front3: Triangle that in front of p1
		:type tri_in_front3: Triangle
		:param id: Id of a triangle
		:type id: str
		"""
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3

		self.tri_in_front1 = tri_in_front1
		self.tri_in_front2 = tri_in_front2
		self.tri_in_front3 = tri_in_front3

		self.p_in_front1 = p_in_front1
		self.p_in_front2 = p_in_front2
		self.p_in_front3 = p_in_front3

		self.bq_params = None
		self.bl_params = None

		self.id = id

	def __str__(self):
		if self.id is None:
			return self.p1.__str__() + ',' + self.p2.__str__() + ',' + self.p3.__str__()
		else:
			return str(self.id) + \
			       ' (' + \
			       str(self.p1.id) + \
			       ',' + \
			       str(self.p2.id) + \
			       ',' + \
			       str(self.p3.id) + ']'

	def getPoints(self):
		return [self.p1, self.p2, self.p3]

class Triangulation():
	"""
	Triangulation class hold triangle data list
	"""

	def __init__(self, tri_corners, points):
		self.points_np = points
		self.points = []
		self.triangles = []
		for row in range(0, self.points_np.shape[0]):
			self.points.append(Point(self.points_np[row, 0],
			                         self.points_np[row, 1],
			                         self.points_np[row, 2],
			                         row))

		for row in range(0, tri_corners.shape[0]):
			self.triangles.append(Triangle(self.points[tri_corners[row, 0]],
			                               self.points[tri_corners[row, 1]],
			                               self.points[tri_corners[row, 2]]))
		for i in range(0, len(self.triangles)):
			tri = self.triangles.pop(i)
			for front in self.triangles:
				if self.isattached(tri, front):
					index = Triangulation.match(tri, front)
					Triangulation.setOposites(tri, front, index)
			self.triangles.insert(i, tri)

		print('pause')

	def __str__(self):
		if self.id is None:
			return self.p1.__str__() + ',' + self.p2.__str__() + ',' + self.p3.__str__()
		else:
			return str(self.id) + \
			       ' (' + \
			       str(self.p1.id) + \
			       ',' + \
			       str(self.p2.id) + \
			       ',' + \
			       str(self.p3.id) + ']'

	# def findPoints(self, searched):
	# 	found = []
	# 	for p_np in range(0,searched.shape[0]):
	# 		for

	@staticmethod
	def isattached(t, t_other):
		"""Cheking how many poins is the same between two triangles

		:param t: triangle 1
		:type t: Triangle
		:param t_other: triangle 2
		:type t_other: Triangle
		:return: returs id true if there is two points same
		:rtype: bool
		"""
		count = 0
		if (t.p1 is t_other.p1) or (t.p1 is t_other.p2) or (t.p1 is t_other.p3):
			count = count + 1
		if (t.p2 is t_other.p1) or (t.p2 is t_other.p2) or (t.p2 is t_other.p3):
			count = count + 1
		if (t.p3 is t_other.p1) or (t.p3 is t_other.p2) or (t.p3 is t_other.p3):
			count = count + 1
		if count == 0:
			return False
		elif count == 1:
			return False
		elif count == 2:
			return True
		else:
			print("Problem in isattached function")

	@staticmethod
	def match(t, t_other):
		"""Return list with matched indexes of points of two triangles

		:param t: triangle 1
		:type t: Triangle
		:param t_other: triangle 2
		:type t_other: Triangle
		:return: matched indexes
		:rtype: list
		"""
		temp = [0, 0]
		if (t.p1 is not t_other.p1) and (t.p1 is not t_other.p2) and \
				(t.p1 is not t_other.p3):
			temp[0] = 1
		elif (t.p2 is not t_other.p1) and (t.p2 is not t_other.p2) and \
				(t.p2 is not t_other.p3):
			temp[0] = 2
		elif (t.p3 is not t_other.p1) and (t.p3 is not t_other.p2) and \
				(t.p3 is not t_other.p3):
			temp[0] = 3

		if (t_other.p1 is not t.p1) and (t_other.p1 is not t.p2) and \
				(t_other.p1 is not t.p3):
			temp[1] = 1
		elif (t_other.p2 is not t.p1) and (t_other.p2 is not t.p2) and \
				(t_other.p2 is not t.p3):
			temp[1] = 2
		elif (t_other.p3 is not t.p1) and (t_other.p3 is not t.p2) and \
				(t_other.p3 is not t.p3):
			temp[1] = 3

		return temp

	@staticmethod
	def setOposites(tri, front, index):
		"""Updates the data of neighborhood triangles

		:param tri: triangle 1
		:type tri: Triangle
		:param front: triangle 2
		:type front: Triangle
		:param index: matched indexes
		:type index: list
		"""
		if index[0] == 1:
			if index[1] == 1:
				tri.tri_in_front1 = front
				tri.p_in_front1 = front.p1
			elif index[1] == 2:
				tri.tri_in_front1 = front
				tri.p_in_front1 = front.p2
			elif index[1] == 3:
				tri.tri_in_front1 = front
				tri.p_in_front1 = front.p3

		if index[0] == 2:
			if index[1] == 1:
				tri.tri_in_front2 = front
				tri.p_in_front2 = front.p1
			elif index[1] == 2:
				tri.tri_in_front2 = front
				tri.p_in_front2 = front.p2
			elif index[1] == 3:
				tri.tri_in_front2 = front
				tri.p_in_front2 = front.p3

		if index[0] == 3:
			if index[1] == 1:
				tri.tri_in_front3 = front
				tri.p_in_front3 = front.p1
			elif index[1] == 2:
				tri.tri_in_front3 = front
				tri.p_in_front3 = front.p2
			elif index[1] == 3:
				tri.tri_in_front3 = front
				tri.p_in_front3 = front.p3

	@staticmethod
	def ccw(pA, pB, pC):
		"""Checks if the pC is ccw with pA and pB

		:param pA: point 1
		:type pA: Point
		:param pB: point 2
		:type pB: Point
		:param pC: checked point
		:type pC: Point
		:return: true = pC is ccw to pA,pB line
		:rtype: bool
		"""
		temp_mat = np.array([[pA.x, pA.y, 1],
		                     [pB.x, pB.y, 1],
		                     [pC.x, pC.y, 1]])
		det = np.linalg.det(temp_mat)
		if det > 0:
			return True
		elif det == 0:
			print('all points on same line')
			return True
		else:
			return False

	def findInitial(self, pi, pf):
		"""Finds initial triangle on pi-pf direction

		:param pi: initial point
		:type pi: Point
		:param pf: final point
		:type pf: Point
		:return: Initial triangle of the chain towards pf
		:rtype: Triangle
		"""
		# Find all relevant triangles (initial)
		list_relevant_tri = []
		for tri in self.triangles:
			if (pi is tri.p1) or (pi is tri.p2) or (pi is tri.p3):
				list_relevant_tri.append(tri)

		# Select the initial
		list_relevant_tri2 = []
		for tri in list_relevant_tri:
			if pi is tri.p1:
				if self.ccw(pi, pf, tri.p2) * self.ccw(pi, pf, tri.p3) == 0 and \
						self.ccw(pi, pf, tri.p2) + self.ccw(pi, pf, tri.p3) == 1:
					list_relevant_tri2.append(tri)
			elif pi is tri.p2:
				if self.ccw(pi, pf, tri.p1) * self.ccw(pi, pf, tri.p3) == 0 and \
						self.ccw(pi, pf, tri.p1) + self.ccw(pi, pf, tri.p3) == 1:
					list_relevant_tri2.append(tri)
			elif pi is tri.p3:
				if self.ccw(pi, pf, tri.p1) * self.ccw(pi, pf, tri.p2) == 0 and \
						self.ccw(pi, pf, tri.p1) + self.ccw(pi, pf, tri.p2) == 1:
					list_relevant_tri2.append(tri)
			else:
				print('Problem in find Initial 1st for loop')

		for tri in list_relevant_tri2:
			if pi is tri.p1:
				if self.ccw(tri.p2, tri.p3, pi) * self.ccw(tri.p2, tri.p3, pf) == 0 and \
						self.ccw(tri.p2, tri.p3, pi) + self.ccw(tri.p2, tri.p3, pf) == 1:
					return tri
			if pi is tri.p2:
				if self.ccw(tri.p1, tri.p3, pi) * self.ccw(tri.p1, tri.p3, pf) == 0 and \
						self.ccw(tri.p1, tri.p3, pi) + self.ccw(tri.p1, tri.p3, pf) == 1:
					return tri
			if pi is tri.p3:
				if self.ccw(tri.p1, tri.p2, pi) * self.ccw(tri.p1, tri.p2, pf) == 0 and \
						self.ccw(tri.p1, tri.p2, pi) + self.ccw(tri.p1, tri.p2, pf) == 1:
					return tri

	def findAllTri(self, pi, pf):
		"""Finds all triangles that intesect with pi-pf line

		:param pi: initial point
		:type pi: Point
		:param pf: final point
		:type pf: Point
		:return: List of triangles that go from pi to pf
		:rtype: list
		"""
		tri_i = self.findInitial(pi, pf)
		tri_next = None
		tri_p_next = None
		list_of_tri = []
		list_of_tri.append(tri_i)

		def findNext(tri, pi, pf, p_in_front_of_prev):
			if tri.p1 is p_in_front_of_prev:
				if self.ccw(pi, pf, tri.p2) == self.ccw(pi, pf, tri.p1):
					return tri.tri_in_front2, tri.p_in_front2
				elif self.ccw(pi, pf, tri.p3) == self.ccw(pi, pf, tri.p1):
					return tri.tri_in_front3, tri.p_in_front3
			elif tri.p2 is p_in_front_of_prev:
				if self.ccw(pi, pf, tri.p1) == self.ccw(pi, pf, tri.p2):
					return tri.tri_in_front1, tri.p_in_front1
				elif self.ccw(pi, pf, tri.p3) == self.ccw(pi, pf, tri.p2):
					return tri.tri_in_front3, tri.p_in_front3
			elif tri.p3 is p_in_front_of_prev:
				if self.ccw(pi, pf, tri.p1) == self.ccw(pi, pf, tri.p3):
					return tri.tri_in_front1, tri.p_in_front1
				elif self.ccw(pi, pf, tri.p2) == self.ccw(pi, pf, tri.p3):
					return tri.tri_in_front2, tri.p_in_front2

		if pi is tri_i.p1:
			tri_next = tri_i.tri_in_front1
			tri_p_next = tri_i.p_in_front1
		elif pi is tri_i.p2:
			tri_next = tri_i.tri_in_front2
			tri_p_next = tri_i.p_in_front2
		elif pi is tri_i.p3:
			tri_next = tri_i.tri_in_front3
			tri_p_next = tri_i.p_in_front3
		else:
			print("problem in findAllTri")

		list_of_tri.append(tri_next)

		while True:
			if (tri_next.p1 is pf) or (tri_next.p3 is pf) or (tri_next.p3 is pf):
				break
			tri_next, tri_p_next = findNext(tri_next, pi, pf, tri_p_next)
			list_of_tri.append(tri_next)
		return list_of_tri

	def filterPoints(self, triangles, pi, pf):
		"""returns list of points without duplicates

		:param triangles: List of triangles that intersect with pi-pf
		:type triangles:
		:param pi: initial point
		:type pi: Point
		:param pf: final point
		:type pf: Point
		:return: list of points
		:rtype: list
		"""
		relevant_tri = triangles
		points_list = []
		for triangle in relevant_tri:
			points_list.extend(triangle.getPoints())

		clean_list = []

		def isInside(list, point):
			for object in list:
				if object is point:
					return True
			return False

		while len(points_list) > 0:
			p_temp = points_list.pop(0)
			if isInside(clean_list, p_temp) or (p_temp is pi) or (p_temp is pf):
				continue
			else:
				clean_list.append(p_temp)

		return clean_list

	def seperatePoints(self, points, pi, pf):
		"""Seperates list of points in two lists each on one side of pi-pf with the endings

		:param points: all poits that involved in new triangulation
		:type points:
		:param pi: initial point
		:type pi: Point
		:param pf: final point
		:type pf: Point
		:return: two list of points
		:rtype: list,list
		"""
		listA = []
		listB = []
		for point in points:
			if self.ccw(pi, pf, point):
				listA.append(point)
			else:
				listB.append(point)
		return listA, listB

	def indexArrays(self, points):
		"""Craetis array of index linking

		:param points: new list of points
		:type points: list
		:return: list of linked indexes
		:rtype: list
		"""
		match_indexes = []
		for point in points:
			match_indexes.append(point.id)
		return match_indexes

	def retun_Triangles_np(self):
		temp_np = np.zeros((len(self.triangles), 3), dtype=int)
		for i in range(len(self.triangles)):
			temp_np[i, :] = np.array([self.triangles[i].p1.id, self.triangles[i].p2.id, self.triangles[i].p3.id])
		return temp_np

	def updateRestrictions(self, list_restriction):
		if type(list_restriction[0]) is not list:
			list_restriction = [list_restriction]
		for segment in list_restriction:
			pi = self.points[int(segment[0])]
			pf = self.points[int(segment[1])]
			triangles = self.findAllTri(pi, pf)
			points = self.filterPoints(triangles, pi, pf)
			pointsA, pointsB = self.seperatePoints(points, pi, pf)

			pointsA.extend([pi, pf])
			pointsB.extend([pi, pf])

			matchA = self.indexArrays(pointsA)
			matchB = self.indexArrays(pointsB)

			triangA = Delaunay(Point.listOfPointsToNp(pointsA)[:, :2]).simplices
			triangB = Delaunay(Point.listOfPointsToNp(pointsB)[:, :2]).simplices

			self.plotDiagramm()
			print("Tri to remove:", len(triangles))
			print("Now list:", len(self.triangles))
			for tri in triangles:
				self.triangles.remove(tri)
			print("After list:", len(self.triangles))
			self.plotDiagramm()

			def creatTriangles(tri_corners, match):
				new_triangles = []
				for i in range(len(tri_corners)):
					for row in range(0, tri_corners[i].shape[0]):
						new_triangles.append(Triangle(self.points[match[i][tri_corners[i][row, 0]]],
						                              self.points[match[i][tri_corners[i][row, 1]]],
						                              self.points[match[i][tri_corners[i][row, 2]]]))
				return new_triangles

			def updateBiglist(new_triangles):
				origin_len = len(self.triangles)
				num_of_added = len(new_triangles)
				self.triangles.extend(new_triangles)

				for i in range(origin_len - 1, origin_len + num_of_added - 1):
					tri = self.triangles.pop(i)
					for front in self.triangles:
						if self.isattached(tri, front):
							index = Triangulation.match(tri, front)
							Triangulation.setOposites(tri, front, index)
					self.triangles.insert(i, tri)

			merged = [triangA, triangB]
			merged_index = [matchA, matchB]
			new_triangles = creatTriangles(merged, merged_index)
			updateBiglist(new_triangles)

			return self.retun_Triangles_np()

	def plotDiagramm(self, Name=None, unpad=None, limits=None):
		"""
		Plotting diagram of the triangles and points

		:param Name: Name of the file if you want to save the plot
		:type Name: str
		:param unpad: Padding to the triangles (seperates them) 0.2 is good
		:type unpad: float
		:param limits: Limits of the plot
		:type limits: list
		:rtype: None
		"""
		fig = plt.figure()

		def addRadilBias(triangle, unpad):
			tt = Triangle(triangle.p1, triangle.p2, triangle.p3)  # temp triangle
			x_avg = (tt.p1.x + tt.p2.x + tt.p3.x) / 3.0
			y_avg = (tt.p1.y + tt.p2.y + tt.p3.y) / 3.0
			p1_radial_angle = np.arctan2(y_avg - tt.p1.y, x_avg - tt.p1.x)
			p2_radial_angle = np.arctan2(y_avg - tt.p2.y, x_avg - tt.p2.x)
			p3_radial_angle = np.arctan2(y_avg - tt.p3.y, x_avg - tt.p3.x)
			tt.p1.x = tt.p1.x + np.cos(p1_radial_angle) * unpad
			tt.p1.y = tt.p1.y + np.sin(p1_radial_angle) * unpad
			tt.p2.x = tt.p2.x + np.cos(p2_radial_angle) * unpad
			tt.p2.y = tt.p2.y + np.sin(p2_radial_angle) * unpad
			tt.p3.x = tt.p3.x + np.cos(p3_radial_angle) * unpad
			tt.p3.y = tt.p3.y + np.sin(p3_radial_angle) * unpad
			return (x_avg, y_avg), tt

		if unpad is not None:
			for triangle in self.triangles:
				center, temp_tri = addRadilBias(triangle, unpad)
				plt.plot([temp_tri.p1.x, temp_tri.p2.x, temp_tri.p3.x, temp_tri.p1.x],
				         [temp_tri.p1.y, temp_tri.p2.y, temp_tri.p3.y, temp_tri.p1.y], linewidth=0.25)
				plt.text(center[0], center[1], triangle.id, fontsize=5)
				plt.axis('equal')
		else:
			for triangle in self.triangles:
				plt.plot([triangle.p1.x, triangle.p2.x, triangle.p3.x, triangle.p1.x],
				         [triangle.p1.y, triangle.p2.y, triangle.p3.y, triangle.p1.y], linewidth=0.25)
				plt.axis('equal')

		for point in self.points:
			plt.scatter(point.x, point.y, color='red', s=0.2)
		# plt.text(point.x, point.y, point.id, fontsize=9)
		if Name is not None:
			plt.savefig(Name, dpi=600)
		if limits is not None:
			plt.xlim(right=limits[0])  # xmax is your value
			plt.xlim(left=limits[1])  # xmin is your value
			plt.ylim(top=limits[2])  # ymax is your value
			plt.ylim(bottom=limits[3])  # ymin is your value
		fig.show()

	def convexPoints(self):
		relevant_triangles = []
		for triangle in self.triangles:
			if triangle.tri_in_front1 is None or triangle.tri_in_front2 is None or triangle.tri_in_front3 is None:
				relevant_triangles.append(triangle)
		relevant_points = []
		for triangle in relevant_triangles:
			if triangle.tri_in_front1 is None:
				relevant_points.append(triangle.p2)
				relevant_points.append(triangle.p3)
			elif triangle.tri_in_front2 is None:
				relevant_points.append(triangle.p1)
				relevant_points.append(triangle.p3)
			else:
				relevant_points.append(triangle.p2)
				relevant_points.append(triangle.p1)

		return Point.listOfPointsToNp(relevant_points)

	def interpolate(self):
		for triangle in self.triangles:
			self.calculateSurface(triangle)

	@staticmethod
	def isInsideTriangle(point, triangle):
		"""
		Cheking if the point is inside the triangle

		:param point: checked point
		:type point: Point
		:param triangle: checked triangle
		:type triangle: Triangle
		:return: True = inside
		:rtype: bool
		"""

		def ccw(pA, pB, pC):  # Repeated code
			temp_mat = np.array([[pA.x, pA.y, 1],
			                     [pB.x, pB.y, 1],
			                     [pC.x, pC.y, 1]])
			det = np.linalg.det(temp_mat)
			if det > 0:
				return True
			elif det == 0:
				print('all points on same line')
				return True
			else:
				return False

		if (ccw(triangle.p1, triangle.p2, point) and \
		    ccw(triangle.p2, triangle.p3, point) and \
		    ccw(triangle.p3, triangle.p1, point)) or \
				(not ccw(triangle.p1, triangle.p2, point) and \
				 not ccw(triangle.p2, triangle.p3, point) and \
				 not ccw(triangle.p3, triangle.p1, point)):
			return True
		else:
			return False

	def inWhichTriangle(self, point):
		"""
		Going over the list of triangle and checking if the point is inside

		:param point: checked point
		:type point: Point
		:return: relevant triangle
		:rtype: Triangle
		"""
		for triangle in self.triangles:
			if Triangulation.isInsideTriangle(point, triangle):
				return triangle

	def newHight(self, point):
		triangle = self.inWhichTriangle(point)
		if triangle is None:
			print('Points is outside the triangulation')
		return self.calculateHight(triangle, point)

	@staticmethod
	def calculateHight(triangle, new_point):
		np = new_point
		if triangle.bq_params is None:
			p = triangle.bl_params
			return p[0] + np.x * p[1] + np.y * p[2]
		else:
			p = triangle.bq_params
			return p[0] + np.x * p[1] + np.y * p[2] + (np.x) ** 2 * p[3] + np.x * np.y * p[4] + (np.y) ** 2 * p[5]

	@staticmethod
	def calculateSurface(triangle):
		if triangle.tri_in_front1 is None or triangle.tri_in_front2 is None or triangle.tri_in_front3 is None:
			points = Point.listOfPointsToNp([triangle.p1, triangle.p2, triangle.p3])
			row1 = np.ones((1, 3))[0, :]
			row2 = points[:, 0]
			row3 = points[:, 1]
			b = points[:, 2]

			A = np.vstack((row1, row2, row3)).T
			x = np.dot(np.linalg.inv(A), b.reshape((3, 1)))
			triangle.bl_params = x.T.tolist()[0]

		else:
			points = Point.listOfPointsToNp([triangle.p_in_front1, triangle.p_in_front2, triangle.p_in_front3,
			                                 triangle.p1, triangle.p2, triangle.p3])
			row1 = np.ones((1, 6))[0, :]
			row2 = points[:, 0]
			row3 = points[:, 1]
			row4 = np.multiply(row2, row2)
			row5 = np.multiply(row2, row3)
			row6 = np.multiply(row3, row3)
			b = points[:, 2]

			A = np.vstack((row1, row2, row3, row4, row5, row6)).T
			x = np.dot(np.linalg.inv(A), b.reshape((6, 1)))
			triangle.bq_params = x.T.tolist()[0]
