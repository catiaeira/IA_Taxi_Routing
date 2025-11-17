from car import *
from graph import Graph

class Task:
    def __init__(self):
        self.completed = False
        self.estimated_time = 0
        self.priority = 0       # priority goes from 1 - 5
        self.time_started = -1  # -1 means it hasnt started yet
    

class Task_Move(Task):      # will only deal with neighboring nodes
    def __init__(self, curr_node, goal_node, graph):
        super().__init__()
        self.priority = 1
        self.curr_node = curr_node
        self.goal_node = goal_node

        distance = graph.get_arc_cost(self.curr_node, self.goal_node)
        speed = graph.get_arc_speed(self.curr_node, self.goal_node)
        time = distance / speed * 60
        self.estimated_time = time

    def update(self, curr_time, graph, car, client):  #todo is missing taking fuel into consideration
        if self.time_started == -1:
            self.time_started = curr_time
        distance = graph.get_arc_cost(self.curr_node, self.goal_node)    # needs to recalculate the estimated time in case the traffic has worsened
        speed = graph.get_arc_speed(self.curr_node, self.goal_node)
        time = distance / speed * 60 # time in mins, distance in kms and speed in km/h
        time = distance / speed * 60 /10 # for testing, speed things up
        self.estimated_time = time

        if curr_time - self.time_started >= time:
            print (f"move {self.curr_node} to {self.goal_node} completed at {curr_time}")
            self.completed = True
            car.curr_node = self.goal_node
            car.update_car_after_trip(distance, car.consumption(distance), True)


class Task_Deliver_Client (Task):
    def __init__(self, path, graph, client, client_controller): # path needs to include the trip to the client 
        super().__init__()
        self.priority = 3
        self.moves: List[Task_Move] = []
        self.current_move_index = 0
        self.client = client
        for i in range(len(path) - 1):
            node_a = path[i]
            node_b = path[i + 1]
            self.moves.append(Task_Move(node_a, node_b, graph)) # create a task_move to each edge

        self.recalc_estimated_time()
        self.client_controller = client_controller
        
    
    def update(self, curr_time, graph, car):
        if self.time_started == -1:
            self.time_started = curr_time
            
        current_move = self.moves[self.current_move_index]
        current_move.update(curr_time, graph, car, self.client)
        if self.time_started == curr_time or current_move.completed: # picking up / dropping a client
             car.update_car_clients(True, self.client)

        if current_move.completed:
            self.current_move_index += 1
            self.recalc_estimated_time()
            if self.current_move_index >= len(self.moves):
                self.completed = True
                self.client_controller.client_arrived_at_goal(self.client)
                print ("client trip completed!")

    # missing: recalculate route

    def recalc_estimated_time(self):
        total = 0
        for i in range(self.current_move_index, len(self.moves)):
            total += self.moves[i].estimated_time
        self.estimated_time = total


class Task_Refuel (Task): # todo finish
    def __init__(self, goal_node, graph):
        super().__init__()
        