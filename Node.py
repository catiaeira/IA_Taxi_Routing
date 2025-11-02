from typing_extensions import override

class Node:
    def __init__(self, name: str) -> None:
        self.name: str = str(name)

    @override
    def __str__(self) -> str:
        return "node " + self.name

    @override
    def __repr__(self) -> str:
        return "node " + self.name

    def getName(self) -> str:
        return self.name

    @override
    def __eq__(self, other: object) -> bool:
        r = False
        if not isinstance(other, Node):
            r = False
        else:
            r = self.name == other.name  
        return r

    @override
    def __hash__(self) -> int:
        return hash(self.name)
