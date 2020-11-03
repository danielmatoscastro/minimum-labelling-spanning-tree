import click
import time
import json
from instance import Instance
from genetic_algorithm import GeneticAlgorithm

@click.command()
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
    solution = algorithm.run()
    stop_time = time.time()
    print(f'Solution fitness: {solution[1]}')
    print(f'Execution time: {stop_time - start_time}')
    
    solution_edges = []
    for node, neighbors in solution[0].items():
        for neighbor, label in neighbors:
            if (neighbor, node, label) not in solution_edges:
                solution_edges.append((node, neighbor, label))

    output = {
        'parameters': {
            'instance': file,
            'seed': seed,
            'population-size': population_size,
            'mutation-rate': mutation_rate,
            'elitism-rate': elitism_rate
        },
        'solution-fitness': solution[1],
        'execution-time': stop_time - start_time,
        'solution': solution_edges
    }

    with open(output_file, mode='w') as out_file:
        out_file.write(json.dumps(output, indent=2))        

if __name__ == '__main__':
    run()

