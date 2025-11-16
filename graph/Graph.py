from typing_extensions import override

import math
from queue import Queue, PriorityQueue

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

        
    def add_edge(self, origin: str, destiny: str, dist: int, speed: int) -> None:
        try:
            # just to make sure the nodes exist
            _ = self.get_node_by_name(origin)
            _ = self.get_node_by_name(destiny)
        except KeyError:
            print(f"Couldn't add edge from {origin} to {destiny}")

        self.adjacency_lists_dict[origin].append((destiny, dist, speed)) 


    def get_nodes(self) -> list[Node]:
        list = []
        for node in self.node_dict.values():
            list.append(node)

        return list


    def get_arc_cost(self, node1: str, node2: str) -> int|float:
        total_cost = math.inf
        adj_list = self.adjacency_lists_dict[node1]
        for (node, cost, _) in adj_list:
            if node == node2:
                total_cost = cost

        return total_cost


    def calculate_cost(self, path: list[str]) -> int|float:
        cost = 0
        length = len(path)
        i = 0
        while i + 1 < length:
            cost = cost + self.get_arc_cost(path[i], path[i + 1])
            i += 1
        return cost

    def calculate_heuristic(self, node1: str, node2: str) -> float:
        origin = self.get_node_by_name(node1)
        destination = self.get_node_by_name(node2)

        return utils.dist(origin.getLatitude(), origin.getLongitude(), destination.getLatitude(), destination.getLongitude())

    def get_neighbours(self, node: str) -> list[tuple[str, int, int]]:
        return self.adjacency_lists_dict[node]


    # draws a directed graph
    def draw(self):
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


    def desenha(self):
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


    def BFS_search(self, origin: str, dest: str) -> tuple[list[str], int|float]|None:

        queue: Queue[str] = Queue()
        queue.put(origin)

        parents: dict[str, str] = {origin: origin}

        visited: set[str] = {origin}

        while not queue.empty():

            current = queue.get()

            if current == dest:
                break

            for node, _, _ in self.get_neighbours(current):
                if node not in visited:
                    visited.add(node)
                    queue.put(node)
                    parents[node] = current

        if parents.get(dest) is None:
                return None
    
        current = dest

        path = []
        while True:
            path.insert(0, current)

            parent = parents[current]

            if parent == current:
                break

            current = parent

        return path, self.calculate_cost(path)
            


    ################################################################################
    # Procura DFS
    ################################################################################

    # recursive DFS, returns (path, cost) --> ([string], int)
    def procura_DFS(self, start, end, path=[], visited=set()):
        path.append(start)
        visited.add(start)

        if start == end:
            cost = self.calculate_cost(path)
            return (path, cost)

        for (adjacent, weight) in self.adjacency_lists_dict[start]:
            if adjacent not in visited:
                result = self.procura_DFS(adjacent, end, path, visited)
                if result is not None:
                    return result
        path.pop()
        return None


    def find_closest_station(self, origin: str, station_type: Energy_Station):
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[int,str]] = PriorityQueue()
        pqueue.put((0, origin))

        # the cost is in minutes (calculated based on distance (kms) and speed (kms/h))
        costs: dict[str,int] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        best_node = ""
        station = ""

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            if bn_cost > costs[best_node]:
                continue

            # stop if the node has the same type as the requested one
            # if the node is CHARGING_AND_FUEL_STATION it satisfies both types, so we can also stop
            if self.get_node_by_name(best_node).getType() == station_type or station_type == Energy_Station.CHARGING_AND_FUEL_STATION:
                station = best_node
                break

            for node, dist, speed in self.get_neighbours(best_node):
                travel_time = utils.calculate_time(dist, speed)
                new_cost = costs[best_node] + travel_time

                if node not in costs or new_cost < costs[node]:
                    costs[node] = new_cost
                    parents[node] = best_node
                    pqueue.put((new_cost, node))

        n = best_node
        # if it's None, it means we never entered the cicle's break condition, so we didn't find our destiny
        if parents.get(station) is not None:
            path: list[str] = list()

            while parents[n] != n:
                path.insert(0, n)
                n = parents[n]

            path.insert(0, origin)

            return (path, self.calculate_cost(path))
        
        else:
            print(f"Couldn't find any station from {origin}")
            return None
        


    def dijkstra_search(self, origin: str, destiny: str) -> tuple[list[str], int|float] | None:
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[int,str]] = PriorityQueue()
        pqueue.put((0, origin))

        # the cost is in minutes (calculated based on distance (kms) and speed (kms/h))
        costs: dict[str,int] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        best_node = ""

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            if bn_cost > costs[best_node]:
                continue

            if best_node == destiny:
                break

            for node, dist, speed in self.get_neighbours(best_node):
                travel_time = utils.calculate_time(dist, speed)
                new_cost = costs[best_node] + travel_time

                if node not in costs or new_cost < costs[node]:
                    costs[node] = new_cost
                    parents[node] = best_node
                    pqueue.put((new_cost, node))

        n = best_node
        # if it's None, it means we never entered the cicle's break condition, so we didn't find our destiny
        if parents.get(destiny) is not None:
            path: list[str] = list()

            while parents[n] != n:
                path.insert(0, n)
                n = parents[n]

            path.insert(0, origin)

            return (path, self.calculate_cost(path))
        
        else:
            print(f"Path not found for origin {origin} and destiny {destiny}")
            return None



    def procura_aStar(self, start, end, car: Car, can_refuel : bool = False) -> tuple[list[str], int, float]:
        queue = set()
        queue.add(start)
        visited = set()

        cost = {}
        cost[start] = 0

        remaining_fuel = {}
        remaining_fuel[start] = car.energy_level

        path = {}
        path[start] = [start]

        while len(queue) > 0:
            chosen_node = None

            for queue_node in queue:
                if chosen_node is None or cost[queue_node] + self.calculate_heuristic(queue_node, end) < cost[chosen_node] + self.calculate_heuristic(chosen_node, end):
                    chosen_node = queue_node
            
            if chosen_node == end:
                break
            
            cost_chosen_node = cost[chosen_node]

            for neighbor, weight, _ in self.get_neighbours(chosen_node):

                fuel_consumed = car.consumption(weight)
                remaining_fuel_if_move = remaining_fuel[chosen_node] - fuel_consumed
             
                if remaining_fuel_if_move < 0:
                    continue  # dont consider path if we cant make it

                if can_refuel:
                    node_type = self.get_node_by_name(neighbor).type
                    if (node_type == car.charges_in() or node_type == Energy_Station.CHARGING_AND_FUEL_STATION):
                        remaining_fuel_if_move = 100            # currently refueling even if it doesnt *need* to

                new_path = path[chosen_node].copy()
                new_path.append(neighbor)

                if neighbor not in queue and neighbor not in visited:
                    queue.add(neighbor)
                    
                    cost[neighbor] = cost_chosen_node + weight

                    path[neighbor] = new_path
                    remaining_fuel[neighbor] = remaining_fuel_if_move

                # reconsider a visited node if the cost or fuel is now better 
                elif cost[neighbor] > cost_chosen_node + weight or remaining_fuel[neighbor] <= remaining_fuel_if_move:
                    cost[neighbor] = cost_chosen_node + weight
                    
                    remaining_fuel[neighbor] = remaining_fuel_if_move
                    path[neighbor] = new_path

                    if neighbor in visited:
                        visited.remove(neighbor)
                        queue.add(neighbor)

            queue.remove(chosen_node)
            visited.add(chosen_node)

        if end in path:
            return (path[end], self.calculate_cost(path[end]), remaining_fuel[end])
            
        print('Path does not exist!')
        return None


    ##########################################
    #   Greedy - To Do
    ##########################################


    # MUST BE UPDATED
    def greedy(self, start, end):
        queue = set()
        queue.add(start)
        visited = set()

        parents = {}
        parents[start] = start

        while len(queue) > 0:
            n = None

            for v in queue:
                if n == None or self.calculate_heuristic(v, end) < self.calculate_heuristic(n, end):
                    n = v

            if n == end:
                break

            for m, _ in self.get_neighbours(n):
                if m not in queue and m not in visited:
                    queue.add(m)
                    parents[m] = n

            queue.remove(n)
            visited.add(n)

        if parents.get(end) is not None:
            path = []

            while parents[n] != n:
                path.insert(0, n)
                n = parents[n]

            path.insert(0, start)

            return (path, self.calculate_cost(path))

        print("Path does not exist!")
        return None
