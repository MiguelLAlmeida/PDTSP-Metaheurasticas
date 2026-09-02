from program.core.problem import Problem

class TravelingSalesmanProblem(Problem):
    def __init__(self, distances, precedences):
        self.precedences = precedences # dicionario para definir o {nó da coleta e o nó de entrega}
                                       # para desconsiderar rotas em que a entrega vem antes da coleta.
        self.distances = distances
        self.n_cities = len(distances) # passar n_cities por parametro é desnecessario e pode gerar conflitos caso o valor não bata
                                       # com a proporção da matriz de distancias, para evitar isso, utiliza-se len(distancies)

    def evaluate(self, tour):
        visited = []
        for node in tour:
            for pickup, delivery in self.precedences.items(): # caso o nó acessado seja um entrega, fazendo uma verificação
                if node == delivery:                          # para saber se já passamos pela coleta.
                    if pickup not in visited:                 # caso não tenha passado, retorna um valor altissimo 
                        return 9999999.0                      # para que o algoritmo descarte essa rota.
            visited.append(node)
        
        cost = 0
        for i in range(len(tour)):                     # para calcular a distancia que está sendo percorrida
            from_node = tour[i]                        # encontramos a origem e destino e procuramos o valor desse
            to_node = tour[(i + 1) % len(tour)]        # trajeto dentro da matriz de distancias e acrescenta
            cost += self.distances[from_node][to_node] # esse valor na variável de custo que será retornada

        return cost
    
    @property
    def size(self):
        return self.n_cities