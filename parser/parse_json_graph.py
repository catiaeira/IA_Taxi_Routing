from graph.Graph import Graph
import json
import math

def parse_graph() -> Graph:
    #file_path = input("File path: ")
    file_path = "parser/graph.json"
    
    with open(file_path, "r") as graph_file:
        json_graph = json.load(graph_file)

    g = Graph()

    nodes_dict = {node["name"]: node for node in json_graph["nodes"]}

    for node in json_graph["nodes"]:
        g.add_node(node["name"], 0, node["type"]) #heuristic initialized at 0

    for edge in json_graph["edges"]:
        origin = nodes_dict.get(edge["origin"])
        destiny = nodes_dict.get(edge["destiny"])
        g.add_edge(edge["origin"], edge["destiny"], dist(origin, destiny), edge["speed"])

    return g

def dist(origin, destiny) -> float:
    latOr = origin["latitude"] * math.pi/180        #converted from decimal degrees to radians
    latDest = destiny["latitude"] * math.pi/180

    longOr = origin["longitude"] * math.pi/180
    longDest = destiny["longitude"] * math.pi/180

    #distance in kms - Haversine Formula (rounding up)
    distance = math.ceil(2 * 6371 * math.asin(math.sqrt(math.pow(math.sin((latDest - latOr)/2), 2) + math.cos(latOr)*math.cos(latDest)*math.pow(math.sin((longDest - longOr)/2),2))))

    return distance


