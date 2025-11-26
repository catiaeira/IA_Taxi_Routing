from car import *
from graph import Graph
import math

class Task:
    def __init__(self):
        self.completed = False
        self.remaining_time = -1
        self.priority = 0       # priority goes from 1 - 5
        self.time_started = -1  # -1 means it hasnt started yet
    

class Task_Move(Task):      # will only deal with neighboring nodes
    def __init__(self, curr_node: str, goal_node: str, graph):
        super().__init__()
        self.priority = 1
        self.curr_node = curr_node
        self.goal_node = goal_node
        self.remaining_time = self.calc_time_between_nodes(self.curr_node, self.goal_node, graph)
        #print (f"From {curr_node} to {goal_node} it should take {self.remaining_time}.")


    def update(self, curr_time, graph, car, client):  #todo is missing taking fuel into consideration
        if self.time_started == -1:
            self.time_started = curr_time

        # needs to recalculate the estimated time in case the traffic has worsened
        new_total_time = self.calc_time_between_nodes(self.curr_node, self.goal_node, graph)
        time_elapsed = curr_time - self.time_started
        self.remaining_time = max(0, new_total_time - time_elapsed)

        if self.remaining_time <= 0:
            #print (f"move {self.curr_node} to {self.goal_node} completed at {curr_time}")
            self.completed = True

            distance = graph.get_arc_distance(self.curr_node, self.goal_node) # in meters
            car.curr_node = self.goal_node
            car.update_car_after_trip(distance, True)


    def calc_time_between_nodes(self, curr_node: str, goal_node : str, graph) -> float:
        distance = graph.get_arc_distance(self.curr_node, self.goal_node) # in meters
        speed = graph.get_arc_speed(self.curr_node, self.goal_node)       # in kms
        if (distance == math.inf or speed == math.inf):
            print (f"Path not found when calculating time: {curr_node} - {goal_node}")
            return 0

        time = distance / 1000 / speed * 60
        return time

# will handle the entire trip of one client
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
        print(f"Estimated remaining time: {self.remaining_time} to client {client}.")
        self.client_controller = client_controller
        
    
    def update(self, curr_time, graph, car): # needs to be able to recalculate the path
        if self.time_started == -1:
            self.time_started = curr_time
            
        #loop to process moves until the current move is incomplete
        while self.current_move_index < len(self.moves):
            current_move = self.moves[self.current_move_index]
            current_move.update(curr_time, graph, car, self.client)

            if current_move.curr_node == self.client.start and not self.client.is_in_car:
                self.client.enter_car()
                car.update_car_clients(True, self.client) # update car, has picked up client

            self.recalc_estimated_time()

            if current_move.completed:
                print (f"car condition: {car}")
                self.current_move_index += 1
                
                if self.current_move_index >= len(self.moves):  # has finished all the moves
                    self.completed = True
                    
                    # drop off client
                    car.update_car_clients(True, self.client)
                    self.client_controller.client_arrived_at_goal(self.client)
                    print ("client trip completed!")
                    break
                
                # we keep looping bc of the cenario where multiple moves are possible in the same minute
            else:
                # the current move isnt completed, so we are done for this time step
                break 
    # missing: recalculate route

    def recalc_estimated_time(self):
        total = 0
        for i in range(self.current_move_index, len(self.moves)):
            total += self.moves[i].remaining_time
        self.remaining_time = total #+ (len(self.moves) - self.current_move_index) # it takes one time unit to change nodes, so we need to sum the number of moves left


class Task_Refuel (Task): # todo finish
    def __init__(self, goal_node, graph):
        super().__init__()
        