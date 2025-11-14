from car import *
from graph import Graph

class Task:
    def __init__(self):
        self.completed = False
        self.estimated_time = 0
        self.priority = 0       # priority goes from 1 - 5
        self.time_started = -1  # -1 means it hasnt started yet
    

class Task_Move(Task):
    def __init__(self, curr_node, goal_node, graph):
        super().__init__()
        self.priority = 1
        self.curr_node = curr_node
        self.goal_node = goal_node

        distance = graph.get_arc_cost(self.curr_node, self.goal_node)
        speed = graph.get_arc_speed(self.curr_node, self.goal_node)
        time = distance / speed * 60
        self.estimated_time = time

    def update(self, curr_time, graph, car):        # updates the localization of the car
        if self.time_started == -1:
            self.time_started = curr_time
        distance = graph.get_arc_cost(self.curr_node, self.goal_node)    # needs to recalculate the estimated time in case the traffic has worsened
        speed = graph.get_arc_speed(self.curr_node, self.goal_node)
        time = distance / speed * 60
        self.estimated_time = time

        if curr_time - self.time_started >= time:
            self.completed = True 
            car.curr_node = self.goal_node


class Task_Deliver_Client (Task):
    def __init__(self, first_node, goal_node, path, graph): # path needs to include the trip to the client 
        super().__init__()
        self.priority = 3
        self.moves: List[Task_Move] = []
        self.current_move_index = 0
        for i in range(len(path) - 1):
            node_a = nodes[i]
            node_b = nodes[i + 1]
            self.moves.append(Task_Move(node_a, node_b, graph)) # create a task move to each edge

        self.recalc_estimated_time()
        
    
    def update(self, curr_time, graph, car):
        if time_started == -1:
            time_started = curr_time
            
        current_move = self.moves[self.current_move_index]
        current_move.update(curr_time, graph, car)
        if current_move.completed:
            self.current_move_index += 1
            self.recalc_estimated_time()
            if self.current_move_index >= len(self.moves):
                self.completed = True


    def recalc_estimated_time(self):
        total = 0
        for i in range(self.current_move_index, len(self.moves)):
            total += self.moves[i].estimated_time
        self.estimated_time = total


class Task_Refuel (Task): # todo finish
    def __init__(self, goal_node, graph):
        super().__init__()
        