from typing import Dict, NamedTuple, List
from math import sqrt, pow

class Position(NamedTuple):
    x: int
    y: int

class Graph:
    
    def __init__(self):
        self._vertices: Dict[str, Position] = {}
        self._edges: Dict[str, set[str]] = {}
        self._weights: Dict[str, float] = {}

    def __str__(self) -> str:
        return f"""
        V={self.vertices}\n
        E={self.edges}
        """
    def __len__(self) -> int:
        return len(self.vertices)

    @property
    def vert_data(self) -> Dict[str, Position]:
        return self._vertices

    @property
    def vertices(self) -> set[str]:
        return set(self._vertices.keys())
    
    @property
    def edges(self) -> set[str]:
        return [[(src, dst) for dst in adjacent] for src, adjacent in self._edges.items()]

    @property
    def edge_data(self) -> Dict[str, set[str]]:
        return self._edges
    
    @property
    def weight_data(self) -> Dict[str, float]:
        return self._weights

    def get_pos(self, vert_key: str) -> Position:
        return self.vert_data[vert_key]

    def adjacent(self, vertex: str) -> set[str]:
        return self.vert_data[vertex]
    
    def add_vert(self, position: Position) -> None:
        self.vert_data[self.__vert_key(position)] = position
    
    def remove_vert(self, vert_key: str) -> None:
        if vert_key in self.vertices:
            del self.vert_data[vert_key]
    
    def add_edge(self, src: Position, dst: Position, weight: float=None, directed: bool=False) -> None:
        # make sure vertices are in graph
        src_key = self.__vert_key(src)
        if src_key not in self.vertices:
            print(f"Source node: {src_key} not found in graph.. (Tip: add_vert)")
            return

        dst_key = self.__vert_key(dst)
        if dst_key not in self.vertices:
            print(f"Destination node: {dst_key} not found in graph.. (Tip: add_vert)")

        # add directed edge
        self._edges[src_key].add(dst_key)
        self._weights[self.__edge_key(src, dst)] = weight

        # add reversed edge (omni-directional)
        if directed == False:
            self._edges[dst_key] = src_key
            self._weights[self.__edge_key(dst, src)] = weight

    def clear(self) -> None:
        self.vert_data.clear()
        self.edge_data.clear()
        self.weight_data.clear()
    
    ### PRIVATE ###
    def __vert_key(self, position: Position) -> str:
        return f"{position}"
    
    def __edge_key(self, src: str, dst: str) -> str:
        return f"({self.__vert_key(src)} -> {self.__vert_key(dst)}"