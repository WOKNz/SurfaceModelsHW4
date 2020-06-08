import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay

import Triangles

if __name__ == "__main__":
	# HW3
	points_np = np.genfromtxt('hw3data/data_small.xyz')  # (X,Y,Z)
	tri = Delaunay(points_np[:, 0:2])
	plt.triplot(points_np[:, 0], points_np[:, 1], tri.simplices, linewidth=0.25)
	# plt.plot(points_np[:, 0], points_np[:, 1], 'o', markersize=0.2)
	# plt.savefig('testset4_sci.png', dpi=600)
	trinagulation = Triangles.Triangulation(tri.simplices, points_np)
	plt.show()
