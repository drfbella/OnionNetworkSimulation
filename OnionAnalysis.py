import networkx as nx
import matplotlib.pyplot as plt
import random
import time
import math

from Message import Message
from Network import Network
import Pathfinding as pf

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

  """
  This basic simulation sets up a network with a set number of routers in
  each tier, and a set number of clients per low-tier router. This forms
  a network graph assembled as a tree.

  The graph is always connected.
  """

  #Network settings
  net_capacity = {
    "top_tier": 3,
    "mid_tier": 3,
    "low_tier": 3,
    "clients": 3
  }

  weight_mods = {
    "top_tier": 0.1,
    "mid_tier": 0.3,
    "low_tier": 0.5,
    "client": 0.9
  }

  #Creating a simulated network.
  simulated_network = Network(net_capacity, weight_mods)

  #Picking arbitrary start and end.
  source = ".".join(map(str,simulated_network.clients[0]))
  target = ".".join(map(str,simulated_network.clients[-1]))

  onion_path = pf.find_onion_path(simulated_network, source, target)  

  #Onion_Simulation(simulated_network)
  """
  source, target =".".join(list(map(str,simulated_network.clients[0]))), ".".join(list(map(str,simulated_network.clients[-1])))
  d, p = modify_djikstra(simulated_network.graph, ".".join(list(map(str,simulated_network.clients[0]))), ".".join(list(map(str,simulated_network.clients[-1]))))
  path = rebuild_path(".".join(list(map(str,simulated_network.clients[0]))), ".".join(list(map(str,simulated_network.clients[-1]))), d, p)

  print(d[target])
  source, target =".".join(list(map(str,simulated_network.clients[-1]))), ".".join(list(map(str,simulated_network.clients[25])))
  d, p = modify_djikstra(simulated_network.graph, ".".join(list(map(str,simulated_network.clients[-1]))), ".".join(list(map(str,simulated_network.clients[25]))))
  path += rebuild_path(".".join(list(map(str,simulated_network.clients[-1]))), ".".join(list(map(str,simulated_network.clients[25]))), d, p)
"""
  #Draw the network for visual inspection.
  simulated_network.draw_network(onion_path)