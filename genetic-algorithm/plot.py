import json
import click
from igraph import *

@click.command()
@click.option('--file', type=click.Path(exists=True), help='path to .json file')
def run(file: str):
    result = dict()
    with open(file, mode='r') as input_file:
        result = json.loads(input_file.read())

    graph = Graph.TupleList(result['solution'], edge_attrs=['label'])
    plot(graph, file.replace('.json', '.png'), layout='tree', bbox=(1000, 1000))

if __name__ == '__main__':
    run()