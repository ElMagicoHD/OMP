import osmnx as ox

road = ox.graph_from_place('Merano, Italy', network_type='drive')

#prj_road = ox.project_graph(road)

#ox.save_graphml(prj_road, filepath='../data/Merano.gxl')



ox.plot_graph(road)
