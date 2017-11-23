import networkx as nx
import matplotlib.pyplot as plt
import random

class Network():
  def __init__(self, capacity, weight_modifiers):
    self.ip_pool = list()
    self.top_tier_net = list()
    self.mid_tier_net = list()
    self.low_tier_net = list()
    self.clients = list()
    self.base_cost = 1
    self.graph = self.generate_tiered_network(capacity["top_tier"], capacity["mid_tier"], capacity["low_tier"], capacity["clients"], weight_modifiers)

  def generate_tiered_network(self, top_tier, mid_tier, low_tier, end_systems, weight_modifiers):
    network = nx.Graph()

    for net in range(1, top_tier+1):
      ip = self.allocate_ip(("*", 0, 0, 0))
      self.ip_pool.append(ip)
      self.top_tier_net.append(ip)

      network.add_node(".".join(list(map(str,ip))))

    mid_tier_net = []

    for net in self.top_tier_net:
      for subnet in range(mid_tier):
        ip = self.allocate_ip((net[0],"*",0,0))
        self.ip_pool.append(ip)
        self.mid_tier_net.append(ip)

        network.add_node(".".join(list(map(str,ip))))

    self.low_tier_net = []

    for net in self.mid_tier_net:
      for subnet in range(low_tier):
        ip = self.allocate_ip((net[0],net[1],"*",0))
        self.ip_pool.append(ip)
        self.low_tier_net.append(ip)

        network.add_node(".".join(list(map(str,ip))))

    clients = []

    for net in self.low_tier_net:
      for client in range(end_systems):
        ip = self.allocate_ip((net[0],net[1],net[2],"*"))
        self.ip_pool.append(ip)
        self.clients.append(ip)

        network.add_node(".".join(list(map(str,ip))))

    #Connecting the graph
    for net in self.top_tier_net:
      for net2 in self.top_tier_net:
        if net != net2:
          network.add_edge(".".join(list(map(str,net))), ".".join(list(map(str,net2))), weight=0)

    for net in self.mid_tier_net:
      network.add_edge("{}.0.0.0".format(net[0]), ".".join(list(map(str,net))), weight=0.1)

    for net in self.low_tier_net:
      network.add_edge("{}.{}.0.0".format(net[0], net[1]), ".".join(list(map(str,net))), weight=0.5)

    for client in self.clients:
      network.add_edge("{}.{}.{}.0".format(client[0], client[1], client[2]), ".".join(list(map(str,client))), weight=0.9)

    return network    

  def allocate_ip(self, mask):
    ip_candidate = list(mask)

    for segment in range(len(ip_candidate)):
      if mask[segment] == "*":
        ip_candidate[segment] = random.randint(0, 255)

    ip_candidate = tuple(ip_candidate)

    return ip_candidate if ip_candidate not in self.ip_pool else self.allocate_ip(mask)


  def draw_network(self, path):

    node_list = self.graph.nodes()
    node_colour = list()

    for node in node_list:
      if node in path:
        node_colour.append("red")
      else:
        node_colour.append("blue")

    edge_colour = list()

    for edge in self.graph.edges():
      if edge[0] in path and edge[1] in path:
        edge_colour.append("red")
      else:
        edge_colour.append("black")

    node_position = nx.spring_layout(self.graph, k=0.15)
    nx.draw(self.graph, node_position, node_color=node_colour, edge_color=edge_colour, with_labels=True, node_size=100, font_size=10, k=0.15)
    plt.draw()
    plt.show()
