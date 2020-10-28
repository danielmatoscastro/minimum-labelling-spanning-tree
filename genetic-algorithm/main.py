from model.instance import Instance
from genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
    seed = 1
    population_size = 100
    mutation_rate = 0.7
    elitism_rate = 0.2

    instance = Instance.load('data/testFile_8_75_37.col')
    algorithm = GeneticAlgorithm(instance, 
                                seed,
                                population_size, 
                                mutation_rate, 
                                elitism_rate)
    solution = algorithm.run()
    print(solution)
