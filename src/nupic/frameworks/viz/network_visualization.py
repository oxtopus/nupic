import networkx as nx
from . import NetworkXRenderer, GraphVizRenderer



class NetworkVisualizer(object):
  def __init__(self, network):
    self.network = network

  def export(self):
    G = nx.MultiDiGraph()
    regions = self.network.getRegions()

    for idx in xrange(regions.getCount()):
      regionPair = regions.getByIndex(idx)
      regionName = regionPair[0]
      G.add_node(regionName, label=regionName)

    for linkName, link in self.network.getLinks():
      G.add_edge(link.getSrcRegionName(),
                 link.getDestRegionName(),
                 src=link.getSrcOutputName(),
                 dest=link.getDestInputName())

    return G

  def render(self, renderer=NetworkXRenderer):
    renderer().render(self.export())
