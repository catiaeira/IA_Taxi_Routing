from graph.Graph import Graph
from graph.Energy_Station import Energy_Station
import json

def parse_graph() -> Graph:
    #file_path = input("File path: ")
    file_path = "parser/graph.json"
    
    with open(file_path, "r") as graph_file:
        json_graph = json.load(graph_file)

    g = Graph()

    for node in json_graph["nodes"]:
        g.add_node(node["name"], node["latitude"], node["longitude"], Energy_Station.convert_from_str(node["type"]))

    for edge in json_graph["edges"]:
        g.add_edge(edge["origin"], edge["destiny"], edge["dist"], edge["speed"])

    return g
