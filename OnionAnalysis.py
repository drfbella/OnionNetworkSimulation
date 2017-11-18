import networkx as nx
import matplotlib.pyplot as plt
import random

G=nx.dense_gnm_random_graph(10,20)

for (u, v) in G.edges():
    rand = random.randint(0,50)
    print(rand)
    G[u][v]['weight'] = rand
nx.draw_networkx(G)

nx.draw_networkx(G)
weight=nx.get_edge_attributes(G,'weight')
print(weight)

plt.draw()
plt.show()


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