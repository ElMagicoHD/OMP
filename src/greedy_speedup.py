# Optimal Meeting Point Graphs
import networkx as nx
import yan_et_al_greedy_upgrade as yan
#import osmnx as ox
import numpy as np
#import matplotlib.pyplot as plt
# benchmarking imports
from time import time
import csv
import random

def random_benchmark(vertices, density, size_of_Q=5):
    number_of_edges = density / 2
    number_of_edges *= vertices
    number_of_edges *= (vertices - 1)

    for i in range(1, 6):
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
        print("greedy go")
        start = time()
        gred, cost_g = yan.greedy_algorithm(G=G, Q=Q)
        duration_greedy = time() - start
        with open("/home/elmagico/OPM/benchmarks/benchmarking_better_greedy_083.txt", mode='a') as f:
            writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                [str(i), str(vertices), str(number_of_edges), str(size_of_Q),
                str(nx.density(G)), str(duration_greedy)])

if __name__ == "__main__":
    random_benchmark(vertices=10000, density=0.8)