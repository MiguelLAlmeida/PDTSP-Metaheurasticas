import copy

class Solution:
    def __init__(self, value, cost = 0.0):
        self.value = value
        self.cost = cost

    @property
    def size(self):
        return len(self.value)
    
    def copy(self):
        return copy.deepcopy(self)