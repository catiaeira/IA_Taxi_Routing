from typing_extensions import override

class Client: 
    def __init__(self, start: str, goal: str, how_many: int = 1):
        self.start = start
        self.goal = goal
        self.is_in_car = False
        self.how_many = how_many
        # missing: preference? time, electric car, premium client

    def enter_car (self):
        self.is_in_car = True

    @override
    def __repr__(self) -> str:
        return "Client: " + self.start + " -> " + self.goal + " [" + str(self.how_many) + " passengers]"
