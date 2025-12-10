import osmnx.io as oxio
import osmnx.graph as oxgraph
import osmnx.plot as oxplot

import os.path as osp

from graph.Graph import Graph, Energy_Station

def get_graph() -> Graph:

    graph_path = "parser/osmnx.graphml"
    if osp.isfile(graph_path):
        graph_osmnx = oxio.load_graphml(graph_path)
    else:
        graph_osmnx = oxgraph.graph_from_place("Porto", network_type="drive")
        oxio.save_graphml(graph_osmnx, filepath=graph_path)

    graph = Graph()

    for node, data in graph_osmnx.nodes(data=True):
        graph.add_node(str(node), data['y'], data['x'], Energy_Station.NONE)

    max_speed = 0
    for origin, destination, data in graph_osmnx.edges(data=True):
        speed = 50
        if speed > max_speed:
            max_speed = speed
        # the distances come in meters as floats, so it's safe to convert to int
        graph.add_edge(str(origin), str(destination), int(data["length"]), speed)

    graph.set_max_speed(max_speed)

    print(graph.number_of_nodes())
    print(graph.number_of_edges())
    print(graph_osmnx.number_of_nodes())
    print(graph_osmnx.number_of_edges())

    #oxplot.plot_graph(graph_osmnx)
    
    return graph


if __name__ == "__main__":
    get_graph()
