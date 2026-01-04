import random
import utils
from Client import Client

class Client_Controller:
    central_popular_node : str = None           # the closest node to the most visited nodes averages

    sum_starting_coordinates = [0.0, 0.0] # lat, lng; sum of coords the clients started in
    how_many_clients : int = 0                     # counter of how many clients have requested a ride

    sum_waiting_time : int = 0

    def __init__(self, dynamic_client: bool, roam : bool, graph):
        self.waiting_clients : list [Client] = [] # swap for a priority queue?
        self.clients_on_route : list [Client] = []
        self.dynamic_client = dynamic_client

        self.waiting_clients.extend (self.get_clients(graph))
        if roam:
            self.calculate_central_node(graph)

    def update(self, curr_time, graph, roam : bool):
        for client in self.waiting_clients:
            Client_Controller.sum_waiting_time += 1

        if self.dynamic_client is True:
            spawn_chance = 0.2 # 20% chance of spawning a new client

            if random.random() < spawn_chance:
                nodes = list(graph.node_dict.keys())
                start_node = random.choice(nodes)

                nodes.remove(start_node) # ensures the goal node won't be the same as the start
                goal_node = random.choice(nodes)

                num_passengers = random.randint(1, 4)

                wants_green = random.random() < 0.3 # 30% want an electric car

                is_premium = random.random() < 0.2 # 20% premium
                
                new_client = Client(start_node, goal_node, num_passengers, wants_green, is_premium)

                self.waiting_clients.append(new_client)
                self.waiting_clients.sort(key=lambda c: not c.is_premium)

                Client_Controller.how_many_clients += 1

                if roam: 
                    node_start = graph.get_node_by_name (new_client.start)
                    Client_Controller.sum_starting_coordinates[0] += node_start.getLatitude()
                    Client_Controller.sum_starting_coordinates[1] += node_start.getLongitude()

                    self.calculate_central_node(graph)

                print(f"\n[NEW CLIENT] {new_client}\n")

    def client_got_car_assigned (self, client: Client):
        self.waiting_clients.remove(client)
        self.clients_on_route.append(client)

    def client_arrived_at_goal (self, client: Client):
        self.clients_on_route.remove(client)

    def get_clients(self, graph) -> list [Client]: # manual method to add clients, for testing
        #c1 = Client ("Alandroal", "Monsaraz", 4)
        #c2 = Client ("Palmela", "Lisboa", 3)

        clients = []
        for c in clients:
            node_start = graph.get_node_by_name (c.start)
            Client_Controller.sum_starting_coordinates[0] += node_start.getLatitude()
            Client_Controller.sum_starting_coordinates[1] += node_start.getLongitude()
        Client_Controller.how_many_clients += len(clients)
        return clients

    def get_n_waiting_clients (self):
        return len(self.waiting_clients)

    def see_waiting_clients (self):
        i = 0
        for client in self.waiting_clients:
            print("Client", i, ":", end=" ")
            print(client)
            i += 1

    def see_clients_on_route (self):
        i = 0
        for client in self.clients_on_route:
            print("Client", i, ":", end=" ")
            print(client)
            i += 1

    def add_client (self, client_start: str, client_goal: str, client_how_many: int):
        client = Client(client_start, client_goal, client_how_many)
        self.waiting_clients.append(client)

    def delete_client(self, index: int):
        self.waiting_clients.pop(index)

    def change_client(self, index: int, client_start: str, client_goal: str, client_how_many: int):
        new_client = Client(client_start, client_goal, client_how_many)
        self.waiting_clients[index] = new_client

    def calculate_central_node (self, graph):
        if Client_Controller.how_many_clients == 0:
            return None
        lat, lng = Client_Controller.sum_starting_coordinates
        lat_avg = lat / Client_Controller.how_many_clients
        lng_avg = lng / Client_Controller.how_many_clients

        closest_node = "" 
        closest_dist = float("inf")
        for node in graph.node_dict.values():
            dist = utils.dist(node.getLatitude(), node.getLongitude(), lat_avg, lng_avg)
            if dist < closest_dist:
                closest_node = node.name
                closest_dist = dist

        print ("central node ", closest_node)
        Client_Controller.central_popular_node = closest_node
