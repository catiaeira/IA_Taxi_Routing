from car import Car
from graph import Graph
from tasks.Task import Task

class Task_Move_Node(Task):      # will only deal with neighboring nodes
    def __init__(self, curr_node: str, goal_node: str, graph):
        super().__init__()
        self.priority = 1
        self.curr_node = curr_node
        self.goal_node = goal_node
        self.remaining_time = graph.calc_time_between_nodes(self.curr_node, self.goal_node)
        #print (f"From {curr_node} to {goal_node} it should take {self.remaining_time}.")


    def __str__(self) -> str:
        return (
            (
            f"  Starting node: {self.curr_node}\n"
            f"  Goal node = {self.goal_node}\n "
            )
        )

    def update(self, curr_time, available_time, graph, car, graph_changed) -> float:
        if self.time_started == -1:
            self.time_started = curr_time

        if graph_changed:
            new_total_time = graph.calc_time_between_nodes(self.curr_node, self.goal_node)
            time_elapsed = curr_time - self.time_started
            self.remaining_time = max(0, new_total_time - time_elapsed)

        time_used = min(self.remaining_time, available_time)
        self.remaining_time -= time_used
        available_time -= time_used

        if self.remaining_time <= 0:
            #print (f"move {self.curr_node} to {self.goal_node} completed at {curr_time}")
            self.completed = True

            distance = graph.get_arc_distance(self.curr_node, self.goal_node) # in meters
            car.curr_node = self.goal_node
            car.update_car_after_trip(distance)
            if car.energy_level <= 0:
                print ("Ran out of energy!")
                self.completed = True

        return available_time