from Message import Message
from Network import Network
import Pathfinding as pf
import OnionSimulation as onion

"""
Main runtime, executed if OnionAnalysis.py is run directly.
"""

if __name__ == "__main__":
  """
  This basic simulation sets up a network with a set number of routers in
  each tier, and a set number of clients per low-tier router. This forms
  a network graph assembled as a tree.

  The graph is always connected.

  Note on density: the network capacity applies recursively; if mid_tier is set to 5, each top-tier
  will have its own unique 5 mid-tiers, same applies for mid-tier/low-tier and low-tier/clients.
  """

  #Network settings
  NET_CAPACITY = {
      "top_tier": 2,
      "mid_tier": 2,
      "low_tier": 2,
      "clients": 2
  }

  WEIGHT_MODS = {
      "top_tier": 0.1,
      "mid_tier": 0.3,
      "low_tier": 0.5,
      "client": 0.9
  }

  #Creating a simulated network.
  simulated_network = Network(NET_CAPACITY, WEIGHT_MODS)

  #Picking arbitrary start and end.
  source = ".".join(map(str,simulated_network.clients[0]))
  target = ".".join(map(str,simulated_network.clients[-1]))

  #Finding onion path
  onion_path = pf.find_onion_path(simulated_network, source, target)

  onion.onion_send("hi", onion_path)

  #Draw the network for visual inspection.
  #simulated_network.draw_network(onion_path)