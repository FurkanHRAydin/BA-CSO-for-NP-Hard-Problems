import random


class SeekingMode:
    def __init__(self, smp, spc, srd):
        self.smp = smp
        self.spc = spc
        self.srd = srd

    @staticmethod
    def calculate_fitness(position):
        total = 0
        for coord in position:
            total += coord ** 2
        return total

    def create_and_modify_positions(self, current_position):
        copies = []
        num_copies = self.smp if self.spc else self.smp - 1
        for i in range(num_copies):
            copies.append(current_position[:])  # Erstellen einer Kopie der aktuellen Position

        if self.spc:
            copies.append(current_position[:])  # Hinzufügen der aktuellen Position, wenn spc wahr ist

        modified_copies = []
        for i in range(len(copies)):
            copy = copies[i]
            modified_copy = []
            for j in range(len(copy)):
                coord = copy[j]
                modified_coord = coord * (1 + random.uniform(-self.srd, self.srd))
                modified_copy.append(modified_coord)
            modified_copies.append(modified_copy)

        return modified_copies

    @staticmethod
    def calculate_selection_probabilities(fitness_scores):
        max_fitness = max(fitness_scores)
        min_fitness = min(fitness_scores)
        probabilities = []
        if max_fitness == min_fitness:
            for i in range(len(fitness_scores)):
                probabilities.append(1.0)
        else:
            for i in range(len(fitness_scores)):
                fitness = fitness_scores[i]
                probability = (abs(fitness - max_fitness) / (max_fitness - min_fitness))
                probabilities.append(probability)
        return probabilities

    @staticmethod
    def choose_new_position(modified_copies, selection_probabilities):
        chosen_index = random.choices(range(len(modified_copies)), weights=selection_probabilities, k=1)[0]
        return modified_copies[chosen_index]

