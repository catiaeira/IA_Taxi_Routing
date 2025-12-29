from car import *
from graph import Graph
from tasks.Task import Task

class Task_Roam (Task):
    def __init__(self, node):
        from tasks.Task_Move import Task_Move
        super().__init__()
        self.node = node
        self.priority = 1
        self.move = Task_Move(self)

    def __str__(self) -> str:
        return (
            "- Roam " + super().__str__() + (
            f"  Node: {self.node}\n"
            f"  Time started = {self.time_started}\n"
            f"  {self.move}"
            )
        )

    def update(self, curr_time, graph, car, graph_changed :bool):
        if self.time_started == -1:
            self.time_started = curr_time

        self.move.update(curr_time, graph, car, graph_changed)
        self.remaining_time = self.move.remaining_time

        if self.move.completed:
            self.completed = True
            print ("Arrived at most central node!")