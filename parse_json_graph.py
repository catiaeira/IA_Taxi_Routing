from Graph import Graph
import json

def parse_graph() -> Graph:
    #file_path = input("File path: ")
    file_path = "graph.json"
    
    with open(file_path, "r") as graph_file:
        json_graph = json.load(graph_file)

    g = Graph()

    for node in json_graph["nodes"]:
        g.add_node(node["name"], node["heuristic"])

    for edge in json_graph["edges"]:
        g.add_edge(edge["origin"], edge["destiny"], edge["dist"], edge["speed"])

    return g
