import networkx as nx
import pandas as pd
import kdtree as kd


# Euclidean heuristic for A*
def heuristic(u, v):
    """
    Computes the straight-line distance (Luftlinie) in order to use as the heuristic for the A*-algorithm.
    :param u: startnode for the straight-line distance
    :type u: numpy.int64 or string
    :param v: endnode for the straight-line distance
    :type v: numpy.int64 or string
    :return: the computed straight-line distance
    :rtype: float or numpy.float64
    """
    dist = (Graph.nodes[v]["pos"][0] - Graph.nodes[u]["pos"][0]) ** 2 + (
            Graph.nodes[v]["pos"][1] - Graph.nodes[u]["pos"][1]) ** 2
    dist **= 0.5
    return dist


def baseline_algorithm(G, Q):
    """
    Baseline algorithm for finding an OMP. Source: Da Yan et al. [1]
    :param G: the graph on which the OMP should be found
    :type G: networkx.Graph
    :param Q: the list of starting points to find an OMP
    :type Q: list
    :return: omp - the found OMP. sod_omp - the sum of distances for all q in Q to omp on G
    :rtype: omp - numpy.int64 or string. sod_omp - numpy.float64
    """
    omp = None
    min_cost = float('inf')
    # not in use since our Q is part of V
    # for q in Q:
    #     cost = sod(G=G, v=q, Q=Q, min_cost=min_cost)
    #     if cost < min_cost:
    #         min_cost = cost
    #         opt = q

    # Set Graph as global, so the method "heuristic" can access it
    global Graph
    Graph = G

    for v in G.nodes:
        cost = sod(G=G, v=v, Q=Q, min_cost=min_cost)

        if cost < min_cost:
            min_cost = cost
            omp = v
    return omp, min_cost


def sod(G, v, Q, min_cost):
    sum_of_distance = 0
    for q in Q:
        sum_of_distance += nx.astar_path_length(G, v, q, heuristic=heuristic, weight="weight")

        if sum_of_distance > min_cost:
            return sum_of_distance

    return sum_of_distance


def greedy_algorithm(G, Q):
    """
    Greedy algorithm from Da Yan et al. [1]

    :param G: the graph on which the OMP should be found
    :type G: networkx.Graph
    :param Q: the list of starting points to find an OMP
    :type Q: list
    :return: omp - the found OMP. sod_omp - the sum of distances for all q in Q to omp on G
    :rtype: omp - numpy.int64 or string. sod_omp - numpy.float64
    """
    # compute center of gravity
    nodes_with_positions = pd.DataFrame.from_dict(nx.get_node_attributes(G, "pos"))
    positions_of_Q = nodes_with_positions[Q]
    all_x_axes = positions_of_Q.iloc[0]
    all_y_axes = positions_of_Q.iloc[1]
    gravity = (all_x_axes.mean(), all_y_axes.mean())

    # build kdtree
    tree = kd.KdTree()
    tree.build_tree(nodes_list=nodes_with_positions)

    # Set Graph as global, so the method "heuristic" can access it
    global Graph
    Graph = G
    omp = tree.nearest_neighbor(gravity).name
    sod_omp = greedy_sod(G, omp, Q)

    while True:

        neighbors = G.neighbors(omp)
        min_node = None
        sod_min = float("inf")
        # arg min like in line 6 of the pseudocode from yan et al.
        for n in neighbors:
            current_sod = greedy_sod(G, n, Q)
            if sod_min > current_sod:
                min_node = n
                sod_min = current_sod
        # subtle change from the pseudocode
        if sod_min >= sod_omp:
            return omp, sod_omp
        else:
            omp = min_node
            sod_omp = sod_min


def greedy_sod(G, v, Q):
    sum_of_distance = 0
    for q in Q:
        sum_of_distance += nx.astar_path_length(G, q, v, heuristic=heuristic, weight="weight")
    return sum_of_distance


def better_greedy_algorithm(G, Q):
    """
    Improved greedy algorithm with base from Da Yan et al. [1]

    :param G: the graph on which the OMP should be found
    :type G: networkx.Graph
    :param Q: the list of starting points to find an OMP
    :type Q: list
    :return: omp - the found OMP. sod_omp - the sum of distances for all q in Q to omp on G
    :rtype: omp - numpy.int64 or string. sod_omp - numpy.float64
    """
    # compute center of gravity
    nodes_with_positions = pd.DataFrame.from_dict(nx.get_node_attributes(G, "pos"))
    positions_of_Q = nodes_with_positions[Q]
    all_x_axes = positions_of_Q.iloc[0]
    all_y_axes = positions_of_Q.iloc[1]
    gravity = (all_x_axes.mean(), all_y_axes.mean())
    # build kdtree
    tree = kd.KdTree()
    tree.build_tree(nodes_list=nodes_with_positions)
    global Graph
    Graph = G
    omp = tree.nearest_neighbor(gravity).name
    sod_omp = greedy_sod(G, omp, Q)
    visited = {}

    while True:

        neighbors = G.neighbors(omp)
        min_node = None
        sod_min = float("inf")
        # arg min like in line 6 of the pseudocode from yan et al.
        for n in neighbors:
            if n in visited.keys():  # improvement as mentioned in bachelor thesis
                continue
            current_sod = greedy_sod(G, n, Q)
            visited[n] = n
            if sod_min > current_sod:
                min_node = n
                sod_min = current_sod
        # subtle change from the pseudocode
        if sod_min >= sod_omp:
            return omp, sod_omp
        else:
            omp = min_node
            sod_omp = sod_min
