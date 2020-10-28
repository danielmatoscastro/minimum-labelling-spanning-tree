from model.instance import Instance
from genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
    seed = 1
    population_size = 50
    reproduction_rate = 1.0
    mutation_rate = 0.2
    elitism_rate = 0.2

    instance = Instance.load('data/testFile_8_75_37.col')
    algorithm = GeneticAlgorithm(instance, 
                                seed,
                                population_size, 
                                reproduction_rate, 
                                mutation_rate, 
                                elitism_rate)
    solution = algorithm.run()
    print(solution)
