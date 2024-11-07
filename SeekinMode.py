import random
from Nurse import Nurse


class SeekingMode:
    def __init__(self, smp, spc, srd, cdc):
        self.smp = smp
        self.spc = spc
        self.srd = srd  # Modifikationsrate für Diversität (Exploration)
        self.cdc = cdc  # Anzahl der Dimensionen (Tage oder Schichten), die verändert werden


    def create_and_modify_positions(self, nurses):
        """
        Erzeugt neue Positionen (Schichtpläne) durch Modifikation der aktuellen Positionen.
        """
        modified_positions = []
        for _ in range(self.smp if not self.spc else self.smp - 1):
            new_nurses = []
            for nurse in nurses:
                new_schedule = nurse.schedule[:]
                # Wähle zufällig CDC Schichten aus, die modifiziert werden sollen
                indices_to_modify = random.sample(range(len(new_schedule)), self.cdc)

                for i in indices_to_modify:
                    # SRD steuert die Wahrscheinlichkeit, ob eine Änderung vorgenommen wird
                    if random.random() < self.srd:
                        new_schedule[i] = random.choice(['Früh', 'Spät', 'Nacht', 'None'])

                new_nurses.append(new_schedule)
            modified_positions.append(new_nurses)

        if self.spc:  # Wenn spc=True, füge auch die aktuelle Position zur Modifikation hinzu
            modified_positions.append([nurse.schedule[:] for nurse in nurses])

        return modified_positions

    @staticmethod
    def calculate_selection_probabilities(fitness_scores):
        """
        Berechnet die Auswahlwahrscheinlichkeiten basierend auf den Fitnesswerten der Positionen.
        """
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
        """
        Wählt eine neue Position aus den modifizierten Kopien basierend auf den Auswahlwahrscheinlichkeiten.
        """
        chosen_index = random.choices(range(len(modified_copies)), weights=selection_probabilities, k=1)[0]
        return modified_copies[chosen_index]
