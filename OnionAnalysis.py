import networkx as nx
import matplotlib.pyplot as plt
import random
import time

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
def modify_djikstra(G, source, target):
    paths = list(nx.all_simple_paths(G, source=source, target=target))
    reliabilities = []
    for p in paths:
        tolRel = 1
        for i in range(len(p) - 1):
            tolRel = tolRel * float(G[p[i]][p[i + 1]]['r'])
        reliabilities.append(tolRel)
    path_sorted = []
    reliabilities_sorted = []
    for i in range(len(reliabilities)):
        index, value = max(enumerate(reliabilities), key=operator.itemgetter(1))
        path_sorted.append(paths[index])
        reliabilities_sorted.append(value)
        del paths[index]
        del reliabilities[index]
    return path_sorted, reliabilities_sorted

t1= time.clock()

rroutingTime = t1-t0

Generate_Random_Network(10,20,40)
