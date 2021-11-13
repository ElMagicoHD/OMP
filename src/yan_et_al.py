import networkx as nx
import convex_hull
import pandas as pd
import kdtree as kd


# Euclidean heuristic for A*
def heuristic(u, v):
    """
    computes the straight-line distance (Luftlinie) in order to use as the heuristic for the A*-algorithm
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


def baseline_omp(G, Q):
    """
    baseline algorithm for finding an OMP. Source: Da Yan et al. [1]
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

        #
        if sum_of_distance > min_cost:
            return sum_of_distance

    return sum_of_distance


def two_phase_online_convex_hull_based_pruning(G, Q):
    H = convex_hull.two_phase_convex_hull(G=G, Q=Q)
    opt = None
    min_cost = float('inf')

    for q in Q:
        cost = sod(G=G, v=q, Q=Q, min_cost=min_cost)

        if cost < min_cost:
            min_cost = cost
            opt = q

    pos = nx.get_node_attributes(G=G, name='pos')
    pos_df = pd.DataFrame(pos)
    pos_hull = pos_df[H]
    sorted_by_x = pos_hull.sort_values(by=0, axis=1)
    sorted_by_y = pos_hull.sort_values(by=1, axis=1)
    # MBR[x_min, x_max, y_min, y_max]
    MBR = [sorted_by_x.iloc[:, 0][0], sorted_by_x.iloc[:, -1][0], sorted_by_y.iloc[:, 0][1], sorted_by_y.iloc[:, -1][1]]

    for v in G.nodes:

        if pos_df[v][0] < MBR[0] or pos_df[v][1] > MBR[1] or MBR[2] > pos_df[v][1] or pos_df[v][1] > MBR[3]:
            if not is_inside_of_convex_hull(hull=H, p=v, pos=pos):
                continue

        cost = sod(G=G, v=v, Q=Q, min_cost=min_cost)

        if cost < min_cost:
            min_cost = cost
            opt = v

    return opt


def is_inside_of_convex_hull(hull, p, pos):
    p = pos[p]
    hull = hull[::-1]
    for i in range(len(hull) - 1):

        p1, p2 = pos[hull[i]], pos[hull[i + 1]]
        ccw = (p2[0] - p1[0]) * (p[1] - p1[1]) - (p[0] - p1[0]) * (p2[1] - p1[1])

        if ccw <= 0:
            return True
    return False


def greedy_algorithm(G, Q):
    """
    greedy algorithm from Da Yan et al. [1]

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
    improved greedy algorithm with base from Da Yan et al. [1]

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
