import random

from car.Car import *
from car.Simulation_Car import Simulation_Car
from Client import Client
from Client_Controller import Client_Controller
from graph import Graph
from tasks import *

class Car_Controller: 
    def __init__(self, dynamic_car: bool):
        self.simulation_cars : list[Simulation_Car] = []
        self.dynamic_car = dynamic_car

        cars = self.get_cars()
        for car in cars:
            sim_car = Simulation_Car(car)
            self.simulation_cars.append(sim_car)        

    CHOOSING_PREFERENCE = "TIME"        # time taken is the default choice when a car is being chosen

    def get_cars (self) -> list[Car]: # default cars it starts with... maybe change to import from a file
        car1 = FuelCar(energy_level=30)
        car2 = ElectricCar()

        car1.assign_location("Elvas")
        car2.assign_location("Elvas")

        return [car1]
    
    def get_number_of_cars (self):
        return len(self.simulation_cars)

    def see_cars (self):
        i = 0
        for sim_car in self.simulation_cars:
            print("Car", i, ":", end=" ")
            print(sim_car.car)
            i += 1

    def see_sim_cars (self):
        i = 0
        for sim_car in self.simulation_cars:
            print("Car", i, ":", end=" ")
            print(sim_car)
            i += 1

    def add_car (self, car_type: int, car_capacity: int, car_energy_level: float, car_curr_node: str): #make car_type a str ?
        if(car_type == 1):
            car = FuelCar(energy_level=car_energy_level, capacity=car_capacity, curr_node=car_curr_node)
        elif(car_type == 2):
            car = ElectricCar(energy_level=car_energy_level, capacity=car_capacity, curr_node=car_curr_node)

        sim_car = Simulation_Car(car)
        self.simulation_cars.append(sim_car)

    def delete_car(self, index: int):
        self.simulation_cars.pop(index)

    def change_car(self, index: int, car_type: int, car_capacity: int, car_energy_level: int, car_curr_node: str):
        sim_car = self.simulation_cars[index]
        new_car = sim_car.car.change_characteristics(car_type, car_capacity, car_energy_level, car_curr_node)
        sim_car.car = new_car

    def update (self, curr_time, client_controller, graph, graph_changed : bool, roam : bool):
        waiting_clients  : list[Client] = client_controller.waiting_clients
        clients_on_route : list[Client] = client_controller.clients_on_route
        most_central_node : dict[str, int] = client_controller.central_popular_node
        if not roam: 
            most_central_node = None
        i = 0
        while i < len(waiting_clients):
            client = waiting_clients[i]
            if self.assign_car_to_client(client, graph, client_controller):
                client_controller.client_got_car_assigned(client)
            else:
                i += 1
            
        for s_car in self.simulation_cars: # update all cars
            s_car.update(curr_time, graph, graph_changed, most_central_node)
        
        if self.dynamic_car is True:
            action = random.choice(["create", "delete"])
            new_spawn_chance = 0.2 # 20% chance of spawning a new car
            delete_chance = 0.1 # 10% chance to delete a car

            if action == "create":
                if random.random() < new_spawn_chance:
                    car_type = random.choice([FuelCar, ElectricCar])
                    car_capacity = random.randint(3,9)
                    car_energy = random.randint(50,100)

                    nodes = list(graph.node_dict.keys())
                    curr_node = random.choice(nodes)

                    new_car = car_type(capacity=car_capacity, energy_level=car_energy, curr_node=curr_node)

                    self.simulation_cars.append(Simulation_Car(new_car))

                    print(f"\n[NEW CAR] {new_car}\n")
                    
            elif action == "delete":
                if self.simulation_cars and random.random() < delete_chance:
                    idle_cars = list(filter(lambda c : c.current_task != Task_Deliver_Client, self.simulation_cars)) #filters and keeps the cars that aren't transporting clients
                    if len(idle_cars) > 0:
                        to_delete = random.choice(idle_cars)

                        self.simulation_cars.remove(to_delete)
                        print(f"\n[CAR DELETED] {to_delete.car}\n")
        
    def assign_car_to_client (self, client, graph, client_controller) -> bool:
        car_set = set([])
        for sim_car in self.simulation_cars:
            if sim_car.is_car_busy():       # if a car already has a trip assigned, dont consider it
                continue
            car_set.add(sim_car.car)

        trip = graph.create_path_to_client(car_set, client, self.CHOOSING_PREFERENCE)

        if trip == None: # couldnt find a suitable car, will wait
            return False

        best_car, path, _, _ = trip

        best_sim_car = None
        for sim_car in self.simulation_cars:
            if sim_car.car == best_car:
                best_sim_car = sim_car
                break

        if best_sim_car == None:
            print ("error finding sim car assigning a car!") # shouldnt happen
            return False

        print (f"{client} assigned to {best_car}")
        task = Task_Deliver_Client (path, graph, client, client_controller, self.CHOOSING_PREFERENCE)
        best_sim_car.tasks_list.append (task)
        return True