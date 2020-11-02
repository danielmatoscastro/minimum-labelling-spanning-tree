import random
from typing import List, Tuple, Set
from math import ceil
from model.instance import Instance
from model.edge import Edge

MAX_ITERATIONS = 500
MAX_ITERATIONS_WITHOUT_IMPROVING = 200
BEST_POSSIBLE_FITNESS = 1

class GeneticAlgorithm:
    '''Genetic Algorithm to solve the MLST problem.
   
    After instantiating, just call the run() method.

    Args:
        instance (Instance): MLST instance to be solved.
        seed (int): RNG seed.
        population_size (int): Number of simultaneous solutions.
        mutation_rate (float): Probability of a solution mutate.
        elitism_rate (float): Percentage of best solutions to be preserved across iterations.
    '''
    def __init__(self, instance: Instance, seed: int, population_size: int, mutation_rate: float, elitism_rate: float):
        self._instance = instance
        self._population_size = population_size
        self._mutation_rate = mutation_rate
        self._elitism_rate = elitism_rate
        self._edges_set = set(self._instance.edges)
        random.seed(seed)

    def run(self) -> Tuple[List[Edge], int, float]:
        '''Runs the algorithm until reaching a stop criteria.

        Returns:
            Tuple with solution, absolute fitness, and relative fitness (in this order).
        '''
        elite_size = ceil(self._elitism_rate*self._population_size)
        new_solutions_size = self._population_size - elite_size
        population = self._generate_initial_population()
        should_stop = False
        i = 1
        last_improvement = 1
        best_solution = None
        while not should_stop:
            print(f'iteration {i}')
            evaluated_pop = self._evaluate_population(population)
            elite = self._elitism_operator(evaluated_pop, elite_size)

            if not best_solution or best_solution[1] > evaluated_pop[0][1]:
                best_solution = evaluated_pop[0]
                last_improvement = i

            new_solutions = self._crossover_operator(evaluated_pop, new_solutions_size)
            population = elite + self._mutation_operator(new_solutions)
            should_stop = self._stopping_criterion(best_solution, last_improvement, i)
            i += 1

        return best_solution

    def _generate_initial_population(self) ->  List[List[Edge]]:
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

    def _dfs_tree(self, root: int, solution: List[Edge] = None) -> List[Edge]:
        '''Generates a spanning tree through DFS.

        Args:
            root (int): Initial spanning tree node.
            solution (List[Edge], optional): Graph to be traversed. Defaults to None.
                If its value is falsy (like the `None` default), then `self._instance.edges` is used.
        
        Returns:
            Spanning tree.
        '''
        if not solution:
            solution = self._instance.edges

        return self._dfs_tree_internal(root, {root, }, [], solution)

    def _dfs_tree_internal(self, root: int, expanded_nodes: Set[int], expanded_edges: List[Edge], solution: List[Edge]) -> List[Edge]:
        '''Generates a spanning tree through DFS.

        This method must not be used directly. Use the wrapper `self._dfs_tree` instead.

        Args:
            root (int): Initial spanning tree node.
            expanded_nodes (Set[int]): Nodes already visited.
            expanded_edges (List[Edge]): Edges already choosed.
            solution (List[Edge]): Graph being traversed.

        Returns:
            Spanning tree.
        '''
        edges = self._find_all_possible_nodes(root, solution)
        random.shuffle(edges)

        for node, edge in edges:
            if node not in expanded_nodes:
                expanded_nodes.add(node)
                expanded_edges.append(edge)
                self._dfs_tree_internal(node, expanded_nodes, expanded_edges, solution)

        return expanded_edges

    def _find_all_possible_nodes(self, root: int, solution: List[Edge]) -> List[Tuple[int, Edge]]:
        '''Generates a list with all neighbors of root.

        The output is a list of pairs, with a node `u` as the first component and an edge `(root, u)`
        or `(u, root)` as second.

        Args:
            root (int): Node whose neighbors will be found.
            solution (List[Édge]): Graph being traversed.

        Returns:
            All neighbors of root and the edges between them.
        '''
        pairs = []
        for edge in solution:
            if edge.u == root:
                pairs.append((edge.v, edge))
            elif edge.v == root:
                pairs.append((edge.u, edge))

        return pairs

    def _evaluate_population(self, population: List[List[Edge]]) -> List[Tuple[List[Edge], int, float]]:
        '''Computes the absolute and relative fitness for each solution.

        Args:
            population (List[List[Edge]]): Solutions whose fitness will be calculated.

        Returns:
            A list of tuples with a solution as the first component, the absolute fitness as second 
                and the relative fitness as third. The result is sorted by absolute fitness, 
                in ascending order.
        '''
        result = []

        for solution in population:
            labels = [edge.l for edge in solution]
            fitness = len(set(labels))
            result.append((solution, fitness))
        
        fitness_sum = sum([fitness for _, fitness in result])
        result = [(solution, fitness, fitness/fitness_sum) for solution, fitness in result]
        sorted_result = sorted(result, key=lambda x: x[1])
        return sorted_result

    def _elitism_operator(self, population: List[Tuple[List[Edge], int, float]], elite_size: int) -> List[List[Edge]]:
        '''Generates a list with the best solutions.

        Args:
            population (List[Tuple[List[Edge], int, float]]): Popolation already evaluated and sorted.
            elite_size (int): Number of best solutions to be selected.

        Returns:
            List of `elite_size` best solutions.
        '''
        return [solution for solution, _, _ in population[0:elite_size]]

    def _crossover_operator(self, population: List[Tuple[List[Edge], int, float]], new_solutions_size: int) -> List[List[Edge]]:
        '''Produces a new population applying crossover in the current population.

        This method implements the `roulette method`.
        
        Two solutions are combined by merging its edges in a list and applying DFS from a random root.

        Args:
            population (List[Tuple[List[Edge], int, float]]): Current population already evaluated.
            new_solutions_size (int): Size of new population.

        Returns:
            New population.
        '''
        new_solutions = []
        probs = [relative_fitness for _, _, relative_fitness in population]

        for i in range(new_solutions_size):
            father_1, father_2 = [solution for solution, _, _ in random.choices(population, weights=probs, k=2)]
            graph = list(set(father_1 + father_2))
            root = random.choice(self._instance.nodes)
            new_solutions.append(self._dfs_tree(root, graph))

        return new_solutions

    def _mutation_operator(self, population: List[List[Edge]]) -> List[List[Edge]]:
        '''Applies random mutations in population.

        Each solution will be mutated with probability `self._mutation_rate`.
        
        The mutation is doing by merging the solution edges with 10% of the graph edges
        that aren't in solution and applying DFS in this list, starting from a random root.

        Args:
            population (List[List[Edge]]): Population to be mutated.

        Returns:
            New population.
        '''
        new_solutions =[]

        for solution in population:
            should_mutate = random.choices([True, False], weights=[self._mutation_rate, 1-self._mutation_rate])[0]
            # 'in' operator is EXTREMELY FASTER with sets. 55s with lists, 16s with sets.
            solution_set = set(solution)
            if should_mutate:
                edges_complement = list(self._edges_set.difference(solution_set))
                additional_edges_quant = ceil(0.10*len(edges_complement))
                additional_edges = random.choices(edges_complement, k=additional_edges_quant)
                edges_total = solution + additional_edges
                root = random.choice(self._instance.nodes)
                new_solutions.append(self._dfs_tree(root, edges_total))
            else:
                new_solutions.append(solution)

        return new_solutions

    def _select_solution(self, population: List[List[Edge]]) -> Tuple[List[Edge], int, float]:
        '''Returns the best solution of a population.

        Args:
            population (List[List[Edge]]): Population.

        Returns:
            Best solution from the population.
        '''
        evaluated_pop = self._evaluate_population(population)
        return min(evaluated_pop, key=lambda x: x[1])

    def _stopping_criterion(self, best_solution: Tuple[List[Edge], int, float], last_improvement: int, iteration: int) -> bool:
        '''Decides if must stop the algorithm.

        Args:
            best_solution (Tuple[List[Edge], int, float]): Best solution found in the last iteration,
                already evaluated. 
            last_improvement (int): Last iteration in which a better solution was found.
            iteration (int):  Number of executed iterations.

        Returns:
            True if the algorithm must stop. False otherwise.
        '''
        return best_solution[1] == BEST_POSSIBLE_FITNESS or \
                iteration-last_improvement == MAX_ITERATIONS_WITHOUT_IMPROVING or \
                iteration == MAX_ITERATIONS