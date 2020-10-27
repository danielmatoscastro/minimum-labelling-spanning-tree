import random
from typing import List, Tuple
from model.instance import Instance
from model.edge import Edge

class GeneticAlgorithm:
    def __init__(self, instance: Instance, seed: int, population_size: int, reproduction_rate: float, mutation_rate: float, elitism_rate: float):
        self._instance = instance
        self._population_size = population_size
        self._reproduction_rate = reproduction_rate
        self._mutation_rate = mutation_rate
        self._elitism_rate = elitism_rate
        random.seed(seed)

    def run(self) -> List[Edge]:
        population = self._generate_initial_population()
        should_stop = False
        i = 1
        while not should_stop:
            evaluated_pop = self._evaluate_population(population)
            selected_pop = self._selection_operator(evaluated_pop)
            population_with_new_solutions = self._crossover_operator(selected_pop)
            population = self._mutation_operator(population_with_new_solutions)
            should_stop = self._stopping_criterion(i)
            i += 1

        return self._select_solution(population)

    def _generate_initial_population(self) ->  List[List[Edge]]:
        population = []

        for root in random.sample(self._instance.nodes, k=self._population_size):
            population.append(self._dfs_tree(root, [root, ]))

        return population

    def _dfs_tree(self, root: int, expanded_nodes: List[int], expanded_edges: List[Edge] = []) -> List[Edge]:
        edges = [edge for edge in self._instance.edges if edge.u == root and edge.v not in expanded_nodes]
        
        for edge in edges:
            expanded_nodes.append(edge.v)
            expanded_edges.append(edge)
            self._dfs_tree(edge.v, expanded_nodes, expanded_edges)

        return expanded_edges

    def _evaluate_population(self, population: List[List[Edge]]) -> List[Tuple[List[Edge], int]]:
        result = []

        for solution in population:
            labels = [edge.l for edge in solution]
            fitness = len(set(labels))
            result.append((solution, fitness))
        
        return result

    def _selection_operator(self, population: List[Tuple[List[Edge], int]]) -> List[List[Edge]]:
        pass

    def _crossover_operator(self, population: List[List[Edge]]) -> List[List[Edge]]:
        pass

    def _mutation_operator(self, population: List[List[Edge]]) -> List[List[Edge]]:
        pass

    def _select_solution(self, population: List[List[Edge]]) -> List[Edge]:
        pass

    def _stopping_criterion(self, iteration: int) -> bool:
        return iteration == 10