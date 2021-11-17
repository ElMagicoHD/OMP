import networkx as nx
import yan_et_al as yan
# relevant for city graphs
# import osmnx as ox
import matplotlib.pyplot as plt
from time import time
import random as rnd


def random(density, number_of_nodes, size_of_Q):
    # Graph setup
    number_of_edges = density / 2
    number_of_edges *= number_of_nodes
    number_of_edges *= (number_of_nodes - 1)
    if density < 0.6:
        while True:
            G = nx.gnm_random_graph(number_of_nodes, number_of_edges)
            if nx.is_connected(G):
                break
    else:
        while True:
            G = nx.dense_gnm_random_graph(number_of_nodes, number_of_edges)
            if nx.is_connected(G):
                break

    nx.set_node_attributes(G, nx.random_layout(G), name="pos")
    # Set euclidean distance
    for (u, v, d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist **= 0.5
        d["weight"] = dist
    # Graph setup done
    return benchmark(G=G, size_of_Q=size_of_Q)


def k_regular(k, number_of_nodes, size_of_Q):
    # Graph setup
    while True:
        G = nx.random_regular_graph(d=k, n=number_of_nodes)
        if nx.is_connected(G):
            break
    nx.set_node_attributes(G=G, values=nx.spring_layout(G=G), name="pos")
    # Set euclidean distance
    for (u, v, d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist **= 0.5
        d["weight"] = dist
    # Graph setup done
    return benchmark(G=G, size_of_Q=size_of_Q)


def grid(nodes_per_axis, size_of_Q):
    # Graph setup
    G = nx.grid_2d_graph(nodes_per_axis, nodes_per_axis)

    for (v, d) in G.nodes(data=True):
        d["pos"] = v
    # Set euclidean distance
    for (u, v, d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist = dist ** 0.5
        d["weight"] = dist
    # Graph setup done
    return benchmark(G=G, size_of_Q=size_of_Q)


def benchmark(G, size_of_Q):
    Q = rnd.sample(list(G.nodes()), size_of_Q)
    print("Greedy algorithm start...")
    start = time()
    greedy_omp, greedy_sod = yan.greedy_algorithm(G=G, Q=Q)
    duration_greedy = time() - start
    print("Greedy algorithm done.\nBaseline algorithm start...")
    start = time()
    baseline_omp, baseline_sod = yan.baseline_algorithm(G=G, Q=Q)
    duration_baseline = time() - start
    print("Baseline algorithm done.")
    print("Greedy algorithm took", duration_greedy, " seconds. \nBaseline algorithm took", duration_baseline,
          " seconds.")
    if greedy_sod == baseline_sod:
        print("They both found the same or an equivalent OMP!")
    else:
        diff_in_percent = greedy_sod / baseline_sod
        diff_in_percent -= 1
        diff_in_percent *= 100
        print("The greedy algorithm found a suboptimal node, by ", diff_in_percent, "%.")

    if duration_baseline > duration_greedy:
        diff_in_sec = duration_baseline - duration_greedy
        print("And the greedy algorithm was ", diff_in_sec, "seconds faster.")
    else:
        diff_in_sec = duration_greedy - duration_baseline
        print("And the baseline algorithm was ", diff_in_sec, "seconds faster.")

    print("Drawing graph...")
    color_list = ["#CCEEFF" for i in range(G.number_of_nodes())]
    for q in Q:
        color_list[list(G.nodes()).index(q)] = "#0000FF"
    color_list[list(G.nodes()).index(greedy_omp)] = "#FF5500"
    color_list[list(G.nodes()).index(baseline_omp)] = "#FF00FF"
    nx.draw_networkx(G=G, pos=nx.get_node_attributes(G=G, name="pos"), node_color=color_list, with_labels=False,
                     node_size=25000 / G.number_of_nodes(), alpha=0.8)
    print(
        "Legend:\nblue: node\nyellow: Q\nred: greedy OMP\ngreen: baseline OMP\nIf there is no red node, then the algorithms found the same OMP.")
    plt.show()
    return


def main():
    size_of_Q = 5
    graph_type = input(
        "For which graph would you like to see the OMP algorithms?\nPlease select from: \"random\", \"k-regular\", \"grid\" : ")
    if graph_type == "random":
        return random(density=0.2, number_of_nodes=50, size_of_Q=size_of_Q)
    elif graph_type == "k-regular":
        return k_regular(k=5, number_of_nodes=50, size_of_Q=size_of_Q)
    elif graph_type == "grid":
        return grid(nodes_per_axis=25, size_of_Q=size_of_Q)
    else:
        print("Please choose one of the given examples!")
        return main()


if __name__ == "__main__":
    main()
