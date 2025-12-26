import random

from Client import Client

class Client_Controller:
    def __init__(self, dynamic_client: bool):
        self.waiting_clients : list [Client] = [] # swap for a priority queue?
        self.clients_on_route : list [Client] = []
        self.dynamic_client = dynamic_client

        self.waiting_clients.extend (self.get_clients())

    def update(self, curr_time, graph):
        if self.dynamic_client is True:
            spawn_chance = 0.2 # 20% chance of spawning a new client

            if random.random() < spawn_chance:
                nodes = list(graph.node_dict.keys())
                start_node = random.choice(nodes)

                nodes.remove(start_node) # ensures the goal node won't be the same as the start
                goal_node = random.choice(nodes)

                num_passengers = random.randint(1, 4)

                new_client = Client(start_node, goal_node, num_passengers)

                self.waiting_clients.append(new_client)

                print(f"\n[NEW CLIENT] {new_client}\n")

    def client_got_in_car (self, client: Client):
        self.waiting_clients.remove(client)
        self.clients_on_route.append(client)

    def client_arrived_at_goal (self, client: Client):
        self.clients_on_route.remove(client)

    def get_clients(self) -> list [Client]: # manual method to add clients, for testing
        c1 = Client ("Alandroal", "Monsaraz", 4)
        c2 = Client ("Palmela", "Lisboa", 3)

        return [c1, c2]

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