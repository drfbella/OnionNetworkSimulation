import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import math

from Message import Message
from Network import Network

"""
Rebuilds the path based on the distance and previous lists provided by Djikstra's.
@param source ID of the node from which to start the pathing.
@param target ID of the node to which our path ends.
@param distance List of distances between nodes.
@param previous List of ancestors.
@return List representing the path.
"""

def rebuild_path(source, target, distance, previous):
	path = [target]

	while previous[path[0]] != source:
		path.insert(0, previous[path[0]])

	path.insert(0, source)

	return path

"""
Executes the Djikstra algorithm on the graph given a source and a target.
@param G networkx graph object
@param source ID of the node to start from.
@param target ID from the node to end at.
@return Lists representing distances and precedence between the two nodes selected.
"""

def modify_djikstra(G, source, target):
	node_pool = G.nodes().keys()

	vertex_pool = list()
	distance = dict()
	prev = dict()
	
	for vertex in node_pool:
		distance[vertex] = math.inf
		prev[vertex] = None
		vertex_pool.append(vertex)

	distance[source] = 0

	while vertex_pool:
		current_min = None
		min_val = math.inf

		for vertex in vertex_pool:
			if current_min is None or distance[vertex] < min_val:
				current_min = vertex
				min_val = distance[vertex]

		vertex_pool.remove(current_min)

		neighbours = G.edges(current_min, data=True)

		for neighbour in neighbours:
			target = neighbour[1]
			alt = distance[current_min] + neighbour[2]['weight']

			if alt < distance[target]:
				distance[target] = alt
				prev[target] = current_min

	return distance, prev

#simulates layer encryption at sender, by appending randomly picked nodes to the destination stack
def Onion_Encrypting(G,msg,numTargets):
		numNodes = nx.number_of_nodes(G)
		sect = numNodes/numTargets
		
		for i in range(1,numTargets):
				msg.destination.append((i-1)*sect +random.randint(0,sect))
		print(msg.destination)
		return msg

#simulates per-router decryption
def Onion_Decrypting(msg):
		dest = msg.destination.pop()
		msg.source.append(dest)
		return dest

#simulates message transmission on network
def send(G,msg):
	while (msg.destination):
			source = msg.source[-1]
			dest = Onion_Decrypting(msg)
			print("On this hop, my source is node ",source,"and destination ", dest)
			modify_djikstra(G, source, dest)
	print(msg.destination)
	print(msg.source)
	print(msg.message)
		

def Onion_Simulation(network):
	
	#Creates message object
	msg = Message()
	msg.source.append(".".join(list(map(str,network.clients[0]))))
	msg.destination.append(".".join(list(map(str,network.clients[-1]))))
	msg.message = "My Name is Daniel"
	
	msg = Onion_Encrypting(network.graph, msg, 3)
	send(network.graph, msg)

"""
Main runtime, executed if OnionAnalysis.py is run directly.
"""

if __name__ == "__main__":

	#Created a simulated network.
	simulated_network = Network(210, 40)

	#Run the Onion simulation.
	#Onion_Simulation(simulated_network)
	source, target =".".join(list(map(str,simulated_network.clients[0]))), ".".join(list(map(str,simulated_network.clients[-1])))
	d, p = modify_djikstra(simulated_network.graph, ".".join(list(map(str,simulated_network.clients[0]))), ".".join(list(map(str,simulated_network.clients[-1]))))
	path = rebuild_path(".".join(list(map(str,simulated_network.clients[0]))), ".".join(list(map(str,simulated_network.clients[-1]))), d, p)

	print(d[target])
	source, target =".".join(list(map(str,simulated_network.clients[-1]))), ".".join(list(map(str,simulated_network.clients[25])))
	d, p = modify_djikstra(simulated_network.graph, ".".join(list(map(str,simulated_network.clients[-1]))), ".".join(list(map(str,simulated_network.clients[25]))))
	path += rebuild_path(".".join(list(map(str,simulated_network.clients[-1]))), ".".join(list(map(str,simulated_network.clients[25]))), d, p)

	print(d[target])
	#Draw the network for visual inspection.
	simulated_network.draw_network(path)