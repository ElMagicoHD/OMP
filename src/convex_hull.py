import networkx as nx
import pandas as pd


def compute_convex_hull(G):

    pos = nx.get_node_attributes(G, "pos")
    df = pd.DataFrame.from_dict(pos)
    sor = df.sort_values(by=[0,1], axis=1)


    return None

