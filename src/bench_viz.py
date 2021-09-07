import matplotlib.pyplot as plt
import osmnx as ox
import pandas as pd
import seaborn as sns


def duration_plotting(type_of_graph: str):
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
    sns.set_context(context="talk")
    g = sns.lineplot(
        data=df, legend=True,
        x="vertices", y="duration",
        hue="Algorithm",
        ci="sd"
    )
    # plt.title(title)
    g.set(yscale="linear",
          xlabel="Anzahl der Knoten", ylabel="Dauer in Sekunden")

    plt.legend(loc="upper left")
    # plt.savefig(type_of_graph+"_talk.png")
    g.figure.savefig(type_of_graph+"_talk.png", bbox_inches="tight")
    plt.show()
    return

def difference_plotting(type_of_graph: str):

    df = pd.DataFrame(pd.read_csv("../benchmarks/benchmarking_" + type_of_graph +".txt"))
    df = df[["vertices", "number_of_edges", "same_omp", "diff_to_base"]]
    same = (df.diff_to_base.values == 0.0).sum()
    not_same = (df.diff_to_base.values != 0.0).sum()

    same = same / (same+not_same)
    same *= 100
    not_same = 100 - same
    print(same, not_same)
    g = sns.countplot(
        data=df,
        x=[same, not_same]

    )
    g.set(xlabel="Anzahl der Knoten", ylabel="Distanzunterschied zum wahren OMP in Prozent")

    plt.show()

def difference_greedy(with_normal_greedy=True):

    if with_normal_greedy:
        df_better_greedy = pd.DataFrame(pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_better_greedy_08.txt"))
        df_normal_greedy = pd.DataFrame(pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_random_08.txt"))
        df_better_greedy = df_better_greedy.rename(columns={"duration_greedy": "duration"})
        df_normal_greedy = df_normal_greedy.rename(columns={"duration_greedy": "duration"})
        df_normal_greedy = df_normal_greedy[["vertices", "number_of_edges", "size_of_Q", "density", "duration"]]
        df_better_greedy = df_better_greedy[["vertices", "number_of_edges", "size_of_Q", "density", "duration"]]
        df_normal_greedy["Algorithm"] = "Greedy"
        df_better_greedy["Algorithm"] = "Verbesserter Greedy"
        df = pd.concat([df_normal_greedy, df_better_greedy])
        title = "diff_to_normal_greedy_talk.png"
    else:
        df_better_greedy = pd.DataFrame(
            pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_better_greedy_08.txt"))
        df_baseline = pd.DataFrame(
            pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_random_08.txt"))
        df_better_greedy = df_better_greedy.rename(columns={"duration_greedy": "duration"})
        df_baseline = df_baseline.rename(columns={"duration_baseline": "duration"})
        df_better_greedy = df_better_greedy[["vertices", "number_of_edges", "size_of_Q", "density", "duration"]]
        df_baseline = df_baseline[["vertices", "number_of_edges", "size_of_Q", "density", "duration"]]
        df_better_greedy["Algorithm"] = "Verbesserter Greedy"
        df_baseline["Algorithm"] = "Baseline"
        df = pd.concat([df_better_greedy, df_baseline])
        title = "diff_better_greedy_to_baseline_talk.png"
    sns.set_context(context="talk")
    g = sns.lineplot(
        data=df, legend=True,
        x="vertices", y="duration",
        hue="Algorithm",
        ci="sd"
    )
    g.set(yscale="linear",
          xlabel="Anzahl der Knoten", ylabel="Dauer in Sekunden"
          )
    plt.legend(loc="upper left")
    g.figure.savefig(title, bbox_inches="tight")
    plt.show()
    return


def plot_city(name="meran"):
    if name == "meran":
        df = pd.DataFrame(pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_" + name + ".txt"))
        dfb = df[["size_of_Q", "duration_baseline"]]
        dfg = df[["size_of_Q", "duration_greedy"]]
        dfb = dfb.rename(columns={"duration_baseline": "duration"})
        dfg = dfg.rename(columns={"duration_greedy": "duration"})
        dfb["Algorithm"] = "Baseline"
        dfg["Algorithm"] = "Greedy"
        df = pd.concat([dfb, dfg])
        sns.set_context(context="talk")
        g = sns.lineplot(
            data=df, legend=True,
            x="size_of_Q", y="duration",
            hue="Algorithm",
            ci="sd"
        )
        g.set(yscale="linear",
              xlabel="|Q|", ylabel="Dauer in Sekunden"
              )
        g.set_xticks([2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
        plt.legend(loc="upper left")
        g.figure.savefig("../images/meran_q.png", bbox_inches="tight")
        plt.show()
    else:
        df = pd.DataFrame(pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_" + name + ".txt"))
        dfb = df[["size_of_Q", "duration_baseline"]]
        dfg = df[["size_of_Q", "duration_greedy"]]
        dfg2 = pd.DataFrame(pd.read_csv(filepath_or_buffer="../benchmarks/benchmarking_greedy_" + name + ".txt"))[
            ["size_of_Q", "duration_greedy"]]
        dfg = pd.concat([dfg, dfg2])
        dfb["Algorithm"] = "Baseline"
        dfg["Algorithm"] = "Greedy"
        dfb = dfb.rename(columns={"duration_baseline": "duration"})
        dfg = dfg.rename(columns={"duration_greedy": "duration"})
        df = pd.concat([dfb, dfg])
        df["duration"] = df["duration"] / 60.0
        sns.set_context(context="talk")
        g = sns.lineplot(
            data=df, legend=True,
            x="size_of_Q", y="duration",
            hue="Algorithm",
            ci="sd"
        )
        g.set(yscale="linear",
              xlabel="|Q|", ylabel="Dauer in Minuten"
              )
        g.set_xticks([2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
        g.figure.savefig("../images/" + name + "_q_min.png", bbox_inches="tight")
        plt.show()

def streetnetwork(name="meran"):
    fname = "/home/elmagico/OPM/data/" + name + ".gxl"
    Gx = ox.load_graphml(filepath=fname)
    # clist = ox.plot.get_colors(n=2, cmap="plasma", return_hex=True)
    fig, ax = ox.plot.plot_graph(Gx, bgcolor="white", node_color="black", figsize=[8, 8])
    fig.savefig("/home/elmagico/OPM/images/" + name + "_streetnetwork.png")


if __name__ == "__main__":
    # duration_plotting(type_of_graph="grid")
    # difference_greedy()
    # difference_plotting(type_of_graph="random_02")
    plot_city("")
    # streetnetwork("berlin")
    # streetnetwork("nyc")
    # streetnetwork("vienna")
    # streetnetwork("tokyo")
