from collections import namedtuple

class Edge(namedtuple('Edge', ['u', 'v', 'l'])):
    def __eq__(self, other: "Edge") -> bool:
        if not isinstance(other, Edge):
            return False
            
        nodes_are_equal = (self.u == other.u and self.v == other.v) or (self.v == other.u and self.u == other.v)
        labels_are_equal = self.l == other.l
        return nodes_are_equal and labels_are_equal

    def __hash__(self) -> int:
        return self.u ^ self.v ^ self.l