import matplotlib.pyplot as plt
import numpy as np
from main import load_pdtsp_instance
from program.problems.traveling_salesman import TravelingSalesmanProblem
from program.algorithims.ils import IterativeLocalSearch
from program.algorithims.brkga import BRKGA
from program.termination.maximum_iteration import MaximumIteration

def collect_data(problem, algo_type, target, runs=30):
    results = []
    print(f"\nColetando dados para {algo_type.__name__}...")
    
    for i in range(runs):
        term = MaximumIteration(5000) 
        
        if algo_type == IterativeLocalSearch:
            algo = algo_type(n_local_iter=100, p_size=5, termination=term, problem=problem)
        else:
            algo = algo_type(population_size=100, elite_prop=0.2, mutant_prop=0.1, rho=0.7, 
                            termination=term, problem=problem)
        algo.initialize()
        count = 0
        while algo.best_solution.cost > target and count < 5000:
            algo.advance()
            count += 1
        
        results.append(count)
        print(f"  Run {i+1}/{runs}: {count} iterações")
    
    return sorted(results)

def run_ttt():
    matrix, precs = load_pdtsp_instance("pdtsp-n105.txt")
    problem = TravelingSalesmanProblem(matrix, precs)
    
    target_value = 24000.0 
    n_runs = 20
    data_ils = collect_data(problem, IterativeLocalSearch, target_value, runs=n_runs)
    data_brkga = collect_data(problem, BRKGA, target_value, runs=n_runs)
    
    probs = [(i - 0.5) / n_runs for i in range(1, n_runs + 1)]
    
    plt.figure(figsize=(10, 6))
    plt.plot(data_ils, probs, 'o-', label='ILS', markersize=4)
    plt.plot(data_brkga, probs, 's-', label='BRKGA', markersize=4)
    
    plt.axvline(x=np.mean(data_ils), color='blue', linestyle='--', alpha=0.3, label='Média ILS')
    plt.axvline(x=np.mean(data_brkga), color='orange', linestyle='--', alpha=0.3, label='Média BRKGA')
    
    plt.title(f'Gráfico Time-to-Target (Target: {target_value})')
    plt.xlabel('Iterações (Tempo)')
    plt.ylabel('Probabilidade Acumulada')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('grafico_ttt.png')
    plt.show()

if __name__ == "__main__":
    run_ttt()