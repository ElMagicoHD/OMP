import networkx as nx
import convex_hull
import pandas as pd


def baseline_opm(Q, G):
    opt = None
    min_cost = float('inf')  # positive infinity

    for q in Q:
        cost = sod(G=G, v=q, Q=Q, min_cost=min_cost)
        if cost < min_cost:
            min_cost = cost
            opt = q

    for v in G.nodes:
        cost = sod(G=G, v=v, Q=Q, min_cost=min_cost)

        if cost < min_cost:
            min_cost = cost
            opt = v
    return opt


def sod(G, v, Q, min_cost):
    sum_of_distance = 0
    for q in Q:
        sum_of_distance += nx.shortest_path_length(G, v, q, weight='weight')

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
    # compute center of gravity
    positions = pd.DataFrame.from_dict( nx.get_node_attributes(G, "pos") )[Q]
    all_x_axes = positions.iloc[0]
    all_y_axes = positions.iloc[1]
    q_x, q_y = all_x_axes.mean(), all_y_axes.mean()




    return None


