import ast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def better_data():
    # only 50 entries at a time
    data = pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_edges_per_node_random_05_20.txt", sep=",",
                       nrows=50, skiprows=0, header=None)

    # converting string to tuples
    for i in data:
        data[i] = data[i].apply(ast.literal_eval)

    for column in range(data.shape[0]):
        for row in range(data.shape[1]):
            data[row][column] = data[row][column][1]
    # get histogram info
    flat = data.stack().values

    unique, counts = np.unique(flat,
                               return_counts=True)  # help from https://stackoverflow.com/questions/28663856/how-to-count-the-occurrence-of-certain-item-in-an-ndarray
    d = dict(zip(unique, counts))
    percentage = list(d.values())
    percentage = [(i / sum(percentage)) * 100.0 for i in percentage]
    print(sum(percentage))
    sns.set_context(context="notebook")
    ax = sns.barplot(x=list(d.keys()), y=percentage, color="cornflowerblue")
    ax.set(xlabel="Anzahl der Kanten pro Knoten", ylabel="Häufigkeit in %")
    # ax.figure.savefig("random_02_100_adj_distribution.png", bbox_inches="tight")
    plt.show()
    print(list(d.keys()))


def print_avg():
    data = pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_edges_per_node_random_08_20.txt",
                       nrows=10, skiprows=1, header=None)
    for i in data:
        data[i] = data[i].apply(ast.literal_eval)

    for column in range(data.shape[0]):
        for row in range(data.shape[1]):
            data[row][column] = data[row][column][1]
    flat = data.stack().values
    mean = np.mean(flat)
    print(mean)
    return


def hist():
    meran = [0, 138, 36, 495, 63, 5]
    nyc = [0, 3766, 347, 26354, 24216, 601, 57, 3, 1]
    tokyo = [0, 33057, 1207, 187071, 50343, 1042, 118, 14]
    vienna = [0, 1926, 483, 9589, 3888, 150, 16, 1]
    berlin = [0, 3308, 425, 16716, 7227, 178, 8]
    l = np.array([])
    for i in range(len(tokyo)):
        x = np.repeat(i, tokyo[i])
        l = np.append(l, x)
    # print(np.median(l))
    sns.set_context(context="talk")
    g = sns.barplot(x=list(range(len(vienna))), y=vienna)
    g.set(xlabel="Anzahl der Kanten pro Knoten", ylabel="Absolute Häufigkeit")
    g.figure.savefig("../images/vienna_distribution.png", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    # better_data()
    # hist()
    print_avg()
