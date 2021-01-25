import networkx as nx
import pandas as pd


def create_example_graph():
    e_list = pd.read_csv('../data/bspgraph.csv', sep=";")
    G = nx.from_pandas_edgelist(e_list, edge_attr=True)

    # adding positions for better graph
    G.add_node('A', pos=(0, 9))
    G.add_node('B', pos=(3, 9))
    G.add_node('C', pos=(5, 9))
    G.add_node('D', pos=(8, 9))
    G.add_node('E', pos=(0, 7))
    G.add_node('F', pos=(3, 7))
    G.add_node('G', pos=(6, 7))
    G.add_node('H', pos=(9, 7))
    G.add_node('I', pos=(2, 5))
    G.add_node('J', pos=(4, 5))
    G.add_node('K', pos=(6, 5))
    G.add_node('L', pos=(1, 3))
    G.add_node('M', pos=(3, 3))
    G.add_node('N', pos=(5, 3))
    G.add_node('O', pos=(7, 3))
    G.add_node('P', pos=(1, 1))
    G.add_node('Q', pos=(3, 1))
    G.add_node('R', pos=(5, 1))
    G.add_node('S', pos=(7, 1))
    # adding position done

    return G
