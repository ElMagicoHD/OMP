import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


G = nx.read_graphml('../../data/Merano.gxl')

#get axis from all nodes
# x_axis = nx.get_node_attributes(G, 'x')
# y_axis = nx.get_node_attributes(G, 'y')
# ds = [x_axis, y_axis]
# pos = {}
# for k in x_axis.keys():
#     pos[k] = tuple(float(d[k]) for d in ds)
# print(pos)
nx.set_node_attributes(G, (nx.get_node_attributes(G, 'x'), nx.get_node_attributes(G, 'y')), name="pos")
print(G.number_of_nodes())
print(nx.density(G))
nx.draw(G, pos=nx.get_node_attributes(G, name="pos"))
plt.show()


