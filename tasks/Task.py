class Task:
    def __init__(self):
        self.completed = False
        self.remaining_time = -1
        self.priority = 0       # priority goes from 1 - 5
        self.time_started = -1  # -1 means it hasnt started yet

    def __str__(self) -> str:
        return (
            f"Task\n"
            f"  Priority = {self.priority}\n"
            f"  Time remaining = {self.remaining_time}\n"
            f"  Time started = {self.time_started}\n"
            f"  Completed = {self.completed}\n"
        )