from car import *
from graph import Graph
from tasks.Task import Task
from tasks.Task_Move import Task_Move

class Task_Refuel (Task):
    def __init__(self):
        super().__init__()
        self.priority = 1
        self.refueling = False
        self.time_left_refuel = -1
        self.moves: list[Task_Move] = []
        self.current_move_index = 0
    
    def __str__(self) -> str:
        return (
            "- Refuel " + super().__str__() + (
            f"  Refueling: {self.refueling}\n",
            f"  Time left refueling = {self.time_left_refuel}\n"
            f"  Time started = {self.time_started}\n"
            f"  Current move index = {self.current_move_index}\n"
            )
        )

    def update(self, curr_time, graph, car, graph_changed :bool):
        if self.time_started == -1:
            self.time_started = curr_time

        if self.refueling: # if already refueling
            self.wait_refueling(car)

        else: # going to the fuel/charging station

            if len(self.moves) == 0 or graph_changed:                 # path hasnt been calculated yet or needs updating

                path_changed_midway = graph_changed and len(self.moves)>0
                if path_changed_midway:
                    curr_move = self.moves[self.current_move_index] # if the graph changed midways we need to store the previous move
                    origin = curr_move.goal_node
                else:
                    origin = car.curr_node
                to_station = graph.find_closest_station_by_distance(origin, car.charges_in())   # find the closest station, prioritizing shortest path
                if to_station == None:
                    print (f"{car} can't get to station!")  # rip?
                    return 

                path = to_station[0]
                self.current_move_index = 0     # start/reset the moves
                self.moves = []

                if path_changed_midway:
                    self.moves.append(curr_move)            # save current move

                for i in range(len(path) - 1):
                    node_a = path[i]
                    node_b = path[i + 1]
                    self.moves.append(Task_Move(node_a, node_b, graph)) # create a task_move to each edge                 
                
            while self.current_move_index < len(self.moves):        # going to the station logic
                current_move = self.moves[self.current_move_index]
                current_move.update(curr_time, graph, car, graph_changed)

                self.recalc_estimated_time(car)

                if current_move.completed:
                    self.current_move_index += 1
                    
                    if self.current_move_index >= len(self.moves):  # has finished all the moves                        
                        self.refueling = True
                        print (f"{car} has reached the gas/charging station!")
                        break
                    
                    # we keep looping bc of the cenario where multiple moves are possible in the same minute
                else:
                    # the current move isnt completed, so we are done for this time step
                    break 

    def wait_refueling (self, car):
        # setup refueling time
        if self.time_left_refuel == -1:
            self.time_left_refuel = car.time_to_refuel()
            self.remaining_time = self.time_left_refuel
            print (f"Estimated time to fully refuel: {self.remaining_time}")
            
        elif self.time_left_refuel > 0:
            self.time_left_refuel -= 1
            self.remaining_time = self.time_left_refuel 
        
        # cleanup
        elif self.time_left_refuel == 0:
            self.completed = True
            car.energy_level = 100 
            print (f"Car {car} completed refueling")


    def recalc_estimated_time(self, car):
        total = 0
        for i in range(self.current_move_index, len(self.moves)):
            total += self.moves[i].remaining_time
        self.remaining_time = total + car.time_to_refuel()
