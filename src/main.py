import networkx as nx
import yan_et_al as yan
import osmnx as ox  # relevant for city graphs
import matplotlib.pyplot as plt
from time import time
import shutil
import random as rnd


def city(name, size_of_Q):
    """
    A method to setup the Graph of a given city, if data is not stored locally, the data will be downloaded.
    :param name: name of a city
    :type name: str
    :param size_of_Q: |Q|
    :type size_of_Q: int
    :return: the benchmark method
    """
    try:
        G = nx.read_graphml(path="../data/" + name + "_nx.graphml")
    except FileNotFoundError:
        print("Downloading city...")
        ox.config(timeout=10000)  # big timeout to download large cities like tokyo
        G = ox.graph_from_place(query=name, network_type="drive")
        ox.save_graphml(G=G, filepath="../data/" + name + ".graphml")

        # edit file to work better with NetworkX
        shutil.copyfile("../data/" + name + ".graphml", "../data/" + name + "_nx.graphml")
        with open("../data/" + name + "_nx.graphml", 'r') as file:
            data = file.readlines()

        for i, line in enumerate(data):
            if 'attr.name="length"' in line:
                data[i] = data[i].replace('attr.name="length" attr.type="string"',
                                          'attr.name="weight" attr.type="float"')
                break
        for i, line in enumerate(data):
            if 'attr.name="x"' in line:
                data[i] = data[i].replace('attr.type="string"', 'attr.type="float"')
                break
        for i, line in enumerate(data):
            if 'attr.name="y"' in line:
                data[i] = data[i].replace('attr.type="string"', 'attr.type="float"')
                break
        for i, line in enumerate(data):
            if 'graph edgedefault="directed"' in line:
                data[i] = data[i].replace('graph edgedefault="directed"', 'graph edgedefault="undirected"')
                break

        with open("../data/" + name + "_nx.graphml", 'w') as file:
            file.writelines(data)
        G = nx.read_graphml(path="../data/" + name + "_nx.graphml")

    # Graph setup
    # get axis from all nodes
    x_axis = nx.get_node_attributes(G, 'x')
    y_axis = nx.get_node_attributes(G, 'y')
    ds = [x_axis, y_axis]
    pos = {}
    for k in x_axis.keys():
        pos[k] = tuple(float(d[k]) for d in ds)
    nx.set_node_attributes(G, pos, "pos")
    # Graph setup done
    return benchmark(G=G, size_of_Q=size_of_Q, name_of_city=name)


def random(density, number_of_nodes, size_of_Q):
    """
    A method to generate a random undirected graph.
    :param density: density of the graph
    :type density: float
    :param number_of_nodes: |V|
    :type number_of_nodes: int
    :param size_of_Q: |Q|
    :type size_of_Q: int
    :return: the benchmark method
    """
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
    for (u, v, d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist **= 0.5
        d["weight"] = dist
    return benchmark(G=G, size_of_Q=size_of_Q)


def k_regular(k, number_of_nodes, size_of_Q):
    """
    A method to generate a k-regular undirected graph.
    :param k: degree of every node
    :type k: int
    :param number_of_nodes: |V|
    :type number_of_nodes: int
    :param size_of_Q: |Q|
    :type size_of_Q: int
    :return: the benchmark method
    """
    while True:
        G = nx.random_regular_graph(d=k, n=number_of_nodes)
        if nx.is_connected(G):
            break
    nx.set_node_attributes(G=G, values=nx.spring_layout(G=G), name="pos")
    for (u, v, d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist **= 0.5
        d["weight"] = dist
    return benchmark(G=G, size_of_Q=size_of_Q)


def grid(nodes_per_axis, size_of_Q):
    """
    A method to generate an undirected grid graph.
    :param nodes_per_axis: nodes_per_axis*nodes_per_axis == |V|
    :type nodes_per_axis: int
    :param size_of_Q: |Q|
    :type size_of_Q: int
    :return: the benchmark method
    """
    G = nx.grid_2d_graph(nodes_per_axis, nodes_per_axis)

    for (v, d) in G.nodes(data=True):
        d["pos"] = v
    for (u, v, d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist = dist ** 0.5
        d["weight"] = dist
    return benchmark(G=G, size_of_Q=size_of_Q)


def benchmark(G, size_of_Q, name_of_city=None):
    """
    A method to measure the elapsed time for the greedy and the baseline OMP algorithm on a given Graph with a given |Q|.
    Plots the given graph as well as Q and the found OMPs from both algorithms.
    :param G: Graph
    :type G: networkx.classes.graph.Graph
    :param size_of_Q: |Q|
    :type size_of_Q: int
    :param name_of_city: None if generated graph, otherwise the name of the city
    :type name_of_city: None or str
    :return: NoneType
    """
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
        print("The greedy algorithm found a suboptimal node by", diff_in_percent, "%.")

    if duration_baseline > duration_greedy:
        diff_in_sec = duration_baseline - duration_greedy
        print("And the greedy algorithm was", diff_in_sec, "seconds faster.")
    else:
        diff_in_sec = duration_greedy - duration_baseline
        print("And the baseline algorithm was", diff_in_sec, "seconds faster.")

    print("Drawing graph...")
    print(
        "Legend:\nlight blue: node\ndark blue: Q\norange: greedy OMP\nmagenta: baseline OMP\nIf there is no orange node, then the algorithms found the same OMP.\nIf there are less dark blue points than |Q|, then the OMP is a node of Q.\nNodes could be overlapping.")
    color_list = ["#CCEEFF" for i in range(G.number_of_nodes())]  # light blue
    for q in Q:
        color_list[list(G.nodes()).index(q)] = "#0000FF"  # dark blue
    color_list[list(G.nodes()).index(greedy_omp)] = "#FF5500"  # orange
    color_list[list(G.nodes()).index(baseline_omp)] = "#FF00FF"  # magenta
    if name_of_city is not None:
        G = ox.load_graphml("../data/" + name_of_city + ".graphml")
        ox.plot_graph(G=G, node_color=color_list)
    else:
        nx.draw_networkx(G=G, pos=nx.get_node_attributes(G=G, name="pos"), node_color=color_list, with_labels=False,
                         node_size=25000 / G.number_of_nodes(), alpha=0.8)

    plt.show()
    return


def main():
    size_of_Q = 5
    graph_type = input(
        "For which graph would you like to see the OMP algorithms?\nPlease select from: \"random\", \"k-regular\", \"grid\", \"city\" : ")

    if graph_type == "random":
        return random(density=0.2, number_of_nodes=50, size_of_Q=size_of_Q)
    elif graph_type == "k-regular":
        return k_regular(k=5, number_of_nodes=50, size_of_Q=size_of_Q)
    elif graph_type == "grid":
        return grid(nodes_per_axis=25, size_of_Q=size_of_Q)
    elif graph_type == "city":
        return city(name="meran", size_of_Q=size_of_Q)
    else:
        print("Please choose one of the given examples!")
        return main()


if __name__ == "__main__":
    main()
