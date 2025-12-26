from typing_extensions import override

import math
from queue import PriorityQueue
from collections import deque
import random

import networkx as nx
import matplotlib.pyplot as plt

from .Node import Node
from graph.Energy_Station import Energy_Station
from car.Car import Car
import utils

class Graph:
    ALGORITHM = "A_STAR" # A star is default

    def __init__(self):
        self.node_dict: dict[str, Node] = {}  
        self.adjacency_lists_dict: dict[str, list[tuple[str, int, int]]] = {}  
        self.max_speed: int = 0
        # this dict stores heuristics as they're calculated in order to save time
        self.heuristics_time: dict[tuple[str,str], float] = {}
        self.heuristics_dist: dict[tuple[str,str], int] = {}

    def number_of_nodes(self):
        return len(self.node_dict)

    def number_of_edges(self):
        total = 0
        for list in self.adjacency_lists_dict.values():
            total += len(list)
        return total

    def set_max_speed(self, speed: int):
        self.max_speed = speed


    def get_max_speed(self):
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

    def get_random_node_name(self) -> str:
        if not self.node_dict:
            raise ValueError("The graph is empty; no nodes to select.")
        return random.choice(list(self.node_dict.keys()))

    def node_exists(self, name: str) -> bool:
        if self.node_dict.get(name) is None:
            return 0
        return 1
    
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


    def get_arc_time(self, node1: str, node2: str) -> float:
        total_cost = math.inf
        adj_list = self.adjacency_lists_dict[node1]
        for (node, dist, speed) in adj_list:
            if node == node2:
                total_cost = utils.calculate_time(dist, speed)

        return total_cost

    def get_arc_speed (self, node1: str, node2: str) -> int:
        total_speed = math.inf
        adj_list = self.adjacency_lists_dict[node1]
        for (node, _, speed) in adj_list:
            if node == node2:
                total_speed = speed
                break

        return total_speed


    def get_arc_distance(self, node1: str, node2:str) -> int:
        total_cost = math.inf
        adj_list = self.adjacency_lists_dict[node1]
        for (node, dist, _) in adj_list:
            if node == node2:
                total_cost = dist

        return total_cost


    def calculate_path_time(self, path: list[str]) -> float:
        cost = 0
        length = len(path)
        i = 0
        while i + 1 < length:
            cost = cost + self.get_arc_time(path[i], path[i + 1])
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


    def calculate_heuristic_time(self, node1: str, node2: str) -> float:
        # check if this heuristic was already calculated
        stored = self.heuristics_time.get((node1, node2))

        if stored is not None:
            return stored

        origin = self.get_node_by_name(node1)
        destination = self.get_node_by_name(node2)

        # this cast ensures types match
        # it shouldn't be a problem, since the result is in meters, so the decimal part is irrelevant
        straight_line_dist = int(utils.dist(origin.getLatitude(), origin.getLongitude(), destination.getLatitude(), destination.getLongitude()))

        time = utils.calculate_time(straight_line_dist, self.get_max_speed())
        # save the value for future use
        self.heuristics_time[(node1, node2)] = time

        return time

    def calculate_heuristic_dist(self, node1: str, node2: str) -> int:
        # check if this heuristic was already calculated
        stored = self.heuristics_dist.get((node1, node2))

        if stored is not None:
            return stored

        origin = self.get_node_by_name(node1)
        destination = self.get_node_by_name(node2)

        # this cast ensures types match
        # it shouldn't be a problem, since the result is in meters, so the decimal part is irrelevant
        straight_line_dist = int(utils.dist(origin.getLatitude(), origin.getLongitude(), destination.getLatitude(), destination.getLongitude()))

        # save the value for future use
        self.heuristics_dist[(node1, node2)] = straight_line_dist

        return straight_line_dist
    


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
                return (path, self.calculate_path_time(path), self.calculate_distance(path))

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
                return (path, self.calculate_path_time(path), self.calculate_distance(path))

            if current not in visited:
                visited.add(current)
                for node, _, _ in self.get_neighbours(current):
                    if node not in visited:
                        stack.append(node)
                        parents[node] = current

        # if we exit the cycle, it means the destination wasn't found
        print(f"Path not found for origin {origin} and destination {destination}")
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
        pqueue.put((self.calculate_heuristic_time(origin, destination), origin))

        # the cost is in minutes (calculated based on distance (ms) and speed (kms/h))
        # heuristics must not be considered here
        costs: dict[str,float] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            if bn_cost > costs[best_node] + self.calculate_heuristic_time(best_node, destination):
                continue

            if best_node == destination:
                path: list[str] = self.build_path(parents, origin, destination)
                # here we can't return bn_cost because it has the heuristic value included
                # use costs[destination] instead
                return (path, costs[destination], self.calculate_distance(path))

            for node, dist, speed in self.get_neighbours(best_node):
                travel_time = utils.calculate_time(dist, speed)
                new_cost = costs[best_node] + travel_time

                if node not in costs or new_cost < costs[node]:
                    costs[node] = new_cost
                    parents[node] = best_node
                    pqueue.put((new_cost + self.calculate_heuristic_time(node, destination), node))

        # if we exit the cycle, it means the destination wasn't found
        print(f"Path not found for origin {origin} and destination {destination}")
        return None


    def a_star_search_by_distance(self, origin: str, destination: str) -> tuple[list[str], int] | None:
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[int,str]] = PriorityQueue()
        pqueue.put((self.calculate_heuristic_dist(origin, destination), origin))

        # the cost is in meters
        # heuristics must not be considered here
        costs: dict[str,int] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            if bn_cost > costs[best_node] + self.calculate_heuristic_dist(best_node, destination):
                continue

            if best_node == destination:
                path: list[str] = self.build_path(parents, origin, destination)
                # here we can't return bn_cost because it has the heuristic value included
                # use costs[destination] instead
                return (path, costs[destination])

            for node, dist, _ in self.get_neighbours(best_node):
                new_cost = costs[best_node] + dist

                if node not in costs or new_cost < costs[node]:
                    costs[node] = new_cost
                    parents[node] = best_node
                    pqueue.put((new_cost + self.calculate_heuristic_dist(node, destination), node))

        # if we exit the cycle, it means the destination wasn't found
        print(f"Path not found for origin {origin} and destination {destination}")
        return None


    def greedy_search(self, origin: str, destination: str) -> tuple[list[str], float, int] | None:
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[float,str]] = PriorityQueue()
        pqueue.put((self.calculate_heuristic_time(origin, destination), origin))

        parents: dict[str, str] = {origin: origin}

        visited: set[str] = {origin}

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            _, best_node = pqueue.get()

            if best_node == destination:
                path: list[str] = self.build_path(parents, origin, destination)
                return (path, self.calculate_path_time(path), self.calculate_distance(path))

            for node, _, _ in self.get_neighbours(best_node):
                if node not in visited:
                    visited.add(node)
                    pqueue.put((self.calculate_heuristic_time(node, destination), node))
                    parents[node] = best_node

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


    # this is used to find the closest station by op cost; just need to multiply the distance returned by this by a car's op cost 
    def find_closest_station_by_distance(self, origin: str, station_type: Energy_Station) -> tuple[list[str], float, int]|None:
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[int,str]] = PriorityQueue()
        pqueue.put((0, origin))

        # the cost is in minutes (calculated based on distance (kms) and speed (kms/h))
        dists: dict[str,int] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            if bn_cost > dists[best_node]:
                continue

            # stop if the node has the same type as the requested one
            # if the node is CHARGING_AND_FUEL_STATION it satisfies both types, so we can also stop
            bn_type = self.get_node_by_name(best_node).getType()
            if bn_type == station_type or bn_type == Energy_Station.CHARGING_AND_FUEL_STATION:
                path: list[str] = self.build_path(parents, origin, best_node)
                return (path, self.calculate_path_time(path), bn_cost)

            for node, dist, _ in self.get_neighbours(best_node):
                new_dist = dists[best_node] + dist

                if node not in dists or new_dist < dists[node]:
                    dists[node] = new_dist
                    parents[node] = best_node
                    pqueue.put((new_dist, node))

        # if we exit the cycle, it means no station was found
        print(f"Couldn't find any station from {origin}")
        return None

    def find_closest_car(self, origin: str, cars: set[Car]) -> tuple[list[str], float, int]|None:
        car_nodes: set[str] = set()
        for car in cars:
            car_nodes.add(car.curr_node)

        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[float,str]] = PriorityQueue()
        # calculate heuristic for the first node
        min_heuristic = 10000000000
        for car_node in car_nodes:
            heuristic = self.calculate_heuristic_time(origin, car_node)
            if heuristic < min_heuristic:
                min_heuristic = heuristic
        pqueue.put((min_heuristic, origin))

        # seconds
        times: dict[str, float] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            # calculate heuristic, which is the minimum for every car node
            min_heuristic = 10000000000
            for car_node in car_nodes:
                heuristic = self.calculate_heuristic_time(best_node, car_node)
                if heuristic < min_heuristic:
                    min_heuristic = heuristic
            if bn_cost > times[best_node] + min_heuristic:
                continue

            if best_node in car_nodes:
                path: list[str] = self.build_path(parents, origin, best_node)
                return (path, times[best_node], self.calculate_distance(path))

            for node, dist, speed in self.get_neighbours(best_node):
                travel_time = utils.calculate_time(dist, speed)
                new_time = times[best_node] + travel_time

                if node not in times or new_time < times[node]:
                    times[node] = new_time
                    parents[node] = best_node
                    # calculate heuristic, which is the minimum for every car node
                    min_heuristic = 10000000000
                    for car_node in car_nodes:
                        heuristic = self.calculate_heuristic_time(node, car_node)
                        if heuristic < min_heuristic:
                            min_heuristic = heuristic
                    pqueue.put((new_time + min_heuristic, node))

        # if we exit the cycle, it means no available cars were found
        print(f"Couldn't find any available car from {origin}")
        return None


    # result[2] is the operational cost; must be divided by the chosen car's operational cost per km to get the distance
    def find_closest_car_by_op_cost(self, origin: str, cars: set[Car]) -> tuple[list[str], float, int]|None:
        car_nodes_opcosts: dict[str, int] = {}
        for car in cars:
            car_nodes_opcosts[car.curr_node] = car.op_cost_km

        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[int,str]] = PriorityQueue()
        # calculate heuristic for the first node
        min_heuristic = 10000000000
        for car_node in car_nodes_opcosts.keys():
            heuristic = self.calculate_heuristic_dist(origin, car_node)
            if heuristic < min_heuristic:
                min_heuristic = heuristic
        pqueue.put((min_heuristic, origin))

        # meters
        dists: dict[str,int] = {origin: 0}

        parents: dict[str, str] = {origin: origin}

        # [(path, op cost)]
        results: list[tuple[list[str], int]] = []

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()

            # skip stale entries
            # calculate heuristic, which is the minimum for every car node
            min_heuristic = 10000000000
            for car_node in car_nodes_opcosts.keys():
                heuristic = self.calculate_heuristic_dist(best_node, car_node)
                if heuristic < min_heuristic:
                    min_heuristic = heuristic
            if bn_cost > dists[best_node] + min_heuristic:
                continue

            if best_node in car_nodes_opcosts.keys():
                car_op_cost = car_nodes_opcosts.pop(best_node)
                op_cost: int = dists[best_node] * car_op_cost // 1000
                path: list[str] = self.build_path(parents, origin, best_node)
                results.append((path, op_cost))
                # already found every car, so break the cicle
                if not car_nodes_opcosts:
                    break

            for node, dist, _ in self.get_neighbours(best_node):
                new_dist = dists[best_node] + dist

                if node not in dists or new_dist < dists[node]:
                    dists[node] = new_dist
                    parents[node] = best_node
                    # calculate heuristic, which is the minimum for every car node
                    min_heuristic = 10000000000
                    for car_node in car_nodes_opcosts.keys():
                        heuristic = self.calculate_heuristic_dist(node, car_node)
                        if heuristic < min_heuristic:
                            min_heuristic = heuristic
                    pqueue.put((new_dist + min_heuristic, node))

        if results:
            best_result: tuple[list[str], int] = ([], 100000000000)
            for result in results:
                if result[1] < best_result[1]:
                    best_result = result
            return (best_result[0], self.calculate_path_time(best_result[0]), best_result[1])
        else:
            # if we reach here, it means no available cars were found
            print(f"Couldn't find any available car from {origin}")
            return None


    def build_path(self, parents: dict[str, str], origin: str, destination: str) -> list[str]:
        path: list[str] = list()

        while parents[destination] != destination:
            path.insert(0, destination)
            destination = parents[destination]

        path.insert(0, origin)

        return path

    
    def find_longest_route(self, origin: str) -> tuple[str, str]:
        longest_route: tuple[str, str] = ("","")
        max_path_len = 0

        for destination in self.node_dict.keys():
            search_result = self.a_star_search(origin, destination)
            if search_result is not None:
                path_len = len(search_result[0])
                if path_len > max_path_len:
                    max_path_len = path_len
                    longest_route = (origin, destination)
                    print(f"New max found ({max_path_len}) for nodes {origin} and {destination}")

        return longest_route


    # returns in minutes
    def calc_time_between_nodes(self, curr_node: str, goal_node : str) -> float:
            distance = self.get_arc_distance(curr_node, goal_node) # in meters
            speed = self.get_arc_speed(curr_node, goal_node)       # in km/h
            if (distance == math.inf or speed == math.inf):
                print (f"Path not found when calculating time: {curr_node} - {goal_node}")
                return 0

            time = distance / 1000 / speed * 60
            return time

    def get_algorithm(self):
        match (self.ALGORITHM):
            case ("DFS"):
                return self.DFS_search
            case ("BFS"):
                return self.BFS_search
            case ("DIJKSTRA"):
                return self.dijkstra_search
            case ("GREEDY"):
                return self.greedy_search
            case ("A_STAR"):
                return self.a_star_search
            case (_):
                print ("unknown algorithm") # shouldnt happen
                return None

    # uses the car's current node as the starting point to create the path 
    def create_path_to_client(self, car, client) -> tuple[list[str], float, int] | None:
        return self.create_path_to_client_and_goal(car, client, car.curr_node)


    # updates a path that already started
    def update_path(self, car, client, last_completed_node: str) -> tuple[list[str], float, int] | None:    
        if not client.is_in_car:
            return self.create_path_to_client_and_goal(car, client, last_completed_node)
        else:
            return self.path_to_goal(car, client, last_completed_node)

        
    # creates the entire path from the given origin node to the client and then to the goal
    def create_path_to_client_and_goal(self, car, client, origin_node: str) -> tuple[list[str], float, int] | None:
        if client.how_many > car.capacity - car.passengers_inside:
            print("No capacity!") 
            return None

        algorithm = self.get_algorithm()
        if algorithm is None:
            return None

        # Car to Client 
        to_client = algorithm(origin_node, client.start)
        if to_client is None:
            print(f"Can't get from {origin_node} to client {client.start}!")
            return None
        to_client_path, to_client_time, to_client_dist = to_client

        if not utils.is_trip_feasible(car, to_client_dist, car.energy_level):
            print("Runs out of fuel going to client!")
            return None

        # Client to Goal
        to_goal = algorithm(client.start, client.goal)
        if to_goal is None:
            print(f"Can't deliver client from {client.start} to goal {client.goal}!")
            return None
        to_goal_path, to_goal_time, to_goal_dist = to_goal
        

        total_dist_meters = to_client_dist + to_goal_dist
        if not utils.is_trip_feasible(car, total_dist_meters, car.energy_level):
            print("Runs out of fuel delivering client!")
            return None

        total_time = to_client_time + to_goal_time
        
        if to_goal_path and to_goal_path[0] == client.start and len(to_goal_path[0])>2: 
            to_goal_path.pop(0) # remove head of list, since itll be redundant 
            
        total_path = to_client_path + to_goal_path

        return total_path, total_time, total_dist_meters


    # gives the path from the origin node to the client's goal
    def path_to_goal(self, car, client, origin_node: str) -> tuple[list[str], float, int] | None:
        algorithm = self.get_algorithm()
        if algorithm is None:
            return None

        to_goal = algorithm(origin_node, client.goal)
        if to_goal is None:
            print(f"Can't find a path from {origin_node} to goal {client.goal}!")
            return None
        
        path, time, dist = to_goal
        
        if not utils.is_trip_feasible(car, dist, car.energy_level):
            print("Runs out of fuel on the way to the goal!")
            return None
            
        if path and path[0] == origin_node and len(path)>2: 
            path.pop(0)                     # remove head of list, since itll be redundant 

        return path, time, dist
