import random
from typing import List, Tuple
from math import ceil
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
        elite_size = ceil(self._elitism_rate*self._population_size)
        new_solutions_size = self._population_size - elite_size
        population = self._generate_initial_population()
        should_stop = False
        i = 1
        while not should_stop:
            evaluated_pop = self._evaluate_population(population)
            elite = self._elitism_operator(evaluated_pop, elite_size)
            new_solutions = self._crossover_operator(evaluated_pop, new_solutions_size)
            population = elite + self._mutation_operator(new_solutions)
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

    def _evaluate_population(self, population: List[List[Edge]]) -> List[Tuple[List[Edge], int, float]]:
        result = []

        for solution in population:
            labels = [edge.l for edge in solution]
            fitness = len(set(labels))
            result.append((solution, fitness))
        
        fitness_sum = sum([fitness for _, fitness in result])
        result = [(solution, fitness, fitness/fitness_sum) for solution, fitness in result]

        return result

    def _elitism_operator(self, population: List[Tuple[List[Edge], int, float]], elite_size: int) -> List[List[Edge]]:
        sorted_population = sorted(population, key=lambda x: x[1])
        return [solution for solution, _, _ in sorted_population[0:elite_size]]

    def _crossover_operator(self, population: List[Tuple[List[Edge], int, float]], new_solutions_size: int) -> List[List[Edge]]:
        new_solutions = []
        probs = [relative_fitness for _, _, relative_fitness in population]

        for i in range(new_solutions_size):
            father_1, father_2 = [solution for solution, _, _ in random.choices(population, weights=probs, k=2)]
            graph = set(father_1 + father_2)
            root = random.choice(graph)
            new_solutions.append(self._dfs_tree(root, []))

        return new_solutions

    def _mutation_operator(self, population: List[List[Edge]]) -> List[List[Edge]]:
        pass

    def _stopping_criterion(self, iteration: int) -> bool:
        return iteration == 10