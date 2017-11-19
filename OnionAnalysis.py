import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import math


class Message:
    source = []
    destination = []
    message = ""

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

def Generate_Random_Network(A,B,C):
	#Generates random network, can be changed to specific networks if need be
	G=nx.dense_gnm_random_graph(A,B)
	for (u, v) in G.edges():
			rand = random.randint(0,C)
			G[u][v]['weight'] = rand

	return G

#
#	TESTING
#

# Run Djikstra and try to find the path between nodes 0 and 5

#d, p = modify_djikstra(G, 0, 5)

# Rebuild the path using the Djikstra distance and previous vectors.
# Prints the path, too.

#print(rebuild_path(0, 5, d, p))

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
    

def Onion_Simulation():
    
    #Creates message object
    msg = Message()
    msg.source.append(1)
    msg.destination.append(10)
    msg.message = "My Name is Daniel"
    
    
    G= Generate_Random_Network(210,450,40)
    
    msg = Onion_Encrypting(G,msg,3)
    
    send(G,msg)
    


Onion_Simulation()
"""

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

nx.draw_networkx(G)#
plt.draw()
plt.show()

"""

