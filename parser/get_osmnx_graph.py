import osmnx.io as oxio
import osmnx.graph as oxgraph
import osmnx.plot as oxplot

import os.path as osp

from graph.Graph import Graph
from graph.Energy_Station import Energy_Station

def match_single_type(road_type: str) -> int:
    match road_type:
        case "motorway":
            return 120
        case "trunk":
            return 100
        case "primary":
            return 90
        case "motorway_link" | "trunk_link" | "primary_link" | "secondary":
            return 70
        case "secondary_link" | "tertiary" | "busway":
            return 50
        case "tertiary_link" | "residential" | "unclassified" | "road":
            return 30
        case "living_street" | "service":
            return 20
        case "escape":
            return 5
        case _:
            print(f"Unknown highway type detected -> {road_type}")
            return 1


def parse_highway(road_types: str|list[str]) -> int:
    
    if isinstance(road_types, str):
        return match_single_type(road_types)
    else: 
        speeds: list[int] = []

        for road_type in road_types:
            speeds.append(match_single_type(road_type))

        min = 120
        for speed in speeds:
            if speed < min:
                min = speed

        return min

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
    speed = 0
    for origin, destination, data in graph_osmnx.edges(data=True):
        speed = parse_highway(data['highway'])
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
    _ = get_graph()
