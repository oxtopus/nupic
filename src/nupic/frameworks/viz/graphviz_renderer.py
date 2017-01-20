import io
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



class GraphVizRenderer(object):
  def render(self, G):
    G = nx.nx_agraph.to_agraph(G)
    G.layout()

    buffer = io.BytesIO()
    G.draw(buffer, format="png", prog="dot")
    buffer.seek(0)
    img = mpimg.imread(buffer)
    plt.imshow(img)
    plt.show()