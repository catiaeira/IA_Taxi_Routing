from car.Car import Car
from Client import Client
from Client_Controller import Client_Controller
from tasks import *
from graph import Graph

# updates cars based on the tasks they need to do, decided by a priority system
# eg. refueling might be low priority when theres lots of gas, and become high priority when its running low
#     or when theres a client in the car and we want to carpool another client, getting the new client will be a higher 
#     priority than delivering the first

class Simulation_Car:
    def __init__(self, car):
        self.car: Car = car
        self.tasks_list: list[Task] = []
        self.current_task: Task = None 
        
    def __str__(self) -> str:
        car_info = "    " + str(self.car).replace("\n", "\n    ").strip()

        if self.current_task:
            curr_task_str = "    " + str(self.current_task).replace("\n", "\n    ")
        else:
            curr_task_str = "    None"

        #tasks = ""
        #for t in self.tasks_list:
        #    tasks += "    " + str(t).replace("\n", "\n    ") + "\n"

        return (
            f"\n--- Simulation Car Status ---\n"
            f"Details:\n{car_info}\n"
            f"Current Task:\n{curr_task_str}\n"
            #f"Tasks Queue:\n{tasks if tasks else '    (Empty)'}" # bloats printing
        )

    def is_car_busy(self):
        has_to_deliver_client = False
        for task in self.tasks_list:
            if (isinstance(task, Task_Deliver_Client)):
                has_to_deliver_client = True
                break 

        if self.current_task != None or has_to_deliver_client:
            return True
        return False

    def update(self, curr_time, graph, graph_changed :bool, most_central_node : str):
        if self.current_task is None :
            self.check_energy_level()
            self.check_roam(most_central_node)
            if self.tasks_list:
                self.current_task = max(self.tasks_list, key=lambda t: t.priority)

        if self.current_task is not None:
            self.current_task.update(curr_time, graph, self.car, graph_changed)

            if self.current_task.completed:
                self.tasks_list.remove(self.current_task)
                self.current_task = None
                print(str(self))

    
    def check_energy_level(self): 
        kms_left = self.car.energy_level / self.car.consumption_per_km
        if self.car.total_trips_done == 0:
            average_km_per_trip = 50                    # best to change this after we know an actual average
        else: average_km_per_trip = self.car.total_kms_travelled_w_passengers / self.car.total_trips_done

        if kms_left < 2.5 * average_km_per_trip:
            refuel_task = self.get_refuel_task()
            
            if kms_left < average_km_per_trip:  # very low energy
                print ("increasing refuel task priority to max")
                refuel_task.priority = 5
            elif kms_left < 2 * average_km_per_trip:  # low energy:
                print ("increasing refuel task priority")
                refuel_task.priority = 3        # same priority as delivering normal clients       

        
    def check_roam(self, most_central_node):
        if most_central_node == None or self.car.curr_node == most_central_node:
            return 

        roam_task = Task_Roam(most_central_node)
        for task in self.tasks_list:
            if isinstance(task, Task_Roam):
                if task.node == most_central_node:
                    return
                self.tasks_list.remove(task)    # remove outdated roam task
                break 

        self.tasks_list.append(roam_task)


    def get_refuel_task (self) -> Task_Refuel:    # creates it if there isnt any
        for task in self.tasks_list:
            if isinstance(task, Task_Refuel):
                return task 

        refuel_task = Task_Refuel()
        self.tasks_list.append(refuel_task)
        print("creating refuel task")
        return refuel_task