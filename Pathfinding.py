import random
import re
import math

def find_onion_path(network, source, target, hops=3):
  """
  Route node selection process:

  Nodes participating in an onion route must not be part of the same /16 subnet.
  To ensure this, we choose 3 different low-tier nets and pick one of their clients
  each time. All three should then be in different /16 subnets.

  Note: Nodes on the same route may share a top- or mid-tier node.
  """
  print("\nFINDING ONION PATH USING DIJSKTRA'S SHORTEST PATH.\n")

  selected_low_tier = list()

  while len(selected_low_tier) < hops:
    candidate = network.low_tier_net[random.randint(0, len(network.low_tier_net)-1)]

    if candidate not in selected_low_tier:
      selected_low_tier.append(candidate)
  
  selected_clients = list()

  for subnet in selected_low_tier:
    edges = [client for client in network.graph.edges(".".join(map(str,subnet))) if re.match("[1-9][0-9]*\.[1-9][0-9]*\.[1-9][0-9]*\.[1-9][0-9]*", client[1]) is not None and client[1] != source and client[1] != target]
    selected_clients.append(edges[random.randint(0, len(edges)-1)][1])

  selected_clients.insert(0, source)
  selected_clients.append(target)
  onion_path = list()

  for iteration in range(len(selected_clients)-1):
    dist, prev = modify_djikstra(network.graph, selected_clients[iteration], selected_clients[iteration+1])
    path = rebuild_path(selected_clients[iteration], selected_clients[iteration+1], dist, prev)
    onion_path += path

  cleaned_path = list()

  for node in onion_path:
    if not cleaned_path or cleaned_path[-1] != node:
      cleaned_path.append(node)

  print("\nPATH ESTABLISHED BETWEEN {} and {} HAS {} BOUNCES.\n".format(source, target, len(cleaned_path)-2))

  return cleaned_path


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
