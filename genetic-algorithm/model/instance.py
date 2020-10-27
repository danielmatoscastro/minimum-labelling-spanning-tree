from typing import List
from .edge import Edge

class Instance:
    def __init__(self, nodes: list = [], edges: list = [], labels: list = []):
        self._nodes = nodes
        self._edges = edges
        self._labels = labels

    @property
    def nodes(self) -> List[int]:
        return self._nodes

    @property
    def edges(self) -> List[Edge]:
        return self._edges

    @staticmethod
    def load(path: str) -> "Instance":
        with open(path, mode='r') as file:
            nodes = set()
            edges = set()
            labels = set()

            file.readline()
            for line in file.readlines():
                numbers = line.strip().split(' ')
                numbers = [int(number) for number in numbers]

                nodes.add(numbers[0])
                nodes.add(numbers[1])

                edges.add(Edge(*numbers))

                labels.add(numbers[2])

            return Instance(list(nodes), list(edges), list(labels))