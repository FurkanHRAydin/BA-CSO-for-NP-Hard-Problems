
import random


class Cat:
    def __init__(self, nurses):
        self.nurses = nurses
        self.velocity = [[random.uniform(-1, 1) for _ in nurse.schedule] for nurse in
                         nurses]  # Zufällige Startgeschwindigkeiten
        self.fitness = float('inf')
