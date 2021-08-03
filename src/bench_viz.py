import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def plotting(type_of_graph: str):
    if type_of_graph == "grid":

        df = pd.DataFrame(pd.read_csv("../benchmarks/benchmarking_grid.txt"))

        dfb = df[["vertices", "number_of_edges", "size_of_Q", "density", "duration_baseline"]]
        dfg = df[["vertices", "number_of_edges", "size_of_Q", "density", "duration_greedy"]]
        title = "Gittergraph"

    elif type_of_graph == "random_02":
        df = pd.DataFrame(pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_random_02.txt"))
        dfb = df[["vertices", "number_of_edges", "size_of_Q", "density", "duration_baseline"]]
        dfg = df[["vertices", "number_of_edges", "size_of_Q", "density", "duration_greedy"]]
        title = "Randomisierter Graph mit Dichte von 0.2"

    elif type_of_graph == "random_05":
        df = pd.DataFrame(pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_random_05.txt"))
        dfb = df[["vertices", "number_of_edges", "size_of_Q", "density", "duration_baseline"]]
        dfg = df[["vertices", "number_of_edges", "size_of_Q", "density", "duration_greedy"]]
        title = "Randomisierter Graph mit Dichte von 0.5"

    else:
        df = pd.DataFrame(pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_random_08.txt"))
        dfb = df[["vertices", "number_of_edges", "size_of_Q", "density", "duration_baseline"]]
        dfg = df[["vertices", "number_of_edges", "size_of_Q", "density", "duration_greedy"]]
        title = "Randomisierter Graph mit Dichte von 0.8"

    dfb = dfb.rename(columns={"duration_baseline": "duration"})
    dfg = dfg.rename(columns={"duration_greedy": "duration"})
    dfb["Algorithm"] = "Baseline"
    dfg["Algorithm"] = "Greedy"

    df = pd.concat([dfb, dfg])

    g = sns.lineplot(
        data=df, legend=True,
        x="vertices", y="duration",
        hue="Algorithm",
        ci="sd"
    )
    plt.title(title)
    g.set(yscale="linear",
          xlabel="Anzahl der Knoten", ylabel="Dauer in Sekunden")

    plt.legend(loc="upper left")
    plt.show()
    return







if __name__ == "__main__":
    plotting(type_of_graph="random_05")

