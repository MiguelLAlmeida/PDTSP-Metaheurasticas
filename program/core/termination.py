class Termination():
    def __init__(self):
        self.force_termination = False # o algorítimo pode ser forçado a terminar definindo este atributo como verdadeiro
        self.percentage = 0.0 # o valor que indica qual porcentagem já foi concluída

    def update_progress(self, algorithim):
        if self.force_termination:
            self.percentage = 1.0
        else:
            self.percentage = self.compute_progress(algorithim)
            assert self.percentage >= 0.0, 'Invalid progress was set by the TerminationCriterion'

        return self.percentage
    
    def has_terminated(self):
        return self.percentage >= 1.0
    
    def terminate(self):
        self.force_termination = True

    def compute_progress(self, algorithim):
        pass