# Optimal Meeting Point Graphs
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import string


def main():
    # V = pd.read_csv('../data/cal.cnode', sep=" ")
    # print(V[:10])
    # E = pd.read_csv('../data/cal.cedge', sep=" ")
    # print(E[])
    e_list = pd.read_csv('../data/bspgraph.csv', sep=";")
    G = nx.from_pandas_edgelist(e_list, edge_attr=True)

    ######### adding positions #########
    G.add_node('A', pos=(1,1))
    G.add_node('B', pos=(3,1))
    G.add_node('C', pos=(5,1))
    G.add_node('D', pos=(7,1))
    G.add_node('E', pos=(1,3))
    G.add_node('F', pos=(3,3))
    G.add_node('G', pos=(5,3))
    G.add_node('H', pos=(7,3))
    G.add_node('I', pos=(2,5))
    G.add_node('J', pos=(4,5))
    G.add_node('K', pos=(6,5))
    G.add_node('L', pos=(0,7))
    G.add_node('M', pos=(3,7))
    G.add_node('N', pos=(6,7))
    G.add_node('P', pos=(9,7))
    G.add_node('Q', pos=(0,9))
    G.add_node('R', pos=(3,9))
    G.add_node('S', pos=(5,9))
    G.add_node('T', pos=(8,9))
    ######### adding positions done ########
    pos = nx.get_node_attributes(G,'pos')
    print(pos)

    w = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx(G, pos=pos)
    nx.draw_networkx_edge_labels(G, edge_labels=w, pos=pos)
    plt.show()


if __name__ == "__main__":
    main()
