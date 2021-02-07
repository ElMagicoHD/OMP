import networkx as nx
import pandas as pd


# Andrew's monotone chain convex hull algorithm src:
# https://en.wikibooks.org/w/index.php?title=Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain&oldid=3689563
def compute_convex_hull(graph, nodes):
    # no convex hull possible
    if len(nodes) <= 1:
        return nodes

    pos = nx.get_node_attributes(G=graph, name="pos")
    df = pd.DataFrame.from_dict(pos)
    df = df[nodes]
    sor = df.sort_values(by=[0, 1], axis=1)

    def cross_product(a, b, c):
        a_x, a_y = df[a][0], df[a][1]
        b_x, b_y = df[b][0], df[b][1]
        c_x, c_y = df[c][0], df[c][1]

        return (b_x - a_x) * (c_y - a_y) - (b_y - a_y) * (c_x - a_x)

    U = []
    L = []

    for v in sor:
        while len(L) >= 2 and cross_product(L[-2], L[-1], v) <= 0:
            L.pop()
        L.append(v)

    for v in sor.iloc[:, ::-1]:
        while len(U) >= 2 and cross_product(U[-2], U[-1], v) <= 0:
            U.pop()
        U.append(v)

    return L[:-1] + U[:-1]


def two_phase_convex_hull(G, Q):
    P = []

    for node in Q:
        neighbors = nx.all_neighbors(graph=G, node=node)
        P.append(node)
        for neighbor in neighbors:
            P.append(neighbor)

    # eliminate duplicates
    P = list(set(P))

    H = compute_convex_hull(graph=G, nodes=P)

    # just like the pseudocode of the paper
    H.append(H[0])
    S = []
    for i in range(len(H) - 1):
        shortest_path = nx.shortest_path(G, source=H[i], target=H[i + 1], weight="weight")
        for v in shortest_path:
            S.append(v)

    # eliminate duplicates again
    S = list(set(S))

    final_hull = compute_convex_hull(graph=G, nodes=S)
    return final_hull
