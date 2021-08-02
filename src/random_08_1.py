import yan_et_al as yan
import random
from time import time
import csv
import networkx as nx


def random_benchmark(vertices, density, size_of_Q=5):
    number_of_edges = density / 2
    number_of_edges *= vertices
    number_of_edges *= (vertices - 1)

    for i in range(1, 51):
        print("Iteration " + str(i) + " of random bench with " + str(vertices) + " nodes and density of " + str(density))
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
        base, cost_b = yan.baseline_opm(G=G, Q=Q)
        duration_baseline = time() - start
        print("greedy go")
        start = time()
        gred, cost_g = yan.greedy_algorithm(G=G, Q=Q)
        duration_greedy = time() - start
        if base == gred:
            with open("/home/elmagico/OPM/benchmarks/benchmarking_random_08.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(i), str(vertices), str(number_of_edges), str(size_of_Q),
                    str(density), str(duration_baseline), str(duration_greedy), "True", "0"])
        else:
            percentual_difference = cost_g - cost_b
            percentual_difference /= cost_b
            percentual_difference *= 100
            with open("/home/elmagico/OPM/benchmarks/benchmarking_random_08.txt", mode='a') as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(i), str(vertices), str(number_of_edges), str(size_of_Q),
                    str(density), str(duration_baseline), str(duration_greedy), "False", str(percentual_difference)])
        with open("/home/elmagico/OPM/benchmarks/benchmarking_edges_per_node_random_08_1.txt", mode='a') as f:
            writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(list(G.degree(G.nodes())))


if __name__ == "__main__":
    vertices = [100,1000]
    for v in vertices:
        random_benchmark(vertices=v, density=0.8)
    