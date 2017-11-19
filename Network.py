import networkx as nx
import matplotlib.pyplot as plt

import random

class Network():
	def __init__(self, nodes, max_weight):
		print("Network created.")
		self.graph = self.generate_random_network(nodes, nodes * 2, max_weight)

	def generate_random_network(self, nodes, edges, max_weight):
		#Generates random network, can be changed to specific networks if need be
		G = nx.dense_gnm_random_graph(nodes, edges)
		for (u, v) in G.edges():
				rand = random.randint(0, max_weight)
				G[u][v]['weight'] = rand

		return G

	def draw_network(self):
		nx.draw_networkx(self.graph)
		plt.draw()
		plt.show()
