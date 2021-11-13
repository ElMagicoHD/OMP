# Optimal Meeting Point Graphs
import networkx as nx
import yan_et_al as yan
# import osmnx as ox
import numpy as np
# import matplotlib.pyplot as plt
# benchmarking imports
from time import time
import csv
import random


# def calculate_opm():
#     # Setting up the Graph
#     G = nx.read_graphml(path="../data/Merano_nx.gxl")
#
#     # get axis from all nodes
#     x_axis = nx.get_node_attributes(G, 'x')
#     y_axis = nx.get_node_attributes(G, 'y')
#     ds = [x_axis, y_axis]
#     pos = {}
#     for k in x_axis.keys():
#         pos[k] = tuple(float(d[k]) for d in ds)
#     nx.set_node_attributes(G, pos, "pos")
#     # Graph setup done
#
#     number_of_random_Q_points = 3
#     number_of_nodes = G.number_of_nodes()
#     randomQ = np.random.randint(number_of_nodes, size=number_of_random_Q_points)
#     Q = np.array(G.nodes)[randomQ]
#     reps = 3
#     # start = time()
#     # for i in range(0, reps):
#     #    opt = yan.baseline_opm(G=G, Q=Q)
#     # end = time()
#     # print("Baseline dauert " + str(((end - start) / reps)) + " Sekunden im Durchschnitt")
#     start = time()
#     for i in range(0, reps):
#         opt = yan.greedy_algorithm(G, Q)
#     end = time()
#     print("Greedy dauert " + str(((end - start) / reps)) + " Sekunden im Durchschnitt")
#
#     routes = []
#     for i in range(number_of_random_Q_points):
#         # maybe use astar_path with heuristic from yan.
#         r = nx.shortest_path(G, Q[i], opt)
#         r = [int(k) for k in r]
#         routes.append(r)
#     route_colors = ['b', 'r', 'g']
#     Gx = ox.load_graphml(filepath="../data/Merano.gxl")
#     # ox.plot_graph(Gx)
#     ox.plot_graph_routes(Gx, routes, route_colors=route_colors)
#
#     # print(opt)
#     # nx.draw(G, pos=pos)
#     # plt.show()
#     return


def grid_benchmark(vertices_per_axis, size_of_Q=5, filepath="/home/elmagico/OPM/benchmarks/benchmarking_grid.txt"):
    G = nx.grid_2d_graph(vertices_per_axis, vertices_per_axis)

    for (v, d) in G.nodes(data=True):
        d["pos"] = v

    for (u, v, d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist = dist ** 0.5
        d["weight"] = dist

    for i in range(1, 51):
        print("Iteration " + str(i) + " of grid bench with " + str(vertices_per_axis) + "x" + str(
            vertices_per_axis) + " nodes")
        Q = random.sample(G.nodes(), size_of_Q)
        start = time()
        base, cost_b = yan.baseline_opm(G=G, Q=Q)
        duration_baseline = time() - start
        start = time()
        gred, cost_g = yan.greedy_algorithm(G=G, Q=Q)
        duration_greedy = time() - start

        if gred == base:
            with open("/home/elmagico/OPM/benchmarks/benchmarking_grid.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(i), str(vertices_per_axis * vertices_per_axis), str(nx.number_of_edges(G)), str(size_of_Q),
                     str(nx.density(G)), str(duration_baseline), str(duration_greedy), "True", "0"])
        else:
            percentual_difference = cost_g - cost_b
            percentual_difference /= cost_b
            percentual_difference *= 100
            with open("/home/elmagico/OPM/benchmarks/benchmarking.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(i), str(vertices_per_axis * vertices_per_axis), str(nx.number_of_edges(G)), str(size_of_Q),
                     str(nx.density(G)), str(duration_baseline), str(duration_greedy), "False",
                     str(percentual_difference)])

        with open("/home/elmagico/OPM/benchmarks/benchmarking_edges_per_node_grid.txt") as f:
            writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(list(G.degree(G.nodes())))


def random_benchmark(vertices, density, size_of_Q=5):
    number_of_edges = density / 2
    number_of_edges *= vertices
    number_of_edges *= (vertices - 1)

    for i in range(1, 51):
        print(
            "Iteration " + str(i) + " of random bench with " + str(vertices) + " nodes and density of " + str(density))
        # For not dense is gnm faster, otherwise dense_gnm
        if density < 0.6:
            G = nx.gnm_random_graph(vertices, number_of_edges)
            # G should be connected, otherwise inf-loop
            while not nx.is_connected(G):
                G = nx.gnm_random_graph(vertices, number_of_edges)
        else:
            G = nx.dense_gnm_random_graph(vertices, number_of_edges)
            # G should be connected, otherwise inf-loop
            while not nx.is_connected(G):
                G = nx.dense_gnm_random_graph(vertices, number_of_edges)

        nx.set_node_attributes(G, nx.random_layout(G), name="pos")
        Q = random.sample(G.nodes(), size_of_Q)
        # for (_,d) in G.nodes(data=True):
        #     d["pos"] = (random.random(), random.random())
        # set weights, euclidean space
        for (u, v, d) in G.edges(data=True):
            dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                    G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
            dist **= 0.5
            d["weight"] = dist
        print("baseline go")
        start = time()
        base, cost_b = yan.baseline_omp(G=G, Q=Q)
        duration_baseline = time() - start
        print("greedy go")
        start = time()
        gred, cost_g = yan.greedy_algorithm(G=G, Q=Q)
        duration_greedy = time() - start
        
        if base == gred:
            with open("/home/elmagico/OPM/benchmarks/benchmarking_random_02.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(i), str(vertices), str(number_of_edges), str(size_of_Q),
                     str(density), str(duration_baseline), str(duration_greedy), "True", "0"])
        else:
            percentual_difference = cost_g - cost_b
            percentual_difference /= cost_b
            percentual_difference *= 100
            with open("/home/elmagico/OPM/benchmarks/benchmarking_random_02.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(i), str(vertices), str(number_of_edges), str(size_of_Q),
                     str(density), str(duration_baseline), str(duration_greedy), "False", str(percentual_difference)])
        with open("/home/elmagico/OPM/benchmarks/benchmarking_edges_per_node_random.txt", mode='a') as f:
            writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(list(G.degree(G.nodes())))


def benchmarking():  # 2jobs@node08
    vertices = [100, 1000, 10000]

    for v in vertices:
        random_benchmark(vertices=v, density=0.2)
    for v in vertices:
        random_benchmark(vertices=v, density=0.5)
    for v in vertices:
        random_benchmark(vertices=v, density=0.8)
    for v in vertices:
        grid_benchmark(vertices_per_axis=v)

    return


if __name__ == "__main__":
    benchmarking()
