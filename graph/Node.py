from typing_extensions import override
from .Energy_Station import Energy_Station

class Node:
    def __init__(self, name: str, type_node: Energy_Station) -> None:
        self.name: str = str(name)
        self.type: Energy_Station = type_node

    @override
    def __str__(self) -> str:
        return "node " + self.name

    @override
    def __repr__(self) -> str:
        return "node: " + self.name + " | type: " + self.type.name

    def getName(self) -> str:
        return self.name

    @override
    def __eq__(self, other: object) -> bool:
        r = False
        if not isinstance(other, Node):
            r = False
        else:
            r = self.name == other.name and self.type == other.type
        return r

    @override
    def __hash__(self) -> int:
        return hash(self.name)
