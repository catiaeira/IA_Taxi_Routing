from car import *
from graph import Graph
from tasks.Task import Task
# will handle the entire trip of one client
class Task_Deliver_Client (Task):
    total_time_trip : int = 0

    def __init__(self, path, graph, client, client_controller, choosing_preference, is_premium = False): # path needs to include the trip to the client 
        from tasks.Task_Move import Task_Move
        super().__init__()
        if is_premium:
            self.priority = 4
        else:
            self.priority = 3
        self.current_move_index = 0
        self.client = client
        self.CHOOSING_PREFERENCE = choosing_preference
        self.move = Task_Move(self, path, graph)

        self.remaining_time = self.move.remaining_time 
        print(f"Estimated remaining time: {self.remaining_time} to client {client}.")
        self.client_controller = client_controller
        
    def __str__(self) -> str:
        return (
            "- Delivering Client " + super().__str__() + (
            f"  Client = {self.client}\n"
            f"  {self.move}"
            )
        )

    def update(self, curr_time, graph, car, graph_changed :bool):
        if self.time_started == -1:
            self.time_started = curr_time

        self.move.update(curr_time, graph, car, graph_changed)
        self.remaining_time = self.move.remaining_time
        
        if self.move.completed:
            car.update_car_clients(self.client)
            self.client_controller.client_arrived_at_goal(self.client)
            self.completed = True
            Task_Deliver_Client.total_time_trip += (curr_time - self.time_started)
            print ("Client trip completed!")