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
    G.add_node('K', pos=(8, 5))
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


def create_grids(G: nx.classes.graph.Graph, number_of_grids_per_level=4, number_of_levels=1) \
        -> nx.classes.graph.Graph:
    """
    Splits input graph in different grids, for Graph G = (V,E), where vertex for every v in V
    v is in exactly one grid per layer
    ----
    :argument G: nx.classes.graph.Graph
    :argument number_of_grids_per_level: int
    :argument number_of_levels: int

    :returns Graph with Node attributes including Grids
    ____

    """
    assert (G is not None)
    assert (number_of_grids_per_level >= 1)
    assert (number_of_levels >= 1)

    pos = nx.get_node_attributes(G, "pos")
    list_of_positions = list(pos.values())
    x, y = zip(*list_of_positions)
    min_vertical = min(y)
    min_horizontal = min(x)
    max_vertical = max(y)
    max_horizontal = max(x)

    # calculate the step size
    x_step_size = (max_vertical - min_vertical) / number_of_grids_per_level
    y_step_size = (max_horizontal - min_horizontal) / number_of_grids_per_level

    #creating dict with gridattributes
    node_layers = dict.fromkeys(G.nodes(),{})
    for node in node_layers:
        for i in range(number_of_levels):
            index = "level" + str(i)
            node_layers[node][index] = -1 #initializing with -1

    for gridx in range(number_of_grids_per_level):
        for gridy in range(number_of_grids_per_level):
            break

    return G
