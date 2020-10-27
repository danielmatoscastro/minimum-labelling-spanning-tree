from model.instance import Instance
from genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
    instance = Instance.load('data/testFile_0_10_5.col')
    algorithm = GeneticAlgorithm(instance, 100, 1.0, 0.2, 0.2)
    solution = algorithm.run()
    print(solution)
