from typing import Dict, List, Tuple
from math import sqrt, pow

class Graph:
    
    def __init__(self):
        self._vertices: Dict[str, Tuple[int, int]] = {}
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
    def vert_data(self) -> Dict[str, Tuple[int, int]]:
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

    def get_pos(self, vert_key: str) -> Tuple[int, int]:
        return self.vert_data[vert_key]

    def adjacent(self, vertex: str) -> set[str]:
        return self.vert_data[vertex]
    
    def add_vert(self, position: Tuple[int, int]) -> None:
        vert_key = self.vert_key(position)
        self.vert_data[vert_key] = position
        self.edge_data[vert_key] = set()
    
    def remove_vert(self, vert_key: str) -> None:
        if vert_key in self.vertices:
            del self.vert_data[vert_key]
            del self.edge_data[vert_key]
    
    def add_edge(self, src_key: str, dst_key: str, weight: float=None, directed: bool=False) -> None:
        # make sure vertices are in graph
        if src_key not in self.vertices:
            print(f"Source node: {src_key} not found in graph.. (Tip: add_vert)")
            return

        if dst_key not in self.vertices:
            print(f"Destination node: {dst_key} not found in graph.. (Tip: add_vert)")

        # add directed edge
        self._edges[src_key].add(dst_key)
        self._weights[self.edge_key(src_key, dst_key)] = weight if weight != None else self.distance(src_key, dst_key)

        # add reversed edge (omni-directional)
        if directed == False:
            self._edges[dst_key].add(src_key)
            self._weights[self.edge_key(dst_key, src_key)] = weight if weight != None else self.distance(src_key, dst_key)

    def clear(self) -> None:
        self.vert_data.clear()
        self.edge_data.clear()
        self.weight_data.clear()

    def vert_key(self, position: Tuple[int, int]) -> str:
        return f"{position}"
    
    def edge_key(self, src: str, dst: str) -> str:
        return f"{src}->{dst}"

    def distance(self, src_key: str, dst_key: str) -> float:
        src: Tuple[int, int] = self.get_pos(src_key)
        dst: Tuple[int, int] = self.get_pos(dst_key)
        print(f"Src: {src}({type(src)}) -> Dst: {dst}({type(dst)})")
        return sqrt(pow(src[0] - dst[0], 2) + pow(src[1] - dst[1], 2))
    
