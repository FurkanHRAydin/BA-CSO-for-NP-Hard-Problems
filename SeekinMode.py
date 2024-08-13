import random
from Nurse import Nurse


class SeekingMode:
    def __init__(self, smp, spc, srd):
        self.smp = smp
        self.spc = spc
        self.srd = srd

    def create_and_modify_positions(self, nurses):
        modified_positions = []
        for _ in range(self.smp):
            new_nurses = []
            for nurse in nurses:
                new_schedule = nurse.schedule[:]
                if random.random() < self.srd:
                    for i in range(len(new_schedule)):
                        new_schedule[i] = random.choice(['Früh', 'Spät', 'Nacht', 'None'])
                new_nurses.append(new_schedule)
            modified_positions.append(new_nurses)

        if self.spc:
            modified_positions.append([nurse.schedule[:] for nurse in nurses])

        # Debugging: Überprüfe, ob gültige Positionen erstellt wurden
        if not modified_positions:
            print("Fehler: Keine gültigen Positionen wurden erstellt.")

        return modified_positions

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
