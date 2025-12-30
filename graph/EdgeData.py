from typing_extensions import override

class EdgeData:
    def __init__(self, dist: int, max_speed: int, curr_speed: int, multiplier: float) -> None:
        self.dist: int = dist
        self.max_speed: int = max_speed
        self.curr_speed: int = curr_speed
        self.multiplier: float = multiplier

    @override
    def __str__(self) -> str:
        return ""
