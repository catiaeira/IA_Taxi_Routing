from car import *
import Client


class Car_Controller: 
    def __init__(self, dynamic_car: bool):
        self.simulation_cars : List[Simulation_Car] = []
        self.dynamic_car = dynamic_car

        cars = get_cars()
        for car in cars:
            sim_car = Simulation_Car(car)
            simulation_cars.append(sim_car)        


    def get_cars () -> list(Car): # default cars it starts with... maybe change to import from a file
        car1 = FuelCar()
        car2 = ElectricCar()

        car1.assign_location("Elvas")
        car2.assign_location("Lisboa")

        return [car1,car2]

    def update (curr_time, client_controller, graph):
        waiting_clients : List [Client] = []
        clients_on_route : List[Client] = []
        # get clients from client controller ...
        # for each waiting client assign a car ... 

        for s_car in simulation_cars: # update all cars
            s_car.update(curr_time, graph)
        
        # if dynamic_car:
        #   remove/add cars with x chance
        

# updates cars based on the tasks they need to do, decided by a priority system
# eg. refueling might be low priority when theres lots of gas, and become high priority when its running low
#     or when theres a client in the car and we want to carpool another client, getting the new client will be a higher 
#     priority than delivering the first

class Simulation_Car:
    def __init__(self, car):
        self.car: Car = car
        self.tasks_list: list[Task] = []
        self.current_task: Task = None 

    def update(self, curr_time, graph):
        if self.current_task is None and self.tasks_list:
            self.current_task = max(self.tasks_list, key=lambda t: t.priority)

        if self.current_task is not None:
            self.current_task.update(curr_time, graph, self.car)

            if self.current_task.completed:
                self.tasks_list.remove(self.current_task)
                self.current_task = None 

        self.current_task = max(self.tasks_list, key=lambda t: t.priority)