import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay

import Triangles

if __name__ == "__main__":
	# HW4
	# IMport Points
	points_np = np.genfromtxt('hw3data/data_small.xyz')  # (X,Y,Z)
	# Scipi triangulation
	tri = Delaunay(points_np[:, 0:2])
	# Plot Scipy Result
	plt.triplot(points_np[:, 0], points_np[:, 1], tri.simplices, linewidth=0.25)
	# plt.plot(points_np[:, 0], points_np[:, 1], 'o', markersize=0.2)
	# plt.savefig('testset4_sci.png', dpi=600)
	# Triangulation object initialization
	trinagulation = Triangles.Triangulation(tri.simplices, points_np)
	convex = trinagulation.convexPoints()
	trinagulation.interpolate()
	new_point_hight_bq = trinagulation.newHight(Triangles.Point(10, 80, None))
	new_point_hight_bl = trinagulation.newHight(Triangles.Point(11.0, 120.0, None))
	print([[10, 80, np.round(new_point_hight_bq, 3)],
	       [11.0, 120.0, np.round(new_point_hight_bl, 3)]])
	restrictions = np.genfromtxt('hw3data/constrains.txt', delimiter=",")
	points_np_my = trinagulation.updateRestrictions(restrictions.tolist())
	plt.axis('equal')
	plt.show()

	for i in range(0, convex.shape[0], 2):
		plt.plot(convex[i:i + 2, 0], convex[i:i + 2, 1], 'bo-')

	plt.axis('equal')
	plt.show()

	# plt.triplot(points_np[:, 0], points_np[:, 1], points_np_my, linewidth=0.25)
	trinagulation.plotDiagramm()
