# Optimal Meeting Point Graphs
import networkx as nx
import matplotlib.pyplot as plt
from convex_hull import two_phase_convex_hull
import yan_et_al as yan
import pandas as pd
import kdtree as kd

from bspgraph import create_example_graph, create_grids


def calculate_opm():
    G = create_example_graph()

    Q = ['G', 'H', 'N']
    H = two_phase_convex_hull(G,Q)
    print(H)
    opm = yan.baseline_opm(Q=Q, G=G)
    print(opm)
    for q in Q:
        path = nx.shortest_path(G, q, opm, weight='weight')
        length = nx.shortest_path_length(G, q, opm, weight='weight')
        print('Shortest path from {} to {} is: \n {} \n with length: {}'.format(q, opm, path, length))
    print(20 * '-')
    opm = yan.two_phase_online_convex_hull_based_pruning(G=G, Q=Q)
    for q in Q:
        path = nx.shortest_path(G, q, opm, weight='weight')
        length = nx.shortest_path_length(G, q, opm, weight='weight')
        print('Shortest path from {} to {} is: \n {} \n with length: {}'.format(q, opm, path, length))

    yan.greedy_algorithm(G=G, Q=Q)
    pos = nx.get_node_attributes(G, "pos")
    print(pos)
    w = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx(G, pos=pos)
    nx.draw_networkx_edge_labels(G, edge_labels=w, pos=pos)
    plt.show()

    pos = nx.get_node_attributes(G=G, name="pos")
    df = pd.DataFrame.from_dict(pos)
    tree = kd.KdTree()
    tree.build_tree(nodes_list=df)
    print(tree.root)
    z = (5, 3)
    nn = tree.nearest_neighbor(z)
    print("nn is " + str(nn))


if __name__ == "__main__":
    calculate_opm()
