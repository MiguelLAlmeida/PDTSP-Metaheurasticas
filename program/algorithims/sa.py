from program.core.algorithm import Algorithm
from program.core.solution import Solution

import math
import random

class SimulatedAnnealing(Algorithm):
    def __init__(self, initial_temperature, termination, problem, verbose = False):
        super().__init__(termination, problem, verbose)

        self.temperature = initial_temperature
        self.best_solution = None

    def initialize(self):
        self.initial_solution = self.__get_initial_solution()
        self.current_solution = self.initial_solution
        self.initial_temperature = 100

    def advance(self):
        neighbor_solution = self.__get_neighbors(self.current_solution)
        delta = neighbor_solution.cost - self.current_solution.cost

        if delta < 0:
            self.best_solution = self.current_solution = neighbor_solution
            if self.verbose:
                print('{} - {}'.format(self.n_iteration, self.best_solution.cost))
        else:
            if random.uniform(0, 1) < math.exp(-delta / self.initial_temperature):
                self.current_solution = neighbor_solution

        self.temperature = 0.97 * self.initial_temperature
        self.n_iteration += 1

    def finalize(self):
        pass

    def __get_initial_solution(self):
        initial_solution = Solution(
            value = random.sample(range(self.problem.size), self.problem.size)
        )
        initial_solution.cost = self.problem.evaluate(initial_solution.value)
        return initial_solution

    def __get_neighbors(self, current_solution):
        i, j = random.sample(list(range(self.problem.size)), 2)
        neighbor_solution = current_solution.copy()
        neighbor_solution.value[i], neighbor_solution.value[j] = neighbor_solution.value[j], neighbor_solution.value[i]
        neighbor_solution.cost = self.problem.evaluate(neighbor_solution.value)
        return neighbor_solution