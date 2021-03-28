import osmnx as ox

road = ox.graph_from_place('Berlin, Germany', network_type='drive')

prj_road = ox.project_graph(road)

ox.save_graphml(prj_road, filepath='../data/Berlin')

ox.plot_graph(prj_road)