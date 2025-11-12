from typing_extensions import override

import math
from queue import Queue, PriorityQueue

import networkx as nx
import matplotlib.pyplot as plt

from .Node import Node
from .Color import Color
from Car import Car, ElectricCar, FuelCar

class Graph:
    def __init__(self):
        self.node_dict: dict[str, Node] = {}  
        self.adjacency_lists_dict: dict[str, list[tuple[str, int, int]]] = {}  
        self.heuristic_dict: dict[str, int] = {}
        self.type: str = ""

    @override
    def __str__(self) -> str:
        out = ""
        for key in self.adjacency_lists_dict.keys():
            out = out + "node: " + str(key) + ": " + str(self.adjacency_lists_dict[key]) + "\n"
        return out


    def get_node_by_name(self, name: str) -> Node|None:
        return self.node_dict.get(name)


    def str_edges(self) -> str:
        edge: str = ""
        for node in self.node_dict.keys():
            for (node2, cost, speed) in self.adjacency_lists_dict[node]:
                edge = edge + node + " -> " + node2 + " | cost: " + str(cost) + "\n"
        return edge


    def add_node(self, name: str, estimate: int, typeNode : str) -> None:
        node = Node(name, typeNode)
        self.node_dict[name] = node
        self.adjacency_lists_dict[name] = []
        self.heuristic_dict[name] = estimate


    def add_heuristic(self, node: str, estimate: int) -> None:
        if node in self.heuristic_dict.keys():
            self.heuristic_dict[node] = estimate
        else:
            raise KeyError("add_heuristic: node doesn't exist")


    def get_heuristic(self, node: str) -> int:
        if node in self.heuristic_dict.keys():
            return self.heuristic_dict[node]
        else:
            raise KeyError("get_heuristic: node doesn't exist")


    def add_edge(self, origin: str, destiny: str, dist: int, speed: int) -> None:
        n1 = self.get_node_by_name(origin)
        n2 = self.get_node_by_name(destiny)

        if n1 is None:
            raise KeyError(f"add_edge: {origin} doesn't exist")
        elif n2 is None:
            raise KeyError(f"add_edge: {destiny} doesn't exist")
        else:
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


    def get_neighbours(self, node: str) -> list[tuple[str, int, int]]:
        return self.adjacency_lists_dict[node]

    ###########################
    # desenha grafo modo grafico
    #########################

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

        parents: dict[str, str] = dict()
        parents[origin] = origin

        visited: set[str] = set()
        visited.add(origin)

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


    # for now it's a dijkstra
    def a_star_search(self, origin: str, destiny: str) -> tuple[list[str], int|float] | None:
        # the entries are of the form (priority_number, data)
        pqueue: PriorityQueue[tuple[int,str]] = PriorityQueue()
        pqueue.put((0, origin))

        # instead of putting WHITE in all nodes, if get() returns None then it's the same as WHITE (not visited)
        colors: dict[str,Color] = dict()
        colors[origin] = Color.GREY

        costs: dict[str,int] = dict()
        costs[origin] = 0

        parents: dict[str, str] = dict()
        parents[origin] = origin

        best_node = ""

        while not pqueue.empty():

            # get() will return the item with the lowest priority_number
            # in our case, the lowest cost (most attractive node)
            bn_cost, best_node = pqueue.get()
            colors[best_node] = Color.BLACK

            if best_node == destiny:
                break

            for node, dist, speed in self.get_neighbours(best_node):
                if colors.get(node) is None:
                    node_cost = bn_cost + dist
                    pqueue.put((node_cost, node))
                    colors[node] = Color.GREY
                    parents[node] = best_node
                    costs[node] = node_cost
                
                elif colors[node] == Color.GREY and bn_cost + dist < costs[node]:
                    parents[node] = best_node
                    costs[node] = costs[best_node] + dist

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



    # MUST BE UPDATED
    def procura_aStar(self, start, end, car: Car):
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
                if chosen_node is None or cost[queue_node] + self.get_heuristic(queue_node) < cost[chosen_node] + self.get_heuristic(chosen_node):
                    chosen_node = queue_node
            
            if chosen_node == end:
                break
            
            cost_chosen_node = cost[chosen_node]
          
            for neighbor, weight in self.get_neighbours(chosen_node):

                fuel_consumed = car.consumption(weight)
                remaining_fuel_if_move = remaining_fuel[chosen_node] - fuel_consumed
             
                if remaining_fuel_if_move < 0:
                    continue  # dont consider path if we cant make it

                if (self.get_node_by_name(neighbor).type == car.charges_in()):
                    remaining_fuel_if_move = 100

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
            return (path[end], self.calculate_cost(path[end]))
            
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
                if n == None or self.heuristic_dict[v] < self.heuristic_dict[n]:
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
