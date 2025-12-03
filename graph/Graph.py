from typing_extensions import override

import math
from queue import PriorityQueue
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt

from .Node import Node
from graph.Energy_Station import Energy_Station
from car.Car import Car, ElectricCar, FuelCar
import utils

class Graph:

    def __init__(self):
        self.node_dict: dict[str, Node] = {}  
        self.adjacency_lists_dict: dict[str, list[tuple[str, int, int]]] = {}  
        self.max_speed: int = 0

    def numberOfNodes(self):
        return len(self.node_dict)

    def numberOfEdges(self):
        total = 0
        for list in self.adjacency_lists_dict.values():
            total += len(list)
        return total

    def setMaxSpeed(self, speed: int):
        self.max_speed = speed


    def getMaxSpeed(self):
        return self.max_speed


    @override
    def __str__(self) -> str:
        out = ""
        for key in self.adjacency_lists_dict.keys():
            out = out + "node: " + str(key) + ": " + str(self.adjacency_lists_dict[key]) + "\n"
        return out


    def get_node_by_name(self, name: str) -> Node:
        node = self.node_dict.get(name)
        if node is None:
            raise KeyError(f"Node {name} doesn't exist")
        else:
            return node


    def str_edges(self) -> str:
        edge: str = ""
        for node in self.node_dict.keys():
            for (node2, dist, speed) in self.adjacency_lists_dict[node]:
                edge = edge + f"{node} -> {node2} | dist: {dist} | speed: {speed}\n"
        return edge


    def str_nodes(self) -> str:
        result: str = ""
        for name in self.node_dict.keys():
            node = self.get_node_by_name(name)
            result = result + f"{name} | ({node.getLatitude()}, {node.getLongitude()}) | {node.getType()}\n"
        return result


    def add_node(self, name: str, latitude: float, longitude: float, type_node: Energy_Station) -> None:
        node = Node(name, type_node, latitude, longitude)
        self.node_dict[name] = node
        self.adjacency_lists_dict[name] = []

        
    def add_edge(self, origin: str, destination: str, dist: int, speed: int) -> None:
        try:
            # just to make sure the nodes exist
            _ = self.get_node_by_name(origin)
            _ = self.get_node_by_name(destination)
        except KeyError:
            print(f"Couldn't add edge from {origin} to {destination}")

        self.adjacency_lists_dict[origin].append((destination, dist, speed)) 


    def get_nodes(self) -> list[Node]:
        list = []
        for node in self.node_dict.values():
            list.append(node)

        return list


    def get_arc_cost(self, node1: str, node2: str) -> float:
        total_cost = math.inf
        adj_list = self.adjacency_lists_dict[node1]
        for (node, dist, speed) in adj_list:
            if node == node2:
                total_cost = utils.calculate_time(dist, speed)

        return total_cost


    def get_arc_distance(self, node1: str, node2:str) -> int:
        total_cost = -1
        adj_list = self.adjacency_lists_dict[node1]
        for (node, dist, _) in adj_list:
            if node == node2:
                total_cost = dist

        return total_cost


    def calculate_cost(self, path: list[str]) -> float:
        cost = 0
        length = len(path)
        i = 0
        while i + 1 < length:
            cost = cost + self.get_arc_cost(path[i], path[i + 1])
            i += 1
        return cost

    
    def calculate_distance(self, path: list[str]) -> int:
        dist = 0
        length = len(path)
        i = 0
        while i + 1 < length:
            dist = dist + self.get_arc_distance(path[i], path[i + 1])
            i += 1
        return dist


    def calculate_heuristic(self, node1: str, node2: str) -> float:
        origin = self.get_node_by_name(node1)
        destination = self.get_node_by_name(node2)

        # this cast ensures types match
        # it shouldn't be a problem, since the result is in meters, so the decimal part is irrelevant
        straight_line_dist = int(utils.dist(origin.getLatitude(), origin.getLongitude(), destination.getLatitude(), destination.getLongitude()))

        return utils.calculate_time(straight_line_dist, self.getMaxSpeed())


    def get_neighbours(self, node: str) -> list[tuple[str, int, int]]:
        return self.adjacency_lists_dict[node]


    # draws the graph with arrows to indicate edge direction
    def draw_directed(self):
        # create directed graph
        g = nx.DiGraph()

        # add nodes and directed edges
        for nodo in self.node_dict.values():
            n = nodo.getName()
            g.add_node(n)
            for (adjacent, weight, _) in self.adjacency_lists_dict[n]:
                g.add_edge(n, adjacent, weight=weight)

        # layout and drawing
        pos = nx.spring_layout(g, seed=42)  # deterministic layout
        nx.draw_networkx_nodes(g, pos, node_size=700)
        nx.draw_networkx_labels(g, pos, font_weight='bold')

        # draw directed edges with arrows
        nx.draw_networkx_edges(
            g, pos,
            arrows=True,
            arrowstyle='-|>',
            arrowsize=20,
            connectionstyle='arc3,rad=0.1'  # slight curve for bidirectional edges
        )

        # show edge labels
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.axis('off')
        plt.tight_layout()
        plt.show()


    def draw(self):
        ##criar lista de vertices
        list_v = self.node_dict.values()
        list_a = []
        g = nx.Graph()
        for nodo in list_v:
            n = nodo.getName()
            g.add_node(n)
            for (adjacent, weight, _) in self.adjacency_lists_dict[n]:
                list = (n, adjacent)
                # lista_a.append(lista)
                g.add_edge(n, adjacent, weight=weight)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()


    def BFS_search(self, origin: str, destination: str) -> tuple[list[str], float, int]|None:

        queue: deque[str] = deque()
        queue.append(origin)

        parents: dict[str, str] = {origin: origin}

        visited: set[str] = {origin}

        while queue:

            current = queue.popleft()

            if current == destination:
                path: list[str] = self.build_path(parents, origin, destination)
                return (path, self.calculate_cost(path), self.calculate_distance(path))

            for node, _, _ in self.get_neighbours(current):
                if node not in visited:
                    visited.add(node)
                    queue.append(node)
                    parents[node] = current
        
        # if we exit the cycle, it means the destination wasn't found
        print(f"Path not found for origin {origin} and destination {destination}")
        return None


    def DFS_search(self, origin: str, destination: str) -> tuple[list[str], float, int]|None:
        
        stack: list[str] = [origin]

        parents: dict[str, str] = {origin: origin}

        visited: set[str] = set()

        while stack:
            current = stack.pop()

            if current == destination:
                path: list[str] = self.build_path(parents, origin, destination)
                return (path, self.calculate_cost(path), self.calculate_distance(path))

            if current not in visited:
                visited.add(current)
                for node, _, _ in self.get_neighbours(current):
                    stack.append(node)
                    parents[node] = current

        # if we exit the cycle, it means the destination wasn't found
        print(f"Path not found for origin {origin} and destination {destination}")
        return None



    def find_closest_station(self, origin: str, station_type: Energy_Station) -> tuple[list[str], float, int]|None:
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[float,str]] = PriorityQueue()
        pqueue.put((0, origin))

        # the cost is in minutes (calculated based on distance (kms) and speed (kms/h))
        costs: dict[str,float] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            if bn_cost > costs[best_node]:
                continue

            # stop if the node has the same type as the requested one
            # if the node is CHARGING_AND_FUEL_STATION it satisfies both types, so we can also stop
            bn_type = self.get_node_by_name(best_node).getType()
            if bn_type == station_type or bn_type == Energy_Station.CHARGING_AND_FUEL_STATION:
                path: list[str] = self.build_path(parents, origin, best_node)
                return (path, bn_cost, self.calculate_distance(path))

            for node, dist, speed in self.get_neighbours(best_node):
                travel_time = utils.calculate_time(dist, speed)
                new_cost = costs[best_node] + travel_time

                if node not in costs or new_cost < costs[node]:
                    costs[node] = new_cost
                    parents[node] = best_node
                    pqueue.put((new_cost, node))

        # if we exit the cycle, it means no station was found
        print(f"Couldn't find any station from {origin}")
        return None


    def find_closest_car(self, origin: str, cars: set[str]) -> tuple[list[str], float, int]|None:
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[float,str]] = PriorityQueue()
        pqueue.put((0, origin))

        # the cost is in minutes (calculated based on distance (kms) and speed (kms/h))
        costs: dict[str,float] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            if bn_cost > costs[best_node]:
                continue

            # stop if the node has an available car
            # for that, it's just necessary to check if the current node is in the provided set
            if best_node in cars:
                path: list[str] = self.build_path(parents, origin, best_node)
                return (path, bn_cost, self.calculate_distance(path))

            for node, dist, speed in self.get_neighbours(best_node):
                travel_time = utils.calculate_time(dist, speed)
                new_cost = costs[best_node] + travel_time

                if node not in costs or new_cost < costs[node]:
                    costs[node] = new_cost
                    parents[node] = best_node
                    pqueue.put((new_cost, node))

        # if we exit the cycle, it means no available cars were found
        print(f"Couldn't find any available car from {origin}")
        return None
        


    def dijkstra_search(self, origin: str, destination: str) -> tuple[list[str], float, int] | None:
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[float,str]] = PriorityQueue()
        pqueue.put((0, origin))

        # the cost is in minutes (calculated based on distance (ms) and speed (kms/h))
        costs: dict[str,float] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            if bn_cost > costs[best_node]:
                continue

            if best_node == destination:
                path: list[str] = self.build_path(parents, origin, destination)
                return (path, bn_cost, self.calculate_distance(path))

            for node, dist, speed in self.get_neighbours(best_node):
                travel_time = utils.calculate_time(dist, speed)
                new_cost = costs[best_node] + travel_time

                if node not in costs or new_cost < costs[node]:
                    costs[node] = new_cost
                    parents[node] = best_node
                    pqueue.put((new_cost, node))

        # if we exit the cycle, it means the destination wasn't found
        print(f"Path not found for origin {origin} and destination {destination}")
        return None


    def a_star_search(self, origin: str, destination: str) -> tuple[list[str], float, int] | None:
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[float,str]] = PriorityQueue()
        pqueue.put((self.calculate_heuristic(origin, destination), origin))

        # the cost is in minutes (calculated based on distance (kms) and speed (kms/h))
        # heuristics must not be considered here
        costs: dict[str,float] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            if bn_cost > costs[best_node] + self.calculate_heuristic(best_node, destination):
                continue

            if best_node == destination:
                path: list[str] = self.build_path(parents, origin, destination)
                # here we can't return bn_cost because it has the heuristic value included
                return (path, costs[destination], self.calculate_distance(path))

            for node, dist, speed in self.get_neighbours(best_node):
                travel_time = utils.calculate_time(dist, speed)
                new_cost = costs[best_node] + travel_time

                if node not in costs or new_cost < costs[node]:
                    costs[node] = new_cost
                    parents[node] = best_node
                    pqueue.put((new_cost + self.calculate_heuristic(node, destination), node))

        # if we exit the cycle, it means the destination wasn't found
        print(f"Path not found for origin {origin} and destination {destination}")
        return None


    def greedy_search(self, origin: str, destination: str) -> tuple[list[str], float, int] | None:
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[float,str]] = PriorityQueue()
        pqueue.put((self.calculate_heuristic(origin, destination), origin))

        parents: dict[str, str] = {origin: origin}

        visited: set[str] = {origin}

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            _, best_node = pqueue.get()

            if best_node == destination:
                path: list[str] = self.build_path(parents, origin, destination)
                return (path, self.calculate_cost(path), self.calculate_distance(path))

            for node, _, _ in self.get_neighbours(best_node):
                if node not in visited:
                    visited.add(node)
                    pqueue.put((self.calculate_heuristic(node, destination), node))
                    parents[node] = best_node

        # if we exit the cycle, it means the destination wasn't found
        print(f"Path not found for origin {origin} and destination {destination}")
        return None


    def build_path(self, parents: dict[str, str], origin: str, destination: str) -> list[str]:
        path: list[str] = list()

        while parents[destination] != destination:
            path.insert(0, destination)
            destination = parents[destination]

        path.insert(0, origin)

        return path
