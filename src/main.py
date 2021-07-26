# Optimal Meeting Point Graphs
import networkx as nx
import yan_et_al as yan
import osmnx as ox
import numpy as np
# benchmarking imports
from time import time
import csv
import random


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

    number_of_random_Q_points = 3
    number_of_nodes = G.number_of_nodes()
    randomQ = np.random.randint(number_of_nodes, size=number_of_random_Q_points)
    Q = np.array(G.nodes)[randomQ]
    reps = 3
    # start = time()
    # for i in range(0, reps):
    #    opt = yan.baseline_opm(G=G, Q=Q)
    # end = time()
    # print("Baseline dauert " + str(((end - start) / reps)) + " Sekunden im Durchschnitt")
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
    route_colors = ['b', 'r', 'g']
    Gx = ox.load_graphml(filepath="../data/Merano.gxl")
    # ox.plot_graph(Gx)
    ox.plot_graph_routes(Gx, routes, route_colors=route_colors)

    # print(opt)
    # nx.draw(G, pos=pos)
    # plt.show()
    return


def opm_function(vertices, density):
    size_of_Q = 10
    number_of_edges = int(density * vertices * (vertices - 1))
    print("baseline with density " + str(density) + "and " + str(vertices) + "nodes...")
    if (density < 0.6):
        # baseline 50 iterations
        for i in range(1, 51):
            G = nx.gnm_random_graph(vertices, number_of_edges)

            for (v, d) in G.nodes(data=True):
                d["pos"] = (random.uniform(0, 1000), random.uniform(0, 1000))

            # distance is simple euclidean
            for (u, v, d) in G.edges(data=True):
                dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                        G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
                dist = dist ** 0.5
                d["weight"] = dist

            Q = random.sample(G.nodes(), size_of_Q)
            start = time()
            yan.baseline_opm(G=G, Q=Q)
            end = time()
            duration = end - start
            with open("../benchmarks/benchmarking.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    ['baseline', str(density), str(vertices), str(number_of_edges), str(size_of_Q), str(i),
                     str(duration),
                     'gnm_random_graph'])

        print("greedy with density " + str(density) + "and " + str(vertices) + "nodes...")
        for i in range(1, 51):
            G = nx.gnm_random_graph(vertices, number_of_edges)

            for (v, d) in G.nodes(data=True):
                d["pos"] = (random.uniform(0, 1000), random.uniform(0, 1000))

            # distance is simple euclidean
            for (u, v, d) in G.edges(data=True):
                dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                        G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
                dist = dist ** 0.5
                d["weight"] = dist

            Q = random.sample(G.nodes(), size_of_Q)
            start = time()
            yan.greedy_algorithm(G=G, Q=Q)
            end = time()
            duration = end - start
            with open("../benchmarks/benchmarking.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    ['greedy', str(density), str(vertices), str(number_of_edges), str(size_of_Q), str(i), str(duration),
                     'gnm_random_graph'])
    else:
        print("baseline with density " + str(density) + "and " + str(vertices) + "nodes...")
        # baseline 50 iterations
        for i in range(1, 51):
            G = nx.dense_gnm_random_graph(vertices, number_of_edges)

            for (v, d) in G.nodes(data=True):
                d["pos"] = (random.uniform(0, 1000), random.uniform(0, 1000))

            # distance is simple euclidean
            for (u, v, d) in G.edges(data=True):
                dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                        G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
                dist = dist ** 0.5
                d["weight"] = dist

            Q = random.sample(G.nodes(), size_of_Q)
            start = time()
            yan.baseline_opm(G=G, Q=Q)
            end = time()
            duration = end - start
            with open("../benchmarks/benchmarking.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    ['baseline', str(density), str(vertices), str(number_of_edges), str(size_of_Q), str(i),
                     str(duration),
                     'gnm_random_graph'])

        print("greedy with density " + str(density) + "and " + str(vertices) + "nodes...")
        for i in range(1, 51):
            G = nx.dense_gnm_random_graph(vertices, number_of_edges)

            # generating random positions
            for (v, d) in G.nodes(data=True):
                d["pos"] = (random.uniform(0, 1000), random.uniform(0, 1000))

            # distance is simple euclidean
            for (u, v, d) in G.edges(data=True):
                dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                        G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
                dist = dist ** 0.5
                d["weight"] = dist

            Q = random.sample(G.nodes(), size_of_Q)
            start = time()
            yan.greedy_algorithm(G=G, Q=Q)
            end = time()
            duration = end - start
            with open("../benchmarks/benchmarking.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    ['greedy', str(density), str(vertices), str(number_of_edges), str(size_of_Q), str(i), str(duration),
                     'gnm_random_graph'])

    return


def grid_bench(vertices):
    G = nx.grid_2d_graph(vertices, vertices)
    size_of_Q = 10

    for (v, d) in G.nodes(data=True):
        d["pos"] = v

    for (u, v, d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist = dist ** 0.5
        d["weight"] = dist

    # baseline
    print("2d_grid baseline with " + str(vertices) + "x" + str(vertices) + " nodes")
    for i in range(1, 51):
        Q = random.sample(G.nodes(), size_of_Q)

        start = time()
        yan.baseline_opm(G=G, Q=Q)
        end = time()
        duration = end - start

        with open("../benchmarks/benchmarking.txt", mode='a') as f:
            writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                ['baseline', 'density not important', str(G.number_of_nodes), str(G.number_of_edges), str(size_of_Q),
                 str(i), str(duration),
                 '2d_grid_graph'])

    # greedy
    print("2d_grid baseline with " + str(vertices) + "x" + str(vertices) + " nodes")
    for i in range(1, 51):
        Q = random.sample(G.nodes(), size_of_Q)

        start = time()
        yan.greedy_algorithm(G=G, Q=Q)
        end = time()
        duration = end - start

        with open("../benchmarks/benchmarking.txt", mode='a') as f:
            writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                ['greedy', 'density not important', str(G.number_of_nodes), str(G.number_of_edges),
                 str(size_of_Q), str(i), str(duration),
                 '2d_grid_graph'])


def benchmarking():
    # toadd 100, deleted since already benchmarked that one
    number_of_vertices = [1000, 10000]  # maybe 1mio, but we'll check that later

    # Density of 0.2:
    for vertices in number_of_vertices:
        opm_function(vertices, 0.2)
    # Density of 0.5
    number_of_vertices = [100, 1000, 10000]
    for vertices in number_of_vertices:
        opm_function(vertices, 0.5)
    # Density of 0.8
    for vertices in number_of_vertices:
        opm_function(vertices, 0.8)

    # Grid Graphs
    number_of_vertices_squared = [10, 30, 50, 70, 100]  # actually that number squared

    for vertices in number_of_vertices_squared:
        grid_bench(vertices)
    return


if __name__ == "__main__":
    benchmarking()
