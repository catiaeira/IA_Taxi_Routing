import osmnx.io as oxio
import osmnx.graph as oxgraph
import osmnx.plot as oxplot

import os.path as osp

from graph.Graph import Graph, Energy_Station

def get_graph() -> Graph:

    graph_path = "parser/gualtar.graphml"
    if osp.isfile(graph_path):
        graph_osmnx = oxio.load_graphml(graph_path)
    else:
        graph_osmnx = oxgraph.graph_from_place("Gualtar, Braga", network_type="drive")
        oxio.save_graphml(graph_osmnx, filepath=graph_path)

    graph = Graph()

    for node in graph_osmnx.nodes():
        graph.add_node(str(node), 0, 0, Energy_Station.NONE)

    for origin, destination, data in graph_osmnx.edges(data=True):
        # the distances come in meters as floats, so it's safe to convert to int
        graph.add_edge(str(origin), str(destination), int(data["length"]), 50)

    print(graph.numberOfNodes())
    print(graph.numberOfEdges())
    print(graph_osmnx.number_of_nodes())
    print(graph_osmnx.number_of_edges())

    oxplot.plot_graph(graph_osmnx)
    
    return graph


if __name__ == "__main__":
    get_graph()
