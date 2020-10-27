from typing import List, Tuple
from model.instance import Instance
from model.edge import Edge

class GeneticAlgorithm:
    def __init__(self, instance: Instance, population_size: int, reproduction_rate: float, mutation_rate: float, elitism_rate: float):
        self._instance = instance
        self._population_size = population_size
        self._reproduction_rate = reproduction_rate
        self._mutation_rate = mutation_rate
        self._elitism_rate = elitism_rate

    def run(self) -> List[Edge]:
        population = self._generate_initial_population()
        
        while not self._stopping_criterion():
            evaluated_pop = self._evaluate_population(population)
            selected_pop = self._selection_operator(evaluated_pop)
            population_with_new_solutions = self._crossover_operator(selected_pop)
            population = self._mutation_operator(population_with_new_solutions)

        return self._select_solution(population)

    def _generate_initial_population(self) ->  List[List[Edge]]:
        pass

    def _evaluate_population(self, population: List[List[Edge]]) -> List[Tuple[List[Edge], int]]:
        pass

    def _selection_operator(self, population: List[Tuple[List[Edge], int]]) -> List[List[Edge]]:
        pass

    def _crossover_operator(self, population: List[List[Edge]]) -> List[List[Edge]]:
        pass

    def _mutation_operator(self, population: List[List[Edge]]) -> List[List[Edge]]:
        pass

    def _select_solution(self, population: List[List[Edge]]) -> List[Edge]:
        pass

    def _stopping_criterion(self) -> bool:
        pass