import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt


def download_city_road_network(filepath, city):

    if not filepath:
        raise ValueError("no filepath")
    if not city:
        raise ValueError("You should state which city you want to download")
    # load graph from osm database
    G = ox.graph_from_place(query=city, network_type="drive")
    # store graph as graphml file to interpret it later with networkx
    ox.save_graphml(G=G, filepath=filepath)

    return

def plot_tokyo():
    G = ox.graph_from_place("Tokyo, Japan", network_type="drive")
    ox.plot_graph(G)
    plt.show()


if __name__ == "__main__":
    # download_city_road_network(, "Berlin, Berlin, Germany")
    # download_city_road_network(, "Merano, Bolzano, Italy") # my hometown
    # download_city_road_network(, "Vienna, Austria")
    # download_city_road_network(, "New York, New York, USA")
    # download_city_road_network(, "") #which other city could be interesting?
    #plot_tokyo()



