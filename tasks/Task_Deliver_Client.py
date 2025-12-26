from car import *
from graph import Graph
from tasks.Task import Task
from tasks.Task_Move import Task_Move

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
        
    def __str__(self) -> str:
        moves = ""
        for m in self.moves:
            moves += "    " + str(m).replace("\n", "\n    ") + "\n"
        return (
            "- Delivering Client " + super().__str__() + (
            f"  Client = {self.client}\n"
            f"  Current move index = {self.current_move_index}\n"
            f"  Moves:\n{moves}"
            )
        )

    def update(self, curr_time, graph, car, graph_changed :bool):
        if self.time_started == -1:
            self.time_started = curr_time

        if graph_changed:                                   # graph changed, so we need to update the moves
            curr_move = self.moves[self.current_move_index] 
            path_tuple = graph.update_path (car, self.client, curr_move.goal_node)
            if path_tuple == None:                          # can't deliver client now, wait in place for traffic to get better?
                print ("No path found to client goal after change in traffic!")
                return 

            path, path_time, path_dist = path_tuple
            self.current_move_index = 0
            self.moves = [curr_move]            # insert the previous move

            for i in range(len(path) - 1):
                node_a = path[i]
                node_b = path[i + 1]
                self.moves.append(Task_Move(node_a, node_b, graph)) # create a task_move to each edge
            
        #loop to process moves until the current move is incomplete
        while self.current_move_index < len(self.moves):
            current_move = self.moves[self.current_move_index]
            current_move.update(curr_time, graph, car, graph_changed)

            if current_move.curr_node == self.client.start and not self.client.is_in_car:
                self.client.enter_car()
                car.update_car_clients(True, self.client) # update car, has picked up client

            self.recalc_estimated_time()

            if current_move.completed:
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

    def recalc_estimated_time(self):
        total = 0
        for i in range(self.current_move_index, len(self.moves)):
            total += self.moves[i].remaining_time
        self.remaining_time = total
