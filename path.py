from dataclasses import dataclass
from typing import List
from edge import Edge

@dataclass
class Path:
    nodes: List[int]
    edges: List[Edge]
    fitness: float = 0.0