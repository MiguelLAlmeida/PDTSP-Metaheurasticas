class Algorithm:
    def __init__(self, termination, problem, verbose = False):
        self.termination = termination # critério de parada a ser utilizado pelo algorítimo
        self.problem = problem # problema a ser resolvido pelo algorítimo
        self.verbose = verbose # se o algorítimo deve imprimir saída nesta execução
        self.n_iteration = 0 # número atual de iterações
        self.start_time = None # o momento em que o algorítimo foi inicializado pela primeira vez

    def run(self):
        self.initialize()
        while not self.termination.has_terminated():
            self.advance()
            self.termination.update_progress(self)
        self.finalize()

    def initialize(self):
        pass

    def advance(self):
        pass

    def finalize(self):
        pass