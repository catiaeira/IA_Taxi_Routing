from car import *
from graph import Graph
from tasks.Task import Task

class Task_Refuel (Task):
    def __init__(self):
        from tasks.Task_Move import Task_Move
        super().__init__()
        self.priority = 2
        self.refueling = False
        self.time_left_refuel = -1
        self.move = Task_Move(self)
    
    def __str__(self) -> str:
        return (
            "- Refuel " + super().__str__() + (
            f"  Refueling: {self.refueling}\n"
            f"  Time left refueling = {self.time_left_refuel}\n"
            f"  Time started = {self.time_started}\n"
            f"  {self.move}"
            )
        )

    def update(self, curr_time, graph, car, graph_changed :bool):
        if self.time_started == -1:
            self.time_started = curr_time

        if self.refueling: # if already refueling
            self.wait_refueling(car)
        else:        
            self.move.update(curr_time, graph, car, graph_changed)
            self.remaining_time = self.move.remaining_time + car.time_to_refuel()
            if self.move.completed:
                self.refueling = True
                print (f"{car} has reached the gas/charging station!")

    def wait_refueling (self, car):
        # setup refueling time
        if self.time_left_refuel == -1:
            self.time_left_refuel = car.time_to_refuel()
            self.remaining_time = self.time_left_refuel
            print (f"Estimated time to fully refuel: {self.remaining_time}")
            
        elif self.time_left_refuel > 0:
            self.time_left_refuel -= 1
            self.remaining_time = self.time_left_refuel 
            car.energy_level += car.recharge_per_min
        
        # cleanup
        elif self.time_left_refuel <= 0:
            self.completed = True
            car.energy_level = 100 
            print (f"{car} Completed refueling")