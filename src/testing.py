import networkx as nx
import random
from time import time
import matplotlib.pyplot as plt
import csv


def a():
    G = nx.gnm_random_graph(10,10)
    list = nx.degree_histogram(G)
    Q = random.sample(G.nodes(), 3)
    print(type(Q), Q)
    nx.draw(G)
    plt.show()
    with open("./testing/test.txt", "a") as f:
        writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(nx.degree_histogram(G))

    print(list)


if __name__ == "__main__":
    a()