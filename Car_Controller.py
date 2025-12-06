from car.Car import *
from Client import Client
from Client_Controller import Client_Controller
from Task import *
from graph import Graph

class Car_Controller: 
    def __init__(self, dynamic_car: bool):
        self.simulation_cars : list[Simulation_Car] = []
        self.dynamic_car = dynamic_car

        cars = self.get_cars()
        for car in cars:
            sim_car = Simulation_Car(car)
            self.simulation_cars.append(sim_car)        


    def get_cars (self) -> list[Car]: # default cars it starts with... maybe change to import from a file
        car1 = FuelCar(30)
        car2 = ElectricCar()

        car1.assign_location("Elvas")
        car2.assign_location("Elvas")

        return [car1]

    def update (self, curr_time, client_controller, graph, graph_changed : bool):
        waiting_clients : list [Client] = client_controller.waiting_clients
        clients_on_route : list[Client] = client_controller.clients_on_route

        i = 0
        while i < len(waiting_clients):
            client = waiting_clients[i]
            if self.assign_car_to_client(client, graph, client_controller):
                client_controller.client_got_in_car(client)
            else:
                i += 1
            
        for s_car in self.simulation_cars: # update all cars
            s_car.update(curr_time, graph, graph_changed)
        
        # if dynamic_car:
        #   remove/add cars with x chance
        

        # todo
        # smarter division when assigning clients (consider cars that are already in a trip)
        #
    def assign_car_to_client (self, client, graph, client_controller): # returns 1 if sucessfull, 0 otherwise
        best_path = []                              # probably can be better
        best_distance = None
        best_car = None

        for sim_car in self.simulation_cars:     
            car = sim_car.car                       # todo currently not considering if its already in a trip

            trip_to_client = graph.create_path_to_client(car, client)
            if trip_to_client == None:
                continue

            path, time_taken, dist_travelled = trip_to_client
            
            # here we need to choose which parameter we're focusing on (eg fastest time, least fuel spent). 
            # only distance for now

            if best_distance == None or dist_travelled < best_distance:
                best_distance = dist_travelled
                best_path = path
                best_car = sim_car 
        
        if best_car == None:
            # couldnt find a suitable car, will wait
            print ("no suitable car found")
            return 0
        
        print (f"{client} assigned to {best_car.car}!")
        task = Task_Deliver_Client (best_path, graph, client, client_controller)
        best_car.tasks_list.append (task)
        return 1


# updates cars based on the tasks they need to do, decided by a priority system
# eg. refueling might be low priority when theres lots of gas, and become high priority when its running low
#     or when theres a client in the car and we want to carpool another client, getting the new client will be a higher 
#     priority than delivering the first

class Simulation_Car:
    def __init__(self, car):
        self.car: Car = car
        self.tasks_list: list[Task] = []
        self.current_task: Task = None 

    def update(self, curr_time, graph, graph_changed :bool):
        if self.current_task is None :
            self.check_energy_level()
            if self.tasks_list:
                self.current_task = max(self.tasks_list, key=lambda t: t.priority)

        if self.current_task is not None:
            self.current_task.update(curr_time, graph, self.car, graph_changed)

            if self.current_task.completed:
                self.tasks_list.remove(self.current_task)
                self.current_task = None

    
    def check_energy_level(self): 
        kms_left = self.car.energy_level / self.car.consumption_per_km
        if self.car.total_trips_done == 0:
            average_km_per_trip = 50                    # best to change this after we know an actual average
        else: average_km_per_trip = self.car.total_kms_travelled_w_passengers / self.car.total_trips_done

        if kms_left < 2 * average_km_per_trip:
            refuel_task = self.get_refuel_task(self.tasks_list)
            
            if kms_left < average_km_per_trip:  # very low energy
                print ("increasing refuel task priority to max")
                refuel_task.priority = 5
            else :                              # low energy
                print ("increasing refuel task priority")
                refuel_task.priority = 3        # same priority as delivering normal clients

        
    def get_refuel_task (self, tasks_list: list[Task]) -> Task_Refuel:    # creates it if there isnt any
        for task in tasks_list:
            if isinstance(task, Task_Refuel):
                return task 

        refuel_task = Task_Refuel()
        self.tasks_list.append(refuel_task)
        print("creating refuel task")
        return refuel_task