import numpy as np


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

	# return str(self.id) + ' (' + str(self.x) + ',' + str(self.y) + ')'

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


class Triangle():
	"""
	Triangle class hold triangle data
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

	def findInitial(self, pi, pf):
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
				list_of_tri.append(tri_next)
				break
			tri_next, tri_p_next = findNext(tri_next, pi, pf, tri_p_next)
			list_of_tri.append(tri_next)
		return list_of_tri

	def updateRestrictions(self, list_restriction):
		pass
