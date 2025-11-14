from car import *
import Client

class Car_controller: 
    def __init__(self, dynamic_car: bool):
        self.simulation_cars = []
        self.waiting_clients = []
        self.clients_on_route = []
        self.dynamic_car = dynamic_car

        cars = get_cars()
        for car in cars:
            sim_car = Simulation_car(car)
            cars.append(sim_car)        


    def get_cars () -> list(Car): # default cars it starts with... maybe change to import from a file
        car1 = FuelCar()
        car2 = ElectricCar()

        car1.assign_location("Elvas")
        car2.assign_location("Lisboa")

        return [car1,car2]

    def update (curr_time, client_controller, graph):
        # get new clients from client controller
        # for each waiting client assign a car

        for s_car in simulation_cars:
            s_car.update(curr_time)
        

class Simulation_car:
    def __init__(self, car):
        self.car : Car = car
        self.tasks_list : list(Task) = []
        self.current_task : tuple(Task, int) = () 

    def update(curr_time, graph):
        current_task.update(curr_time, graph, car)
        curr_priority = curr_task
        most_important_task = curr_task
        
        if current_task.completed:
            task_list.remove(current_task)
            curr_priority = 0

        for t in tasks_list:
            if t.priority > curr_priority:
                most_important_task = t

        current_task = most_important_task
    


class Task:
    def __init__(self,):
        self.completed = False
        self.total_time = 0
        self.priority = 0
    
class Task_Move(Task):
    def __init__(self, curr_node, goal_node, time_started, estimated_time):
        self.curr_node = curr_node
        self.goal_node = goal_node
        self.time_started = time_started
        self.estimated_time = estimated_time

    def update(self, curr_time, graph, car):        # updates the localization of the car
        distance = graph.get_arc_cost (curr_node, goal_node)
        speed = 1 # = graph.getspeed?????????
        time = distance / speed * 60

        if curr_time - time_started >= time:
            self.completed = True 
            car.curr_node = goal_node
