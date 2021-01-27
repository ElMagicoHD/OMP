# Optimal Meeting Point Graphs
import networkx as nx
import matplotlib.pyplot as plt
from convex_hull import compute_convex_hull
import pandas as pd

from bspgraph import create_example_graph, create_grids


def main():
    # V = pd.read_csv('../data/cal.cnode', sep=" ")
    # print(V[:10])
    # E = pd.read_csv('../data/cal.cedge', sep=" ")
    # print(E[])
    G = create_example_graph()
    G = create_grids(G, 3, 1)
    compute_convex_hull(G)
    pos = nx.get_node_attributes(G, 'pos')
    w = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx(G, pos=pos)
    nx.draw_networkx_edge_labels(G, edge_labels=w, pos=pos)
    plt.show()


if __name__ == "__main__":
    main()
