import unittest
from model.instance import Instance
from genetic_algorithm import GeneticAlgorithm

class TestGeneticAlgorithm(unittest.TestCase):
    def _build_algorithm(self) -> GeneticAlgorithm:
        seed = 1
        population_size = 5
        reproduction_rate = 1.0
        mutation_rate = 0.2
        elitism_rate = 0.2

        instance = Instance.load('data/testFile_0_10_5.col')
        return GeneticAlgorithm(instance, 
                                seed,
                                population_size, 
                                reproduction_rate, 
                                mutation_rate, 
                                elitism_rate)

    def test_generate_initial_population(self):
        algorithm = self._build_algorithm()

        result = algorithm._generate_initial_population()

        self.assertEqual(5, len(result))
        for solution in result:
            self.assertEqual(9, len(solution))

if __name__ == '__main__':
    unittest.main()