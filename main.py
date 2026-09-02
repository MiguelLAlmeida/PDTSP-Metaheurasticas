from program.problems.traveling_salesman import TravelingSalesmanProblem
from program.algorithims.ils import IterativeLocalSearch
from program.algorithims.brkga import BRKGA
from program.termination.maximum_iteration import MaximumIteration

import os
import math

def load_pdtsp_instance(filename):
    """
    Carrega os dados da instância, coordenadas e regras de precedência.
    """
    path = os.path.join("program", "instances", filename)
    nodes = []
    precedences = {}
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado em: {path}")

    with open(path, 'r') as f:
        lines = f.readlines()
    
    try:
        num_nodes = int(lines[0].strip())
    except (ValueError, IndexError):
        raise ValueError("A primeira linha do arquivo deve ser o número de cidades.")
        
    for line in lines[1:]:
        parts = line.split()
        if not parts or parts[0] == "-999":
            break

        x, y = float(parts[1]), float(parts[2])
        nodes.append((x, y))


        if len(parts) >= 5 and parts[3] == "1":
            coleta = int(parts[0]) - 1 
            entrega = int(parts[4]) - 1 
            precedences[coleta] = entrega

    n = len(nodes)
    dist_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = math.sqrt((nodes[i][0]-nodes[j][0])**2 + 
                                          (nodes[i][1]-nodes[j][1])**2)

    return dist_matrix, precedences

def run_single_comparison():
    """
    Executa uma rodada de cada meta-heurística para comparação rápida.
    """
    instance_file = "pdtsp-n105.txt" 
    matrix, precs = load_pdtsp_instance(instance_file)
    problem = TravelingSalesmanProblem(matrix, precs)
    
    print(f"Instância '{instance_file}' carregada: {len(matrix)} cidades e {len(precs)} regras.")


    print("\n" + "="*30)
    print("INICIANDO ILS")
    print("="*30)
    term_ils = MaximumIteration(2000)
    ils = IterativeLocalSearch(n_local_iter=200, p_size=5, 
                               termination=term_ils, problem=problem, verbose=True)
    ils.run()

    print("\n" + "="*30)
    print("INICIANDO BRKGA")
    print("="*30)
    term_brkga = MaximumIteration(200)
    brkga = BRKGA(population_size=100, elite_prop=0.2, mutant_prop=0.1, rho=0.7,
                  termination=term_brkga, problem=problem, verbose=True)
    brkga.run()

    print("\n" + "═"*40)
    print(f"RESUMO DOS RESULTADOS ({instance_file})")
    print(f"Melhor Custo ILS:   {ils.best_solution.cost:.2f}")
    print(f"Melhor Custo BRKGA: {brkga.best_solution.cost:.2f}")
    print("═"*40)

if __name__ == "__main__":
    run_single_comparison()