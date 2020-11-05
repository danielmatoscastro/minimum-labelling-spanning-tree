import click
import time
import json
from statistics import stdev
from instance import Instance
from genetic_algorithm import GeneticAlgorithm
from igraph import Graph
from igraph import plot as _plot

def get_solution_edges(solution):
    solution_edges = []
    for node, neighbors in solution[0].items():
        for neighbor, label in neighbors:
            if (neighbor, node, label) not in solution_edges:
                solution_edges.append((node, neighbor, label))
    return solution_edges

@click.group()
def cli():
    pass

@cli.command()
@click.option('--file', type=click.Path(exists=True), help='path to .col file')
@click.option('--seed', type=click.FLOAT, help='rng seed')
@click.option('--population-size', type=click.INT, help='number of simultaneous solutions')
@click.option('--mutation-rate', type=click.FLOAT, help='probability of mutation for each solution')
@click.option('--elitism-rate', type=click.FLOAT, help='percentage of best solutions to be preserved')
@click.option('--output-file', type=click.STRING, help='path for output json file')
def run(file, seed, population_size, mutation_rate, elitism_rate, output_file):
    instance = Instance.load(file)
    algorithm = GeneticAlgorithm(instance, 
                                seed,
                                population_size, 
                                mutation_rate, 
                                elitism_rate)
    start_time = time.time()
    first_solution, solution = algorithm.run()
    stop_time = time.time()
    print(f'Solution fitness: {solution[1]}')
    print(f'Execution time: {stop_time - start_time}')
    
    solution_edges = get_solution_edges(solution)

    output = {
        'parameters': {
            'instance': file,
            'seed': seed,
            'population-size': population_size,
            'mutation-rate': mutation_rate,
            'elitism-rate': elitism_rate
        },
        'first-solution-fitness': first_solution[1],
        'solution-fitness': solution[1],
        'execution-time': stop_time - start_time,
        'solution': solution_edges
    }

    with open(output_file, mode='w') as out_file:
        out_file.write(json.dumps(output, indent=2))        


@cli.command()
@click.option('--file', type=click.Path(exists=True), help='path to .json file')
def plot(file: str):
    result = dict()
    with open(file, mode='r') as input_file:
        result = json.loads(input_file.read())

    graph = Graph.TupleList(result['solution'], edge_attrs=['label'])
    _plot(graph, file.replace('.json', '.png'), layout='tree', bbox=(1000, 1000))

@cli.command()
@click.option('--file', type=click.Path(exists=True), help='path to .col file')
@click.option('--population-size', type=click.INT, help='number of simultaneous solutions')
@click.option('--mutation-rate', type=click.FLOAT, help='probability of mutation for each solution')
@click.option('--elitism-rate', type=click.FLOAT, help='percentage of best solutions to be preserved')
@click.option('--bks', type=click.INT, help='best known solution')
@click.option('--output-file', type=click.STRING, help='path for output json file')
def run_multiple(file, population_size, mutation_rate, elitism_rate, bks, output_file):
    instance = Instance.load(file)
    outputs = []
    for i in range(1, 11):
        algorithm = GeneticAlgorithm(instance, 
                                    i,
                                    population_size, 
                                    mutation_rate, 
                                    elitism_rate)
        print(f'Executing test {i}.')
        start_time = time.time()
        first_solution, solution = algorithm.run()
        stop_time = time.time()
        print(f'Solution fitness: {solution[1]}')
        print(f'Execution time: {stop_time - start_time}')

        solution_edges = get_solution_edges(solution)

        output = {
            'parameters': {
                'instance': file,
                'seed': i,
                'population-size': population_size,
                'mutation-rate': mutation_rate,
                'elitism-rate': elitism_rate
            },
            'first-solution-fitness': first_solution[1],
            'solution-fitness': solution[1],
            'execution-time': stop_time - start_time,
            'solution': solution_edges,
            'percentage-deviation': 100 * (solution[1] - bks) / bks
        }

        outputs.append(output)

    first_solution_fitness = []
    fitness = []
    times = []
    percentage_deviation = []
    output_combined = dict()
    for i, output in enumerate(outputs):
        output_combined[f'execution-{i+1}'] = output
        first_solution_fitness.append(output['first-solution-fitness'])
        fitness.append(output['solution-fitness'])
        times.append(output['execution-time'])
        percentage_deviation.append(output['percentage-deviation'])

    output_combined['result'] = {
        'average-first-solution': sum(first_solution_fitness) / 10,
        'average-solution': sum(fitness) / 10,
        'average-time': sum(times) / 10,
        'std-solution': stdev(fitness),
        'std-time': stdev(times),
        'best-solution': min(fitness),
        'worst-solution': max(fitness),
        'best-known-solution': bks,
        'average-percentage-deviation': sum(percentage_deviation) / 10
    }

    with open(output_file, mode='w') as out_file:
        out_file.write(json.dumps(output_combined, indent=2))       

if __name__ == '__main__':
    cli()

