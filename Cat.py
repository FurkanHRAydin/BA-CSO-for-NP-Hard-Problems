import random


class Cat:
    def __init__(self, num_dimensions):
        self.position = []
        self.velocity = []
        for i in range(num_dimensions):
            self.position.append(random.uniform(-10, 10))
            self.velocity.append(0.0)
        self.fitness = float('inf')
