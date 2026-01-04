from typing_extensions import override

class Client: 
    def __init__(self, start: str, goal: str, how_many: int = 1, is_green=False, is_premium=False):
        self.start = start
        self.goal = goal
        self.is_in_car = False
        self.how_many = how_many
        self.is_green = is_green
        self.is_premium = is_premium

    def enter_car (self):
        self.is_in_car = True

    @override
    def __repr__(self) -> str:
        premium_tag = "Premium " if self.is_premium else ""
        is_green_tag = "Green " if self.is_green else ""
        return (
            f"{premium_tag}{is_green_tag}Client: {self.start} -> {self.goal} "
            f"[{self.how_many} passengers]"
        )