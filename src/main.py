# Optimal Meeting Point Graphs
import networkx as nx
import matplotlib.pyplot as plt
from convex_hull import two_phase_convex_hull
import yan_et_al as yan
import pandas as pd
import kdtree as kd
import osmnx as ox
from time import time
import numpy as np

from bspgraph import create_example_graph, create_grids


def calculate_opm():

    # Setting up the Graph
    G = nx.read_graphml(path="../data/Merano_nx.gxl")

    # get axis from all nodes
    x_axis = nx.get_node_attributes(G, 'x')
    y_axis = nx.get_node_attributes(G, 'y')
    ds = [x_axis, y_axis]
    pos = {}
    for k in x_axis.keys():
        pos[k] = tuple(float(d[k]) for d in ds)
    nx.set_node_attributes(G, pos, "pos")
    # Graph setup done

    number_of_random_Q_points = 5
    number_of_nodes = G.number_of_nodes()
    randomQ = np.random.randint(number_of_nodes, size=number_of_random_Q_points)
    Q = np.array(G.nodes)[randomQ]
    reps = 10
    start = time()
    for i in range(0, reps):
        opt = yan.baseline_opm(G=G, Q=Q)
    end = time()
    print("Baseline dauert " + str(((end - start) / reps)) + " Sekunden im Durchschnitt")
    start = time()
    for i in range(0, reps):
        opt = yan.greedy_algorithm(G, Q)
    end = time()
    print("Greedy dauert " + str(((end - start) / reps)) + " Sekunden im Durchschnitt")

    routes = []
    for i in range(number_of_random_Q_points):
        r = nx.shortest_path(G, Q[i], opt)
        r = [int(k) for k in r]
        routes.append(r)
    route_colors = ['b', 'r', 'g', 'c', 'm']
    Gx = ox.load_graphml(filepath="../data/Merano.gxl")
    #ox.plot_graph(Gx)
    ox.plot_graph_routes(Gx, routes, route_colors=route_colors)

    # print(opt)
    # nx.draw(G, pos=pos)
    # plt.show()
    return


if __name__ == "__main__":
    calculate_opm()
