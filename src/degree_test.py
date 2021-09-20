import networkx as nx
from time import time
import yan_et_al as yan
import csv
import random


def degree_bench(deg: int = 3, size_of_Q: int = 5) -> None:
    # Graph setup
    G = nx.random_regular_graph(d=deg, n=5000)
    while not nx.is_connected(G):
        G = nx.random_regular_graph(d=deg, n=5000)
    nx.set_node_attributes(G=G, values=nx.spring_layout(G=G), name="pos")
    # Set euclidean distance
    for (u, v, d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist **= 0.5
        d["weight"] = dist
    # Graph setup done

    for i in range(1, 51):
        Q = random.sample(list(G.nodes()), size_of_Q)

        start = time()
        base, baseline_cost = yan.baseline_omp(G=G, Q=Q)
        duration_baseline = time() - start

        start = time()
        greedy, greedy_cost = yan.greedy_algorithm(G=G, Q=Q)
        duration_greedy = time() - start

        if base == greedy:
            with open("/home/elmagico/OPM/benchmarks/benchmarking_" + str(deg) + "regular.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(i), str(5000), str(G.number_of_edges()), str(size_of_Q),
                     str(nx.density(G)), str(duration_baseline), str(duration_greedy), "True", "0"])
        else:
            percentual_difference = greedy_cost - baseline_cost
            percentual_difference /= baseline_cost
            percentual_difference *= 100
            with open("/home/elmagico/OPM/benchmarks/benchmarking_" + str(deg) + "regular.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(i), str(5000), str(G.number_of_edges()), str(size_of_Q),
                     str(nx.density(G)), str(duration_baseline), str(duration_greedy), "False",
                     str(percentual_difference)])
        with open("/home/elmagico/OPM/benchmarks/benchmarking_edges_per_node" + str(deg) + "regular.txt",
                  mode='a') as f:
            writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(nx.degree_histogram(G))


if __name__ == "__main__":
    degree_bench(deg=3)
    degree_bench(deg=4)
    degree_bench(deg=5)
    degree_bench(deg=50)
    degree_bench(deg=100)
