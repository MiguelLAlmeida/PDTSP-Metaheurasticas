from program.core.algorithm import Algorithm
from program.core.solution import Solution

import random
 
class IterativeLocalSearch(Algorithm):
    def __init__(self, p_size, n_local_iter, termination, problem, verbose=False):
        super().__init__(termination, problem, verbose)
        self.n_local_iter = n_local_iter # tentativas da busca local
        self.p_size = p_size             # força da perturbação
        self.best_solution = None       

    #def in_bounds(self, point, bounds):
    #    for d in range(len(bounds)):
    #        if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]: # verifica se o ponto está dentro dos limites declarados
    #            return False # se for maior ou menor, retorna falso
    #     return True # se estiver dentro dos limites, retorna verdadeiro
    
    def hillclimbing(self, start_tour):                     
        current_tour = list(start_tour)                         
        current_cost = self.problem.evaluate(current_tour)

        for _ in range(self.n_local_iter):
            i, j = random.sample(range(len(current_tour)), 2)                    
                                                                                    # faz trocas aleatórias n_loca_iter vezes
            current_tour[i], current_tour[j] = current_tour[j], current_tour[i]     # pega uma cidade e troca de lugar na rota com outra
            new_cost = self.problem.evaluate(current_tour)

            if new_cost < current_cost:                                             # caso a troca tenha melhorado o valor da rota
                current_cost = new_cost                                             # o valor atual da rota passa ser o valor melhor
            else:
                current_tour[i], current_tour[j] = current_tour[j], current_tour[i] # caso contrário, desfaz a troca das cidades
        
        return current_tour, current_cost
    
    def initialize(self):                                       # algoritmo que garante que uma rota seja válida
        
        pickups = list(self.problem.precedences.keys())         # lista de todas as cidades qu  e são pontos de coleta
        deliveries = list(self.problem.precedences.values())    # lista de todas as cidades que são pontos de entrega
        
        valid_tour = [0]                                        
        for p in pickups:
            if p != 0: valid_tour.append(p)                     # adiciona todas coletas
        for d in deliveries:
            if d != 0: valid_tour.append(d)                     # adiciona todas entregas
            
        for i in range(self.problem.size):                      # acrescenta até cidades que não são nenhum dos 2 pontos
            if i not in valid_tour:                             # são apenas pontos de passaem
                valid_tour.append(i)

        self.best_solution = Solution(value=valid_tour)         # cria o objeto da solução 
        self.best_solution.cost = self.problem.evaluate(self.best_solution.value) # calcula o custo real
        self.n_iteration = 0

    def advance(self):
        perturbed_tour = list(self.best_solution.value)                 # pega a melhor solução até agora e faz algumas trocas aleatorias
        for _ in range(self.p_size):                                    # permitindo o algoritmo procurar em novos lugares e achar
            idx1, idx2 = random.sample(range(len(perturbed_tour)), 2)   # novas possibilidades de rotas sem abandoa a melhor até agora
            perturbed_tour[idx1], perturbed_tour[idx2] = perturbed_tour[idx2], perturbed_tour[idx1]

        new_tour, new_cost = self.hillclimbing(perturbed_tour)          # passa a rota bagunçada para o hill climbling que fará
                                                                        # modificações na rota trocando cidades de lugar para encontrar a melhor rota
        
        if new_cost < self.best_solution.cost:  # se o custo da rota enontrada for melhor doq a atual
            self.best_solution.value = new_tour # atualiza a variável melhor rota para a encontrada
            self.best_solution.cost = new_cost  # juntamente da variável melhor custo
            if self.verbose:
                print(f'Iteração {self.n_iteration}: Melhor custo = {self.best_solution.cost:.2f}')

        self.n_iteration += 1
    
    def finalize(self):
        if self.verbose:
            print(f'ILS finalizado. Melhor custo encontrado: {self.best_solution.cost}')
    