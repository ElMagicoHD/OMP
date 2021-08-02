import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt


def download_city_road_network(filepath, city):

    if not filepath:
        raise ValueError("no filepath")
    if not city:
        raise ValueError("You should state which city you want to download")
    # adjust timeout because tokyo is a huge file
    ox.config(timeout=10000)
    # load graph from osm database
    G = ox.graph_from_place(query=city, network_type="drive")
    # store graph as graphml file to interpret it later with networkx
    ox.save_graphml(G=G, filepath=filepath)

    return

if __name__ == "__main__":
    download_city_road_network(filepath="/home/elmagico/OPM/data/berlin.gxl", city="Berlin, Germany")
    download_city_road_network(filepath="/home/elmagico/OPM/data/meran.gxl", city="Merano, Bolzano, Italy") # my hometown
    download_city_road_network(filepath="/home/elmagico/OPM/data/vienna.gxl", city="Vienna, Austria")
    download_city_road_network(filepath="/home/elmagico/OPM/data/nyc.gxl", city="New York, New York, USA")
    download_city_road_network(filepath="/home/elmagico/OPM/data/tokyo.gxl", city="Tokyo, Japan") # Tokys 



