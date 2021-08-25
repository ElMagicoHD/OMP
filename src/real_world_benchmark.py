import osmnx as ox
import networkx as nx
import numpy as np
from time import time
import yan_et_al as yan
import csv
import sys
import random


def meran(iterations=50):

    number_of_q = [2,5,10,20,50]

    # Setting up the Graph
    G = nx.read_graphml(path="/home/elmagico/OPM/data/meran_nx.gxl")
    # get axis from all nodes
    x_axis = nx.get_node_attributes(G, 'x')
    y_axis = nx.get_node_attributes(G, 'y')
    ds = [x_axis, y_axis]
    pos = {}
    for k in x_axis.keys():
        pos[k] = tuple(float(d[k]) for d in ds)
    nx.set_node_attributes(G, pos, "pos")
    # Graph setup done

    for q in number_of_q:

        for i in range(1,iterations+1):

            Q = random.sample(G.nodes(), q)
            start = time()
            base, cost_b = yan.baseline_opm(G=G, Q=Q)
            duration_baseline = time() - start
            start = time()
            greedy, cost_g = yan.greedy_algorithm(G=G, Q=Q)
            duration_greedy = time() - start
            file = "/home/elmagico/OPM/benchmarks/benchmarking_meran.txt"
            if base == greedy:
                with open(file, mode='a') as f:
                    writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        [str(i), str(G.number_of_nodes()), str(G.number_of_edges()), str( len(Q) ),
                        str(nx.density(G)), str(duration_baseline), str(duration_greedy), "True", "0"])
            else:
                percentual_difference = cost_g - cost_b
                percentual_difference /= cost_b
                percentual_difference *= 100
                with open(file, mode='a') as f:
                    writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        [str(i), str(G.number_of_nodes()), str(G.number_of_edges()), str( len(Q) ),
                        str(nx.density(G)), str(duration_baseline), str(duration_greedy), "False", str(percentual_difference)])

            with open("/home/elmagico/OPM/benchmarks/meran_degree.txt", mode="a") as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow( nx.degree_histogram(G) )

def berlin(iterations=50):

    number_of_q = [2,5,10,20,50]

    # Setting up the Graph
    G = nx.read_graphml(path="/home/elmagico/OPM/data/berlin_nx.gxl")
    # get axis from all nodes
    x_axis = nx.get_node_attributes(G, 'x')
    y_axis = nx.get_node_attributes(G, 'y')
    ds = [x_axis, y_axis]
    pos = {}
    for k in x_axis.keys():
        pos[k] = tuple(float(d[k]) for d in ds)
    nx.set_node_attributes(G, pos, "pos")
    # Graph setup done

    for q in number_of_q:

        for i in range(1,iterations+1):

            Q = random.sample(G.nodes(), q)
            start = time()
            base, cost_b = yan.baseline_opm(G=G, Q=Q)
            duration_baseline = time() - start
            start = time()
            greedy, cost_g = yan.greedy_algorithm(G=G, Q=Q)
            duration_greedy = time() - start
            file = "/home/elmagico/OPM/benchmarks/benchmarking_berlin.txt"
            if base == greedy:
                with open(file, mode='a') as f:
                    writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        [str(i), str(G.number_of_nodes()), str(G.number_of_edges()), str( len(Q) ),
                        str(nx.density(G)), str(duration_baseline), str(duration_greedy), "True", "0"])
            else:
                percentual_difference = cost_g - cost_b
                percentual_difference /= cost_b
                percentual_difference *= 100
                with open(file, mode='a') as f:
                    writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        [str(i), str(G.number_of_nodes()), str(G.number_of_edges()), str( len(Q) ),
                        str(nx.density(G)), str(duration_baseline), str(duration_greedy), "False", str(percentual_difference)])
            with open("/home/elmagico/OPM/benchmarks/berlin_degree.txt", mode="a") as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow( nx.degree_histogram(G) )


def nyc(iterations=50):

    number_of_q = [2,5,10,20,50]

    # Setting up the Graph
    G = nx.read_graphml(path="/home/elmagico/OPM/data/nyc_nx.gxl")
    # get axis from all nodes
    x_axis = nx.get_node_attributes(G, 'x')
    y_axis = nx.get_node_attributes(G, 'y')
    ds = [x_axis, y_axis]
    pos = {}
    for k in x_axis.keys():
        pos[k] = tuple(float(d[k]) for d in ds)
    nx.set_node_attributes(G, pos, "pos")
    # Graph setup done

    for q in number_of_q:

        for i in range(1,iterations+1):

            Q = random.sample(G.nodes(), q)
            start = time()
            base, cost_b = yan.baseline_opm(G=G, Q=Q)
            duration_baseline = time() - start
            start = time()
            greedy, cost_g = yan.greedy_algorithm(G=G, Q=Q)
            duration_greedy = time() - start
            file = "/home/elmagico/OPM/benchmarks/benchmarking_nyc.txt"
            if base == greedy:
                with open(file, mode='a') as f:
                    writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        [str(i), str(G.number_of_nodes()), str(G.number_of_edges()), str( len(Q) ),
                        str(nx.density(G)), str(duration_baseline), str(duration_greedy), "True", "0"])
            else:
                percentual_difference = cost_g - cost_b
                percentual_difference /= cost_b
                percentual_difference *= 100
                with open(file, mode='a') as f:
                    writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        [str(i), str(G.number_of_nodes()), str(G.number_of_edges()), str( len(Q) ),
                        str(nx.density(G)), str(duration_baseline), str(duration_greedy), "False", str(percentual_difference)])
            with open("/home/elmagico/OPM/benchmarks/nyc_degree.txt", mode="a") as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow( nx.degree_histogram(G) )


