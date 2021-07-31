import networkx as nx
import yan_et_al as yan
from time import time
import matplotlib.pyplot as plt
import csv
import random


def testing(v=10, density=0.2):
    e = density / 2
    e *= v * (v - 1)
    G = nx.gnm_random_graph(n=v, m=e)
    while not nx.is_connected(G):
        G = nx.gnm_random_graph(n=v, m=e)
    nx.set_node_attributes(G=G, values=nx.random_layout(G=G), name="pos")
    for (u,v,d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist = dist ** 0.5
        d["weight"] = dist

    Q = random.sample(G.nodes(), 2)

    nx.draw_networkx(G, nx.get_node_attributes(G=G, name="pos"))
    nx.draw_networkx_nodes(G, pos=nx.get_node_attributes(G=G, name="pos"), nodelist=Q, node_color="r")
    opt, _ = yan.greedy_algorithm(G=G, Q=Q)
    print(Q, opt)
    q1 = nx.astar_path(G=G, source=Q[0], target=opt, heuristic=yan.heuristic, weight="weight")
    q2 = nx.astar_path(G=G, source=Q[1], target=opt, heuristic=yan.heuristic, weight="weight")
    q1 = list(zip(q1, q1[1:]))
    q2 = list(zip(q2, q2[1:]))
    nx.draw_networkx_nodes(G=G, pos= nx.get_node_attributes(G=G, name="pos"), nodelist=[opt], node_color="green")
    nx.draw_networkx_edges(G=G, pos=nx.get_node_attributes(G=G, name="pos"), edgelist=q1, edge_color="yellow")
    nx.draw_networkx_edges(G=G, pos=nx.get_node_attributes(G=G, name="pos"), edgelist=q2, edge_color="red")
    plt.show()
# generates grid graph and plots it with OMP and the routes to the OMP
def grid_testing(v=10):
    G = nx.grid_2d_graph(v,v)
    Q = random.sample(G.nodes(), 2)
    for (v, d) in G.nodes(data=True):
        d["pos"] = v

    for (u, v, d) in G.edges(data=True):
        dist = (G.nodes[v]["pos"][0] - G.nodes[u]["pos"][0]) ** 2 + (
                G.nodes[v]["pos"][1] - G.nodes[u]["pos"][1]) ** 2
        dist = dist ** 0.5
        d["weight"] = dist
    nx.draw_networkx(G, nx.get_node_attributes(G=G, name="pos"))
    nx.draw_networkx_nodes(G, pos=nx.get_node_attributes(G=G, name="pos"), nodelist=Q, node_color="#fffb56")
    opt, _ = yan.greedy_algorithm(G=G, Q=Q)
    q1 = nx.astar_path(G=G, source=Q[0], target=opt, heuristic=yan.heuristic, weight="weight")
    q2 = nx.astar_path(G=G, source=Q[1], target=opt, heuristic=yan.heuristic, weight="weight")
    q1 = list(zip(q1, q1[1:]))
    q2 = list(zip(q2, q2[1:]))
    nx.draw_networkx_nodes(G=G, pos=nx.get_node_attributes(G=G, name="pos"), nodelist=[opt], node_color="#00e6ac")
    nx.draw_networkx_edges(G=G, pos=nx.get_node_attributes(G=G, name="pos"), edgelist=q1, edge_color="#ff41e9")
    nx.draw_networkx_edges(G=G, pos=nx.get_node_attributes(G=G, name="pos"), edgelist=q2, edge_color="#ff41e9")
    plt.show()

if __name__ == "__main__":
    #testing()
    #grid_testing()
