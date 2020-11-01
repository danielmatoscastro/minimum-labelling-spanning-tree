from collections import namedtuple

class Edge(namedtuple('Edge', ['u', 'v', 'l'])):
    _hash = None
    _str = None
    def __eq__(self, other: "Edge") -> bool:
        nodes_are_equal = (self.u == other.u and self.v == other.v) or (self.v == other.u and self.u == other.v)
        labels_are_equal = self.l == other.l
        return nodes_are_equal and labels_are_equal

    def __hash__(self) -> int:
        if not self._hash:
            self._hash = self.u ^ self.v ^ self.l
        return self._hash

    def __str__(self) -> str:
        if not self._str:
            self._str = str(self.u) + str(self.v)
        return self._str