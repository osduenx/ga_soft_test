from typing import List, Dict, Set
import networkx as nx
from edge import Edge
from path import Path

class ControlFlowGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.edges = {}
        self.initial_credit = 10  # As per the paper

    def add_edge(self, source: int, target: int, edge_type: str = 'sequential'):
        edge = Edge(source, target, 0.0, edge_type)
        self.graph.add_edge(source, target, edge=edge)
        self.edges[(source, target)] = edge

    def assign_weights(self):
        self._assign_weights_recursive(0, self.initial_credit, set())

    def _assign_weights_recursive(self, node: int, incoming_credit: float, visited: Set[int]):
        if node in visited:
            return
        visited.add(node)

        out_edges = list(self.graph.out_edges(node))
        if not out_edges:
            return

        sequential_edges = []
        control_edges = []

        for source, target in out_edges:
            edge = self.edges[(source, target)]
            if edge.edge_type == 'sequential':
                sequential_edges.append((source, target))
            else:
                control_edges.append((source, target))

        if control_edges and sequential_edges:
            control_credit = 0.8 * incoming_credit
            sequential_credit = 0.2 * incoming_credit

            for source, target in control_edges:
                self.edges[(source, target)].weight = control_credit / len(control_edges)

            for source, target in sequential_edges:
                self.edges[(source, target)].weight = sequential_credit / len(sequential_edges)

        elif control_edges:
            for source, target in control_edges:
                self.edges[(source, target)].weight = incoming_credit / len(control_edges)

        else:
            for source, target in sequential_edges:
                self.edges[(source, target)].weight = incoming_credit / len(sequential_edges)

        for source, target in out_edges:
            edge_weight = self.edges[(source, target)].weight
            self._assign_weights_recursive(target, edge_weight, visited)

    def get_all_paths(self, start: int, end: int, max_loops: int = 2) -> List[Path]:
        all_paths = []

        def dfs(current: int, path: List[int], edge_path: List[Edge],
                node_visits: Dict[int, int]):
            if current == end:
                all_paths.append(Path(path.copy(), edge_path.copy()))
                return

            for neighbor in self.graph.neighbors(current):
                # Check loop limit
                if node_visits.get(neighbor, 0) < max_loops:
                    new_visits = node_visits.copy()
                    new_visits[neighbor] = new_visits.get(neighbor, 0) + 1

                    edge = self.edges[(current, neighbor)]
                    dfs(neighbor, path + [neighbor], edge_path + [edge], new_visits)

        dfs(start, [start], [], {start: 1})
        return all_paths