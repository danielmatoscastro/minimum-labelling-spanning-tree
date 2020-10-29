import unittest
from model.instance import Instance
from genetic_algorithm import GeneticAlgorithm

class TestGeneticAlgorithm(unittest.TestCase):
    def _build_algorithm(self) -> GeneticAlgorithm:
        seed = 1
        population_size = 5
        mutation_rate = 0.2
        elitism_rate = 0.2

        instance = Instance.load('data/testFile_0_10_5.col')
        return GeneticAlgorithm(instance, 
                                seed,
                                population_size,
                                mutation_rate, 
                                elitism_rate)

    def test_generate_initial_population(self):
        algorithm = self._build_algorithm()

        result = algorithm._generate_initial_population()

        self.assertEqual(5, len(result))
        for solution in result:
            self.assertEqual(9, len(solution))

    def test_generate_initial_population(self):
        algorithm = self._build_algorithm()
        population = algorithm._generate_initial_population()

        result = algorithm._evaluate_population(population)

        self.assertEqual(5, len(result))
        for solution, fitness, relative_fitness in result:
            self.assertEqual(9, len(solution))
            self.assertEqual(5, fitness)
            self.assertEqual(0.2, relative_fitness)

    def test_dfs_tree(self):
        algorithm = self._build_algorithm()

        result = algorithm._dfs_tree(0)

        self.assertEqual(9, len(result))

if __name__ == '__main__':
    unittest.main()