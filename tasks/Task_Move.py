from car import *
from graph import Graph
from tasks.Task_Deliver_Client import Task_Deliver_Client
from tasks.Task_Move_Node import Task_Move_Node
from tasks.Task_Refuel import Task_Refuel
from tasks.Task_Roam import Task_Roam
from tasks.Task import Task


class Task_Move(Task): 
    def __init__(self, main_task, path=[],graph=None):
        super().__init__()
        self.priority = 1
        self.moves: list[Task_Move_Node] = []
        self.main_task = main_task
        self.current_move_index = 0

        if path:
            for i in range(len(path) - 1):
                node_a = path[i]
                node_b = path[i + 1]
                self.moves.append(Task_Move_Node(node_a, node_b, graph)) # create a task_move to each edge

            self.recalc_estimated_time()

    def __str__(self) -> str:
        moves = ""
        for m in self.moves:
            moves += "    " + str(m).replace("\n", "\n    ") + "\n"
        return (
            "- Move " + super().__str__() + (
            f"  Current move index = {self.current_move_index}\n"
            f"  Moves:\n{moves}"
            )
        )

    def update(self, curr_time, graph, car, graph_changed :bool):
        if self.time_started == -1:
            self.time_started = curr_time
            
        if len(self.moves) == 0 or graph_changed:   # create or recreate path to destination
            self.update_path(graph, car, graph_changed)

        if len(self.moves) == 0:
            self.completed = True
            return
        
        #loop to process moves until the current move is incomplete
        while self.current_move_index < len(self.moves):
            current_move = self.moves[self.current_move_index]
            current_move.update(curr_time, graph, car, graph_changed)

            if isinstance(self.main_task, Task_Deliver_Client) and \
                current_move.curr_node == self.main_task.client.start and \
                not self.main_task.client.is_in_car:

                self.main_task.client.enter_car()
                car.update_car_clients(True, self.main_task.client) # update car, has picked up client

            self.recalc_estimated_time()

            if current_move.completed:
                self.current_move_index += 1
                
                if self.current_move_index >= len(self.moves):  # has finished all the moves
                    self.completed = True
                    return
                
                # we keep looping bc of the cenario where multiple moves are possible in the same minute
            else:
                # the current move isnt completed, so we are done for this time step
                break 

    def update_path(self, graph, car, graph_changed):
        path_changed_midway = graph_changed and len(self.moves)>0
        if path_changed_midway:
            curr_move = self.moves[self.current_move_index] # if the graph changed midways we need to store the previous move
            origin = curr_move.goal_node
        else:
            origin = car.curr_node
        
        path_tuple = None
        if isinstance(self.main_task, Task_Deliver_Client):
            path_tuple = graph.update_path (car, self.main_task.client, curr_move.goal_node, self.main_task.CHOOSING_PREFERENCE)
        elif isinstance(self.main_task, Task_Refuel):
            path_tuple = graph.find_closest_station_by_distance(origin, car.charges_in())   # find the closest station, prioritizing shortest path
        elif isinstance(self.main_task, Task_Roam):
            path_tuple = graph.a_star_search_by_distance(origin, self.main_task.node)

        if path_tuple == None:
            return 

        path = path_tuple[0]
        self.current_move_index = 0
        self.moves = []           

        if path_changed_midway:
            self.moves.append(curr_move)            # save current move

        for i in range(len(path) - 1):
            node_a = path[i]
            node_b = path[i + 1]
            self.moves.append(Task_Move_Node(node_a, node_b, graph)) # create a task_move_node to each edge
    
    def recalc_estimated_time(self):
        total = 0
        for i in range(self.current_move_index, len(self.moves)):
            total += self.moves[i].remaining_time

        self.remaining_time = total