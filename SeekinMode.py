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


def main():
    current_position = [1, 2, 3]
    seeking_mode = SeekingMode(smp=5, spc=True, srd=0.1)
    modified_copies = seeking_mode.create_and_modify_positions(current_position)
    fitness_scores = []
    for i in range(len(modified_copies)):
        copy = modified_copies[i]
        fitness = seeking_mode.calculate_fitness(copy)
        fitness_scores.append(fitness)
    selection_probabilities = seeking_mode.calculate_selection_probabilities(fitness_scores)
    new_position = seeking_mode.choose_new_position(modified_copies, selection_probabilities)
    print("Neue Position der Katze:", new_position)

    # Iteriere durch den Optimierungsprozess
    for iteration in range(10):  # Anzahl der Iterationen, z.B. 10
        modified_copies = seeking_mode.create_and_modify_positions(current_position)
        fitness_scores = [seeking_mode.calculate_fitness(copy) for copy in modified_copies]
        selection_probabilities = seeking_mode.calculate_selection_probabilities(fitness_scores)
        current_position = seeking_mode.choose_new_position(modified_copies, selection_probabilities)

        # Ausgabe der aktuellen Position und des Fitnesswerts
        current_fitness = seeking_mode.calculate_fitness(current_position)
        print(f"Iteration {iteration + 1}: Position = {current_position}, Fitness = {current_fitness}")

        # Iteriere durch den Optimierungsprozess
    for iteration in range(10):  # Anzahl der Iterationen, z.B. 10
        modified_copies = seeking_mode.create_and_modify_positions(current_position)
        fitness_scores = [seeking_mode.calculate_fitness(copy) for copy in modified_copies]
        selection_probabilities = seeking_mode.calculate_selection_probabilities(fitness_scores)
        current_position = seeking_mode.choose_new_position(modified_copies, selection_probabilities)

        # Ausgabe der aktuellen Position und des Fitnesswerts
        current_fitness = seeking_mode.calculate_fitness(current_position)
        print(f"Iteration {iteration + 1}: Position = {current_position}, Fitness = {current_fitness}")


if __name__ == "__main__":
    main()
