import networkx as nx
from time import time
import csv
import random
import yan_et_al as yan


def grid_benchmark(vertices_per_axis, size_of_Q=5):
    G = nx.grid_2d_graph(vertices_per_axis, vertices_per_axis)

    for (v, d) in G.nodes(data=True):
        d["pos"] = v

    for (u, v, d) in G.edges(data=True):
        
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist = dist ** 0.5
        d["weight"] = dist

    for i in range(1, 51):
        print("Iteration " + str(i) + " of grid bench with " + str(vertices_per_axis) + "x" + str(vertices_per_axis) + " nodes")
        Q = random.sample(G.nodes(), size_of_Q)
        start = time()
        base, cost_b = yan.baseline_opm(G=G, Q=Q)
        duration_baseline = time() - start
        start = time()
        gred, cost_g = yan.greedy_algorithm(G=G, Q=Q)
        duration_greedy = time() - start

        if gred == base:
            with open("/home/elmagico/OPM/benchmarks/benchmarking_grid_1.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(i), str(vertices_per_axis * vertices_per_axis), str(nx.number_of_edges(G)), str(size_of_Q),
                    str(nx.density(G)), str(duration_baseline), str(duration_greedy), "True", "0"])
        else:
            percentual_difference = cost_g - cost_b
            percentual_difference /= cost_b
            percentual_difference *= 100
            with open("/home/elmagico/OPM/benchmarks/benchmarking_grid_1.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(i), str(vertices_per_axis * vertices_per_axis), str(nx.number_of_edges(G)), str(size_of_Q),
                    str(nx.density(G)), str(duration_baseline), str(duration_greedy), "False", str(percentual_difference)])
 
        with open("/home/elmagico/OPM/benchmarks/benchmarking_edges_per_node_grid_1.txt", mode='a') as f:
            writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(list(G.degree(G.nodes())))

if __name__ == "__main__":
    grid_benchmark(vertices_per_axis=10)
    grid_benchmark(vertices_per_axis=50)
