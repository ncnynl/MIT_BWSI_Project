# from algorithm import algorithm
# from ..profile import Profile
from .node import Node
from itertools import product
import numpy as np

class Graph:
	def __init__(self, profiles):
		"""
		This initializes a list of nodes when a list of profiles is passed towards me
		"""
		self.nodes = []
		for i, profile in enumerate(profiles):
			uniNode = Node(i, {}, profile, truth = profile.name)
			self.nodes.append(uniNode)
		self.computeDistances()

	def __repr__(self):
		return "{}".format(self.nodes) 

	def computeDistances(self):
		#add to list if weight is < 0.45
		for i, node1 in enumerate(self.nodes):
			for j, node2 in enumerate(self.nodes):
				if (i == j):
					continue

				distance = np.linalg.norm(node1.data.descr - node2.data.descr)
				# print("{} {} {}".format(node1, node2, distance))
				if (distance < 0.7):
					node1.neighbors[node2] = 1 / distance ** 2
					node2.neighbors[node1] = 1 / distance ** 2












