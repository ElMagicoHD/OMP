import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


G = nx.read_graphml('../../data/Merano.gxl')

#get axis from all nodes
x_axis = nx.get_node_attributes(G, 'x')
y_axis = nx.get_node_attributes(G, 'y')
ds = [x_axis, y_axis]
pos = {}
for k in x_axis.keys():
    pos[k] = tuple(float(d[k]) for d in ds)
print(pos)
nx.draw(G, pos=pos)
plt.show()


