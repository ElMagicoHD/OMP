# Optimal Meeting Point Graphs
import networkx as nx
import matplotlib.pyplot as plt
from convex_hull import two_phase_convex_hull
import yan_et_al as yan
import pandas as pd
import kdtree as kd
import osmnx as ox
from time import time

from bspgraph import create_example_graph, create_grids


def calculate_opm():
    # G = create_example_graph()
    #
    # Q = ['G', 'H', 'N']
    # H = two_phase_convex_hull(G,Q)
    # print(H)
    # opm = yan.baseline_opm(Q=Q, G=G)
    # print(opm)
    # for q in Q:
    #     path = nx.shortest_path(G, q, opm, weight='weight')
    #     length = nx.shortest_path_length(G, q, opm, weight='weight')
    #     print('Shortest path from {} to {} is: \n {} \n with length: {}'.format(q, opm, path, length))
    # print(20 * '-')
    # opm = yan.two_phase_online_convex_hull_based_pruning(G=G, Q=Q)
    # for q in Q:
    #     path = nx.shortest_path(G, q, opm, weight='weight')
    #     length = nx.shortest_path_length(G, q, opm, weight='weight')
    #     print('Shortest path from {} to {} is: \n {} \n with length: {}'.format(q, opm, path, length))
    #
    # yan.greedy_algorithm(G=G, Q=Q)
    # pos = nx.get_node_attributes(G, "pos")
    # print(pos)
    # w = nx.get_edge_attributes(G, "weight")
    # nx.draw_networkx(G, pos=pos)
    # nx.draw_networkx_edge_labels(G, edge_labels=w, pos=pos)
    # plt.show()
    #
    # pos = nx.get_node_attributes(G=G, name="pos")
    # df = pd.DataFrame.from_dict(pos)
    # tree = kd.KdTree()
    # tree.build_tree(nodes_list=df)
    # print(tree.root)
    # z = (5, 3)
    # nn = tree.nearest_neighbor(z)
    # print("nn is " + str(nn))
    
    G = nx.read_graphml(path="../data/Merano.gxl")

    # get axis from all nodes
    x_axis = nx.get_node_attributes(G, 'x')
    y_axis = nx.get_node_attributes(G, 'y')
    ds = [x_axis, y_axis]
    pos = {}
    for k in x_axis.keys():
        pos[k] = tuple(float(d[k]) for d in ds)
    nx.set_node_attributes(G, pos, "pos")
    #add edges attribute with float instead of string
    len = nx.get_edge_attributes(G, "length")
    length = {k: float(v) for k, v in len.items()}
    nx.set_edge_attributes(G, length, "weight")

    Q = ['244048691', '256347321']
    reps = 10
    start = time()
    for i in range(0, reps):
        opt = yan.baseline_opm(G, Q)
    end = time()
    print(str(((end - start) / reps)) + " Sekunden im Durchschnitt")
    start = time()
    for i in range(0, reps):
        opt = yan.greedy_algorithm(G, Q)
    end = time()
    print(str(((end-start)/reps)) + " Sekunden im Durchschnitt")
    route1 = nx.shortest_path(G, Q[0], opt)
    route2 = nx.shortest_path(G, Q[1], opt)
    #converst routes from string to int
    route1 = [int(k) for k in route1]
    route2 = [int(k) for k in route2]

    Gx = ox.load_graphml(filepath="../data/Merano.gxl")
    ox.plot_graph(Gx)
    ox.plot_graph_routes(Gx, [route1, route2], route_colors=['red', 'yellow'])

    #print(opt)
    #nx.draw(G, pos=pos)
    #plt.show()
    return


if __name__ == "__main__":
    calculate_opm()
