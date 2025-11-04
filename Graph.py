from typing_extensions import override

import math
from queue import Queue

import networkx as nx
import matplotlib.pyplot as plt

from Node import Node


class Graph:
    def __init__(self):
        self.node_dict: dict[str, Node] = {}  
        self.adjacency_lists_dict: dict[str, list[tuple[str, int]]] = {}  
        self.heuristic_dict: dict[str, int] = {}  

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
            for (node2, cost) in self.adjacency_lists_dict[node]:
                edge = edge + node + " -> " + node2 + " | cost: " + str(cost) + "\n"
        return edge


    def add_node(self, name: str, estimate: int) -> None:
        node = Node(name)
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


    def add_edge(self, node1: str, node2: str, weight: int) -> None:
        n1 = self.get_node_by_name(node1)
        n2 = self.get_node_by_name(node2)

        if n1 is None:
            raise KeyError("add_edge: node1 doesn't exist")
        elif n2 is None:
            raise KeyError("add_edge: node2 doesn't exist")
        else:
            self.adjacency_lists_dict[node1].append((node2, weight)) 


    def get_nodes(self) -> list[Node]:
        list = []
        for node in self.node_dict.values():
            list.append(node)

        return list


    def get_arc_cost(self, node1: str, node2: str) -> int|float:
        total_cost = math.inf
        adj_list = self.adjacency_lists_dict[node1]
        for (node, cost) in adj_list:
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


    def get_neighbours(self, node: str) -> list[tuple[str, int]]:
        neighbours = []
        for adj_wght in self.adjacency_lists_dict[node]:
            neighbours.append(adj_wght)
        return neighbours

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
            for (adjacent, weight) in self.adjacency_lists_dict[n]:
                list = (n, adjacent)
                # lista_a.append(lista)
                g.add_edge(n, adjacent, weight=weight)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()


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


    ##########################################
    #    A* - To Do
    ##########################################

    # MUST BE UPDATED
    def procura_aStar(self, start, end):
        queue = set()
        queue.add(start)
        visited = set()

        cost = {}
        cost[start] = 0

        parents = {}
        parents[start] = start

        while len(queue) > 0:
            n = None

            for v in queue:
                if n is None or cost[v] + self.get_heuristic(v) < cost[n] + self.get_heuristic(n):
                    n = v
            
            if n == end:
                break
            
            for m, weight in self.get_neighbours(n):
                if m not in queue and m not in visited:
                    queue.add(m)
                    parents[m] = n
                    cost[m] = cost[n] + weight

                elif cost[m] > cost[n] + weight:
                    cost[m] = cost[n] + weight
                    parents[m] = n

                    if m in visited:
                        visited.remove(m)
                        queue.add(m)

            queue.remove(n)
            visited.add(n)

        if parents.get(end) is not None:
            path = []

            while parents[n] != n:
                path.insert(0, n)
                n = parents[n]

            path.insert(0, start)

            return (path, self.calculate_cost(path))

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
