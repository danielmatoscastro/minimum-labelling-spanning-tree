from collections import defaultdict
import random
from typing import List, Tuple, Set, DefaultDict
from math import ceil
from instance import Instance

MAX_ITERATIONS = 2000
MAX_ITERATIONS_WITHOUT_IMPROVING = 2000
BEST_POSSIBLE_FITNESS = 1

Solution = DefaultDict[int, Set[Tuple[int, int]]]
EvaluatedSolution = Tuple[Solution, int, float]
Population = List[Solution]
EvaluatedPopulation = List[EvaluatedSolution]

class GeneticAlgorithm:
    '''Genetic Algorithm to solve the MLST problem.
   
    After instantiating, just call the run() method.

    Args:
        instance: MLST instance to be solved.
        seed: RNG seed.
        population_size: Number of simultaneous solutions.
        mutation_rate: Probability of a solution mutate.
        elitism_rate: Percentage of best solutions to be preserved across iterations.
    '''
    def __init__(self, instance: Instance, seed: int, population_size: int, mutation_rate: float, elitism_rate: float):
        self._instance = instance
        self._population_size = population_size
        self._mutation_rate = mutation_rate
        self._elitism_rate = elitism_rate
        random.seed(seed)

    def run(self) -> Tuple[EvaluatedSolution, EvaluatedSolution]:
        '''Runs the algorithm until reaching a stop criteria.

        Returns:
            Tuple with first solution and last solution (in this order).
        '''
        elite_size = ceil(self._elitism_rate*self._population_size)
        new_solutions_size = self._population_size - elite_size
        population = self._generate_initial_population()
        should_stop = False
        i = 1
        last_improvement = 1
        first_solution = None
        best_solution = None
        while not should_stop:
            print(f'iteration {i}')
            evaluated_pop = self._evaluate_population(population)
            elite = self._elitism_operator(evaluated_pop, elite_size)

            if i == 1:
                first_solution = evaluated_pop[0]
            if not best_solution or best_solution[1] > evaluated_pop[0][1]:
                best_solution = evaluated_pop[0]
                last_improvement = i

            new_solutions = self._crossover_operator(evaluated_pop, new_solutions_size)
            population = elite + self._mutation_operator(new_solutions)
            should_stop = self._stopping_criterion(best_solution, last_improvement, i)
            i += 1

        return (first_solution, best_solution)

    def _generate_initial_population(self) -> Population:
        ''' Generates the initial solutions.
        
        Each spanning tree is created by recording the selected edges during a DFS on the whole graph.
        
        Each DFS runs with a random root.
        
        Returns:
            List with initial candidate solutions.    
        '''
        population = []
        roots = random.choices(self._instance.nodes, k=self._population_size)
       
        for root in roots:
            population.append(self._dfs_tree(root))

        return population

    def _dfs_tree(self, root: int, solution: Solution = None) -> Solution:
        '''Generates a spanning tree through DFS.

        Args:
            root: Initial spanning tree node.
            solution: Graph to be traversed. Defaults to None.
                If its value is falsy (like the `None` default), then `self._instance.adjacency_list` is used.
        
        Returns:
            Spanning tree.
        '''
        if not solution:
            solution = self._instance.adjacency_list

        return self._dfs_tree_internal(root, {root, }, defaultdict(set), solution)

    def _dfs_tree_internal(self, root: int, expanded_nodes: Set[int], new_solution: Solution, solution: Solution) -> Solution:
        '''Generates a spanning tree through DFS.

        This method must not be used directly. Use the wrapper `self._dfs_tree` instead.

        Args:
            root: Initial spanning tree node.
            expanded_nodes: Nodes already visited.
            new_solution: Solution being calculated.
            solution: Graph being traversed.

        Returns:
            Spanning tree.
        '''
        neighbors = list(solution[root])
        random.shuffle(neighbors)

        for neighbor, label in neighbors:
            if neighbor not in expanded_nodes:
                expanded_nodes.add(neighbor)
                new_solution[root].add((neighbor, label))
                new_solution[neighbor].add((root, label))
                self._dfs_tree_internal(neighbor, expanded_nodes, new_solution, solution)

        return new_solution

    def _evaluate_population(self, population: Population) -> EvaluatedPopulation:
        '''Computes the absolute and relative fitness for each solution.

        Args:
            population: Solutions whose fitness will be calculated.

        Returns:
            A list of tuples with a solution as the first component, the absolute fitness as second 
                and the relative fitness as third. The result is sorted by absolute fitness, 
                in ascending order.
        '''
        result = []

        for solution in population:
            labels = set()
            for edges_list in solution.values():
                for _, label in edges_list:
                    labels.add(label)
            fitness = len(labels)
            result.append((solution, fitness))
        
        fitness_sum = sum([fitness for _, fitness in result])
        result = [(solution, fitness, fitness/fitness_sum) for solution, fitness in result]
        sorted_result = sorted(result, key=lambda x: x[1])
        return sorted_result

    def _elitism_operator(self, population: EvaluatedPopulation, elite_size: int) -> Population:
        '''Generates a list with the best solutions.

        Args:
            population (List[Tuple[List[Edge], int, float]]): Popolation already evaluated and sorted.
            elite_size (int): Number of best solutions to be selected.

        Returns:
            List of `elite_size` best solutions.
        '''
        return [solution for solution, _, _ in population[0:elite_size]]

    def _crossover_operator(self, population: EvaluatedPopulation, new_solutions_size: int) -> Population:
        '''Produces a new population applying crossover in the current population.

        This method implements the `roulette method`.
        
        Two solutions are combined by merging its edges and applying DFS from a random root.

        Args:
            population: Current population already evaluated.
            new_solutions_size: Size of new population.

        Returns:
            New population.
        '''
        new_solutions = []
        probs = [relative_fitness for _, _, relative_fitness in population]

        for i in range(new_solutions_size):
            father_1, father_2 = [solution for solution, _, _ in random.choices(population, weights=probs, k=2)]
            child = defaultdict(Set)
            for node in self._instance.nodes:
                child[node] = father_1[node].union(father_2[node])
            
            root = random.choice(self._instance.nodes)
            new_solutions.append(self._dfs_tree(root, child))

        return new_solutions

    def _mutation_operator(self, population: Population) -> Population:
        '''Applies random mutations in population.

        Each solution will be mutated with probability `self._mutation_rate`.
        
        The mutation is doing by selecting a random node as root and setting its neigbors as all neighbors from the problem instance.
        Lastly, we apply DFS in this solution, starting from selected root.

        Args:
            population: Population to be mutated.

        Returns:
            New population.
        '''
        new_solutions =[]

        for solution in population:
            should_mutate = random.choices([True, False], weights=[self._mutation_rate, 1-self._mutation_rate])[0]
            # 'in' operator is EXTREMELY FASTER with sets. 55s with lists, 16s with sets.
            if should_mutate:
                root = random.choice(self._instance.nodes)
                solution[root] = self._instance.adjacency_list[root]
                for neighbor, label in solution[root]:
                    solution[neighbor].add((root, label))
                new_solutions.append(self._dfs_tree(root, solution))
            else:
                new_solutions.append(solution)

        return new_solutions

    def _stopping_criterion(self, best_solution: EvaluatedSolution, last_improvement: int, iteration: int) -> bool:
        '''Decides if must stop the algorithm.

        Args:
            best_solution: Best solution found in the last iteration, already evaluated. 
            last_improvement: Last iteration in which a better solution was found.
            iteration:  Number of executed iterations.

        Returns:
            True if the algorithm must stop. False otherwise.
        '''
        return best_solution[1] == BEST_POSSIBLE_FITNESS or \
                iteration-last_improvement == MAX_ITERATIONS_WITHOUT_IMPROVING or \
                iteration == MAX_ITERATIONS