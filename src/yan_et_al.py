import networkx as nx
import convex_hull


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

    for v in G.nodes:

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
