import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import math

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

		neighbours = G.edges(current_min)

		for neighbour in neighbours:
			target = neighbour[1]
			alt = distance[current_min] + G[u][v]['weight']

			if alt < distance[target]:
				distance[target] = alt
				prev[target] = current_min

	return distance, prev




//Generates random network, can be changed to specific networks if need be
def Generate_Random_Network(nodes,edges,cost):
    G=nx.dense_gnm_random_graph(nodes,edges)
    for (u, v) in G.edges():
        rand = random.randint(0,cost)
        G[u][v]['weight'] = rand
    nx.draw_networkx(G)
    plt.draw()
    plt.show()


t0 = time.clock()
t1= time.clock()

rroutingTime = t1-t0

Generate_Random_Network(10,20,40)
