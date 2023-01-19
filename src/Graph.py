from typing import Dict, List, Tuple
from math import sqrt, pow

class Graph:
    
    def __init__(self):
        self._edges: Dict[str, set[str]] = {}
        self._weights: Dict[str, float] = {}
        self._positions: Dict[str, Tuple[int, int]] = {}

    def __str__(self) -> str:
        return f"""
        V={self.vertices}\n
        E={self.edges}
        """
    def __len__(self) -> int:
        return len(self._edges)

    @property
    def vertices(self) -> set[str]:
        return set(self._edges.keys())
    
    @property
    def edges(self) -> set[str]:
        return [[(src, dst) for dst in adjacent] for src, adjacent in self._edges.items()]

    @property
    def edge_data(self) -> Dict[str, set[str]]:
        return self._edges
    
    @property
    def weight_data(self) -> Dict[str, float]:
        return self._weights

    @property
    def pos_data(self) -> Dict[str, Tuple[int, int]]:
        return self._positions
    
    def adjacent(self, vert_key: str) -> set[str]:
        return self._edges[vert_key]

    def get_pos(self, vert_key: str) -> Tuple[int, int]:
        return self.pos_data[vert_key]
    
    def add_vert(self, vert_key: str, pos: Tuple[int, int]=None) -> None:
        self._edges[vert_key] = set()
        self._positions[vert_key] = pos
    
    def remove_vert(self, vert_key: str) -> None:
        for src_key, adjacent in self.edge_data.items():
            if vert_key in adjacent:
                self._edges[src_key].remove(vert_key)
                del self._weights[self._edge_key(src_key, vert_key)]
        if vert_key in self._edges.keys():
            del self.edge_data[vert_key]
    
    def add_edge(self, src_key: str, dst_key: str, weight: float=None, directed: bool=False) -> None:
        # make sure vertices are in graph
        if src_key not in self._edges.keys():
            self.add_vert(src_key)

        if dst_key not in self.vertices:
            self.add_vert(dst_key)

        # add directed edge
        self._edges[src_key].add(dst_key)
        self._weights[self.edge_key(src_key, dst_key)] = weight 
        # add reversed edge (omni-directional)
        if directed == False:
            self._edges[dst_key].add(src_key)
            self._weights[self.edge_key(dst_key, src_key)] = weight 

    def clear(self) -> None:
        self.edge_data.clear()
        self.weight_data.clear()
        self.pos_data.clear()

    def edge_key(self, src: str, dst: str) -> str:
        return f"{src}->{dst}"

    def distance(self, src_key: str, dst_key: str) -> float:
        src_x, src_y = self.pos_data[src_key]
        dst_x, dst_y = self.pos_data[dst_key]
        return sqrt(pow(src_x - dst_x, 2) + pow(src_y - dst_y, 2))