def vienna(iterations=50):

    number_of_q = [2,5,10,20,50]

    # Setting up the Graph
    G = nx.read_graphml(path="/home/elmagico/OPM/data/vienna_nx.gxl")
    # get axis from all nodes
    x_axis = nx.get_node_attributes(G, 'x')
    y_axis = nx.get_node_attributes(G, 'y')
    ds = [x_axis, y_axis]
    pos = {}
    for k in x_axis.keys():
        pos[k] = tuple(float(d[k]) for d in ds)
    nx.set_node_attributes(G, pos, "pos")
    # Graph setup done

    for q in number_of_q:

        for i in range(1,iterations+1):

            Q = random.sample(G.nodes(), q)
            start = time()
            base, cost_b = yan.baseline_opm(G=G, Q=Q)
            duration_baseline = time() - start
            start = time()
            greedy, cost_g = yan.greedy_algorithm(G=G, Q=Q)
            duration_greedy = time() - start
            file = "/home/elmagico/OPM/benchmarks/benchmarking_vienna.txt"
            if base == greedy:
                with open(file, mode='a') as f:
                    writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        [str(i), str(G.number_of_nodes()), str(G.number_of_edges()), str( len(Q) ),
                        str(nx.density(G)), str(duration_baseline), str(duration_greedy), "True", "0"])
            else:
                percentual_difference = cost_g - cost_b
                percentual_difference /= cost_b
                percentual_difference *= 100
                with open(file, mode='a') as f:
                    writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        [str(i), str(G.number_of_nodes()), str(G.number_of_edges()), str( len(Q) ),
                        str(nx.density(G)), str(duration_baseline), str(duration_greedy), "False", str(percentual_difference)])
            with open("/home/elmagico/OPM/benchmarks/vienna_degree.txt", mode="a") as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow( nx.degree_histogram(G) )


def tokyo(iterations=50):

    number_of_q = [2,5,10,20,50]

    # Setting up the Graph
    G = nx.read_graphml(path="/home/elmagico/OPM/data/tokyo_nx.gxl")
    # get axis from all nodes
    x_axis = nx.get_node_attributes(G, 'x')
    y_axis = nx.get_node_attributes(G, 'y')
    ds = [x_axis, y_axis]
    pos = {}
    for k in x_axis.keys():
        pos[k] = tuple(float(d[k]) for d in ds)
    nx.set_node_attributes(G, pos, "pos")
    # Graph setup done

    for q in number_of_q:

        for i in range(1,iterations+1):

            Q = random.sample(G.nodes(), q)
            start = time()
            base, cost_b = yan.baseline_opm(G=G, Q=Q)
            duration_baseline = time() - start
            start = time()
            greedy, cost_g = yan.greedy_algorithm(G=G, Q=Q)
            duration_greedy = time() - start
            file = "/home/elmagico/OPM/benchmarks/benchmarking_tokyo.txt"
            if base == greedy:
                with open(file, mode='a') as f:
                    writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        [str(i), str(G.number_of_nodes()), str(G.number_of_edges()), str( len(Q) ),
                        str( nx.density(G) ), str(duration_baseline), str(duration_greedy), "True", "0"])
            else:
                percentual_difference = cost_g - cost_b
                percentual_difference /= cost_b
                percentual_difference *= 100
                with open(file, mode='a') as f:
                    writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        [str(i), str(G.number_of_nodes()), str(G.number_of_edges()), str( len(Q) ),
                        str(nx.density(G)), str(duration_baseline), str(duration_greedy), "False", str(percentual_difference)])
            with open("/home/elmagico/OPM/benchmarks/tokyo_degree.txt", mode="a") as f:
                writer = csv.writer(f, dialect="excel", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow( nx.degree_histogram(G) )


if __name__ == "__main__":
    city = sys.argv[1]

    if city == "meran":
        meran()
    elif city == "vienna":
        vienna()
    elif city == "nyc":
        nyc()
    elif city == "berlin":
        berlin()
    elif city == "tokyo":
        tokyo()
