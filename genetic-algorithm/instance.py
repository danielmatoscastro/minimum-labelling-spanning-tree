from collections import defaultdict
from typing import List, DefaultDict, Set, Tuple

class Instance:
    def __init__(self, nodes: List = [], edges: List = [], labels: List = []):
        self._nodes = nodes
        self._edges = edges
        self._labels = labels
        self._adjacency_list = defaultdict(set)
        for edge in self._edges:
            self._adjacency_list[edge[0]].add((edge[1], edge[2]))
            self._adjacency_list[edge[1]].add((edge[0], edge[2]))

    @property
    def nodes(self) -> List[int]:
        return self._nodes

    @property
    def edges(self) -> List[Tuple[int, int, int]]:
        return self._edges

    @property
    def adjacency_list(self) -> DefaultDict[int, Set[Tuple[int, int]]]:
        return self._adjacency_list

    @staticmethod
    def load(path: str) -> "Instance":
        with open(path, mode='r') as file:
            nodes = set()
            edges = set()
            labels = set()

            file.readline()
            file.readline()
            for line in file.readlines():
                numbers = line.strip().split(' ')
                numbers = [int(number) for number in numbers]

                nodes.add(numbers[0])
                nodes.add(numbers[1])

                edges.add(tuple(numbers))

                labels.add(numbers[2])

            return Instance(list(nodes), list(edges), list(labels))