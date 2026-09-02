import random
from program.core.algorithm import Algorithm
from program.core.solution import Solution

class BRKGA(Algorithm):
    def __init__(self, population_size, elite_prop, mutant_prop, rho, termination, problem, verbose=False):

        super().__init__(termination, problem, verbose)
        
        self.population_size = population_size  # tamanho total da população
        self.elite_prop = elite_prop            # proporção de indivíduos que farão parte da elite
        self.mutant_prop = mutant_prop          # proporção de mutantes introduzidos por geração
        self.rho = rho                          # probabilidade de herdar o gene do pai elite no crossover
        
        self.n_elite = int(population_size * elite_prop)                    # numero de elites total
        self.n_mutants = int(population_size * mutant_prop)                 # numero de mutantes total
        self.n_crossover = population_size - self.n_elite - self.n_mutants  # nuemro de crossovers que ocorre
        
        self.population = []                                                # vetor de população
        self.best_solution = None                                           # melhor solução até agora

    def initialize(self):
        self.n_iteration = 0                                                # iteração 
        self.population = []
        
        for _ in range(self.population_size):                               # gera a população inicial com chaves aleatórias
            keys = [random.random() for _ in range(self.problem.size)]
            ind = Solution(value=keys)                                      # o valor é a chave entre 0 e 1
            
            phenotype = self.__decode(keys)                                 # orgnaiza o vetor e guarda no fenotipo
            ind.cost = self.problem.evaluate(phenotype)                     # avialia o custo da solução
            
            ind.phenotype = phenotype 
            
            self.population.append(ind)                                     # insere na população
            
        self.population.sort(key=lambda x: x.cost)                          # ordena a população pelo custo de cada uma
        
        best_ind = self.population[0]
        self.best_solution = Solution(value=list(best_ind.phenotype))       # guarda a melhor solução e o custo dela
        self.best_solution.cost = best_ind.cost

    def advance(self):
        self.population.sort(key=lambda x: x.cost)                          # ordena a população pelo custo de cada uma
        
        if self.population[0].cost < self.best_solution.cost:               # verifica se há uma solução melhor e organiza elas
            best_ind = self.population[0]
            self.best_solution = Solution(value=list(best_ind.phenotype))
            self.best_solution.cost = best_ind.cost
            if self.verbose:
                print(f'Geração {self.n_iteration} - Melhor custo: {self.best_solution.cost}')
                
        elite = self.population[:self.n_elite]
        non_elite = self.population[self.n_elite:]                          # segrega os grupos entre elite e não elite
        
        next_population = []
        
        
        for ind in elite:                                                   # passa os elites para a próxima geração
            elite_copy = Solution(value=list(ind.value))
            elite_copy.cost = ind.cost
            elite_copy.phenotype = list(ind.phenotype)
            next_population.append(elite_copy)
            
        
        for _ in range(self.n_mutants):                                     # cria mutantes e coloca eles na população
            keys = [random.random() for _ in range(self.problem.size)]
            mutant = Solution(value=keys)
            phenotype = self.__decode(keys)
            mutant.cost = self.problem.evaluate(phenotype)
            mutant.phenotype = phenotype
            next_population.append(mutant)
            

        for _ in range(self.n_crossover):                                   # faz o crossover
            parent_elite = random.choice(elite)
            parent_non_elite = random.choice(non_elite)
            
            child_keys = []
            for g in range(self.problem.size):
                
                if random.random() < self.rho:                              # ve se é numero menor que a probabilidade de herdar o gene do pai elite
                    child_keys.append(parent_elite.value[g])
                else:
                    child_keys.append(parent_non_elite.value[g])
                    
            child = Solution(value=child_keys)
            phenotype = self.__decode(child_keys)
            child.cost = self.problem.evaluate(phenotype)
            child.phenotype = phenotype
            next_population.append(child)
            
        
        self.population = next_population                                   # avança a geração
        self.n_iteration += 1

    def finalize(self):
        if self.verbose:
            print(f'\n--- BRKGA Concluído ---')
            print(f'Melhor custo final: {self.best_solution.cost}')

    def __decode(self, keys):
        tour_indices = sorted(range(len(keys)), key=lambda k: keys[k])           # gera ordem com base nas chaves aleatórias
        
        repaired_tour = []
        pending_deliveries = set()
        
        delivery_to_pickup = {v: k for k, v in self.problem.precedences.items()} # mapeia para saber se um nó é entrega e qual sua coleta
        pickup_to_delivery = self.problem.precedences                            # mapeia para saber se um nó é coleta e qual sua entrega

        for node in tour_indices:
            if node in delivery_to_pickup:          # se é coleta
                pickup = delivery_to_pickup[node]
                if pickup in repaired_tour:         # se já ocorreu a coleta pode ser entregue
                    repaired_tour.append(node)
                else:
                    pending_deliveries.add(node)    # se não guarda na lista de espera
            
            else:                                   # se o nó for uma COLETA ou um NÓ COMUM
                repaired_tour.append(node)  
                if node in pickup_to_delivery:      
                    delivery = pickup_to_delivery[node]
                    if delivery in pending_deliveries: # se esse nó for uma coleta, verificamos se a entrega dele estava esperando
                        repaired_tour.append(delivery)
                        pending_deliveries.remove(delivery)

        for node in tour_indices:
            if node not in repaired_tour:  # se algum nó ficou de fora por lógica de precedencia
                repaired_tour.append(node)

        return repaired_tour