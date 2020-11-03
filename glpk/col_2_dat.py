from pathlib import Path

class Instance:
    def __init__(self, nodes: set, edges: set, labels: set, edges_to_labels: dict):
        self._nodes = nodes
        self._edges = edges
        self._labels = labels
        self._edges_to_labels = edges_to_labels

    @staticmethod
    def load(path: str) -> "Instance":
        with open(path, mode='r') as file:
            nodes = set()
            edges = set()
            labels = set()
            edges_to_labels = dict()

            file.readline()
            file.readline()
            for line in file.readlines():
                numbers = line.strip().split(' ')
                numbers = [int(number) for number in numbers]

                nodes.add(numbers[0])
                nodes.add(numbers[1])

                edges.add((numbers[0], numbers[1]))
                edges_to_labels[(numbers[0], numbers[1])] = numbers[2]
                if numbers[0] != 0:
                    edges.add((numbers[1], numbers[0]))
                    edges_to_labels[(numbers[1], numbers[0])] = numbers[2]

                labels.add(numbers[2])

            return Instance(nodes, edges, labels, edges_to_labels)

    def to_dat(self, path: str) -> None:
        with open(path, mode='w') as file:
            file.write(self._nodes_to_dat())
            file.write(self._edges_to_dat())
            file.write(self._labels_to_dat())
            labels_to_edges = self._calculate_labels_to_edges()
            file.write(self._edges_to_labels_to_dat(labels_to_edges))
            file.write(self._size_nodes_to_dat())
            file.write(self._size_edges_to_labels_to_dat(labels_to_edges))
            file.write('end;')

    def _nodes_to_dat(self) -> str:
        return 'set V := ' + '\n'.join({str(node) for node in self._nodes}) + ';\n\n'

    def _edges_to_dat(self) -> str:
        return 'set E:= \n' + \
                '\n'.join({str(edge) for edge in self._edges}) + \
                ';\n\n'

    def _labels_to_dat(self) -> str:
        return 'set L := ' + '\n'.join({str(label) for label in self._labels}) + ';\n\n'

    def _calculate_labels_to_edges(self) -> dict:
        labels_to_edges = dict()
        for edge, label in self._edges_to_labels.items():
            labels_to_edges.setdefault(label, []).append(edge)
        return labels_to_edges

    def _edges_to_labels_to_dat(self, labels_to_edges: dict) -> str:
        els = []
        for label in self._labels:
            el = f'set EL[{label}] :=\n' + \
                '\n'.join([str(edge) for edge in labels_to_edges[label]]) + \
                ';\n\n'
            els.append(el)

        return ''.join(els)

    def _size_nodes_to_dat(self) -> str:
        return f'param sizeV := {len(self._nodes)};\n\n'

    def _size_edges_to_labels_to_dat(self, labels_to_edges: dict) -> str:
        return 'param sizeEL := \n' + \
            '\n'.join([f'{label} {len(labels_to_edges[label])}' for label in self._labels]) + \
            ';\n\n'

if __name__ == '__main__':
    for path in Path('.', 'data').glob('*.col'):
        old_name = path.absolute().as_posix()
        new_name = path.absolute().as_posix().replace('col', 'dat')
        Instance.load(old_name).to_dat(new_name)