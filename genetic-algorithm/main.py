import click
#import time
from model.instance import Instance
from genetic_algorithm import GeneticAlgorithm

@click.command()
@click.option('--file', type=click.Path(exists=True), help='path to .col file')
@click.option('--seed', type=click.FLOAT, help='rng seed')
@click.option('--population-size', type=click.INT, help='number of simultaneous solutions')
@click.option('--mutation-rate', type=click.FLOAT, help='probability of mutation for each solution')
@click.option('--elitism-rate', type=click.FLOAT, help='percentage of best solutions to be preserved')
def run(file, seed, population_size, mutation_rate, elitism_rate):
    instance = Instance.load(file)
    algorithm = GeneticAlgorithm(instance, 
                                seed,
                                population_size, 
                                mutation_rate, 
                                elitism_rate)
    #start = time.time()
    solution = algorithm.run()
    #end = time.time()
    print(solution)


if __name__ == '__main__':
    run()

