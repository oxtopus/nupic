import networkx as nx
import matplotlib.pyplot as plt



class NetworkXRenderer(object):
  def __init__(self, layoutFn=nx.spring_layout):
    self.layoutFn = layoutFn

  def render(self, G):
    pos = self.layoutFn(G)
    nx.draw_networkx(G, pos)
    nx.draw_networkx_edge_labels(G, pos, clip_on=False, rotate=False)
    plt.show()
