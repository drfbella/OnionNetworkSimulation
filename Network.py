import networkx as nx
import matplotlib.pyplot as plt
import random

class Network():
	def __init__(self, nodes, max_weight):
		print("Network created.")
		self.ip_pool = list()
		self.base_cost = 1
		self.graph = self.generate_tiered_network(3, 3, 3, 3, 5)
		

	def generate_random_network(self, nodes, edges, max_weight):
		#Generates random network, can be changed to specific networks if need be
		G = nx.dense_gnm_random_graph(nodes, edges)
		for (u, v) in G.edges():
				rand = random.randint(0, max_weight)
				G[u][v]['weight'] = rand

		return G

	def generate_tiered_network(self, top_tier, mid_tier, low_tier, end_systems, max_weight):
		network = nx.Graph()

		#Create the top-tier network
		top_tier_net = []

		for net in range(1, top_tier+1):
			ip = self.allocate_ip(("*", 0, 0, 0))
			self.ip_pool.append(ip)
			top_tier_net.append(ip)

			network.add_node(".".join(list(map(str,ip))))

		mid_tier_net = []

		for net in top_tier_net:
			for subnet in range(mid_tier):
				ip = self.allocate_ip((net[0],"*",0,0))
				self.ip_pool.append(ip)
				mid_tier_net.append(ip)

				network.add_node(".".join(list(map(str,ip))))

		low_tier_net = []

		for net in mid_tier_net:
			for subnet in range(low_tier):
				ip = self.allocate_ip((net[0],net[1],"*",0))
				self.ip_pool.append(ip)
				low_tier_net.append(ip)

				network.add_node(".".join(list(map(str,ip))))

		clients = []

		for net in low_tier_net:
			for client in range(end_systems):
				ip = self.allocate_ip((net[0],net[1],net[2],"*"))
				self.ip_pool.append(ip)
				clients.append(ip)

				network.add_node(".".join(list(map(str,ip))))

		#Connecting the graph
		for net in top_tier_net:
			for net2 in top_tier_net:
				if net != net2:
					network.add_edge(".".join(list(map(str,net))), ".".join(list(map(str,net2))), weight=0)

		for net in mid_tier_net:
			network.add_edge("{}.0.0.0".format(net[0]), ".".join(list(map(str,net))), weight=0.1)

		for net in low_tier_net:
			network.add_edge("{}.{}.0.0".format(net[0], net[1]), ".".join(list(map(str,net))), weight=0.5)

		for client in clients:
			network.add_edge("{}.{}.{}.0".format(client[0], client[1], client[2]), ".".join(list(map(str,client))), weight=0.9)
				

		return network
		

	def allocate_ip(self, mask):
		ip_candidate = list(mask)

		for segment in range(len(ip_candidate)):
			if mask[segment] == "*":
				ip_candidate[segment] = random.randint(0, 255)

		ip_candidate = tuple(ip_candidate)

		return ip_candidate if ip_candidate not in self.ip_pool else self.allocate_ip(mask)


	def draw_network(self):
		nx.draw_spring(self.graph, with_labels=True)
		plt.draw()
		plt.show()
