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

    CHOOSING_PREFERENCE = "TIME"        # time taken is the default choice when a car is being chosen

    def get_cars (self) -> list[Car]: # default cars it starts with... maybe change to import from a file
        car1 = FuelCar(energy_level=30)
        car2 = ElectricCar()

        car1.assign_location("Elvas")
        car2.assign_location("Elvas")

        return [car1, car2]
    
    def get_number_of_cars (self):
        return len(self.simulation_cars)

    def see_cars (self):
        i = 0
        for sim_car in self.simulation_cars:
            print("Car", i, ":", end=" ")
            print(sim_car.car)
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
        
    def assign_car_to_client (self, client, graph, client_controller): # returns 1 if sucessfull, 0 otherwise
        best_path = []
        best_parameter = None
        best_car = None

        for sim_car in self.simulation_cars:
            if sim_car.is_car_busy():       # if a car already has a trip assigned, dont consider it
                continue    

            car = sim_car.car                     

            trip_to_client = graph.create_path_to_client(car, client)
            if trip_to_client == None:
                continue

            path, time_taken, dist_travelled = trip_to_client
            
            # here we need to choose which parameter we're focusing on (eg fastest time, least fuel spent). 
            # only distance for now

            if self.CHOOSING_PREFERENCE == "TIME":
                if best_parameter == None or time_taken < best_parameter:
                    best_parameter = time_taken
                    best_path = path
                    best_car = sim_car 
            else:                           # todo will change to consider the cost instead of distance !!!!
                if best_parameter == None or dist_travelled < best_parameter:
                    best_parameter = dist_travelled
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

    def is_car_busy(self):
        has_to_deliver_client = False
        for task in self.tasks_list:
            if (isinstance(task, Task_Deliver_Client)):
                has_to_deliver_client = True
                break 

        if self.current_task != None or has_to_deliver_client:
            return True
        return False

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