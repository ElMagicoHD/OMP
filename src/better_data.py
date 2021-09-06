import numpy as np
import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns



def better_data():

    # first 50 entries
    data = pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_edges_per_node_random_05_1.txt", sep=",", nrows=50, skiprows=50, header=None)

    #converting string to tuples
    for i in data:
        data[i] = data[i].apply(ast.literal_eval)

    for column in range(data.shape[0]):
        for row in range(data.shape[1]):
            data[row][column] = data[row][column][1]
    # get histogram info
    flat = data.stack().values

    unique, counts = np.unique(flat, return_counts=True)    #help from https://stackoverflow.com/questions/28663856/how-to-count-the-occurrence-of-certain-item-in-an-ndarray
    d = dict(zip(unique, counts))
    percentage = list(d.values())
    percentage = [(i/sum(percentage))*100.0 for i in percentage]
    print(sum(percentage))
    sns.set_context(context="notebook")
    ax = sns.barplot(x=list(d.keys()), y=percentage, color="cornflowerblue")
    ax.set(xlabel="Anzahl der Kanten pro Knoten", ylabel="Häufigkeit in %")
    ax.figure.savefig("random_02_100_adj_distribution.png", bbox_inches="tight")
    plt.show()







if __name__ == "__main__":
    better_data()