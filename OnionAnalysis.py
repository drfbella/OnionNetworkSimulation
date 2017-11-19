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




#Generates random network, can be changed to specific networks if need be
G=nx.dense_gnm_random_graph(210,450)
for (u, v) in G.edges():
    rand = random.randint(0,40)
    G[u][v]['weight'] = rand
nx.draw_networkx(G)
plt.draw()
plt.show()




#G= Generate_Random_Network(210,450,40)


N0 = random.randint(0,70)
N1 = random.randint(71, 140)
N2 = random.randint(141, 210)

t0 = time.clock()
distance, prev = modify_djikstra(G, 1, 92)
path = rebuild_path(1, 92, distance, prev)
print(path)
t1= time.clock()


distance, prev = modify_djikstra(G, 1, N0)
path = rebuild_path(1, N0, distance, prev)
print(path)

distance, prev = modify_djikstra(G, N0, N1)
path = rebuild_path(N0, N1, distance, prev)
print(path)

distance, prev = modify_djikstra(G, N1, N2)
path = rebuild_path(N1, N2, distance, prev)
print(path)

distance, prev = modify_djikstra(G, N2, 92)
path = rebuild_path(N2, 92, distance, prev)
print(path)

t2= time.clock()

#Encryption takes 0.08ms/operation. Decryption takes 1.46ms/operation

normalRouting = t1-t0
print(normalRouting)
onionRouting = t2-t1
print(onionRouting)



