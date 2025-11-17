from typing_extensions import override

class Client: 
    def __init__(self, start: str, goal: str, how_many: int = 1):
        self.start = start
        self.goal = goal
        self.how_many = how_many

    @override
    def __repr__(self) -> str:
        return "Client " + self.start + " - " + self.goal + ": " + self.how_many