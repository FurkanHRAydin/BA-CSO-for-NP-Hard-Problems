import random


class SeekingMode:
    def __init__(self, smp, spc, srd):
        self.smp = smp
        self.spc = spc
        self.srd = srd

    def create_and_modify_positions(self, current_schedule):
        copies = []
        num_copies = self.smp if self.spc else self.smp - 1
        for _ in range(num_copies):
            copies.append([
                [{shift_type: shift.copy() for shift_type, shift in day.items()} for day in nurse_schedule]
                for nurse_schedule in current_schedule
            ])

        if self.spc:
            copies.append([
                [{shift_type: shift.copy() for shift_type, shift in day.items()} for day in nurse_schedule]
                for nurse_schedule in current_schedule
            ])

        modified_copies = []
        for copy in copies:
            modified_copy = []
            for nurse_schedule in copy:
                modified_nurse_schedule = []
                for day in nurse_schedule:
                    modified_day = {}
                    for shift_type, shift in day.items():
                        modified_shift = shift.copy()
                        if random.random() < self.srd:
                            modified_shift['assigned'] = 1 - shift['assigned']  # Schichtzuweisung ändern
                        modified_day[shift_type] = modified_shift
                    modified_nurse_schedule.append(modified_day)
                modified_copy.append(modified_nurse_schedule)
            modified_copies.append(modified_copy)

        return modified_copies

    @staticmethod
    def calculate_selection_probabilities(fitness_scores):
        max_fitness = max(fitness_scores)
        min_fitness = min(fitness_scores)
        probabilities = []
        if max_fitness == min_fitness:
            for _ in fitness_scores:
                probabilities.append(1.0)
        else:
            for fitness in fitness_scores:
                probability = (abs(fitness - max_fitness) / (max_fitness - min_fitness))
                probabilities.append(probability)
        return probabilities

    @staticmethod
    def choose_new_position(modified_copies, selection_probabilities):
        chosen_index = random.choices(range(len(modified_copies)), weights=selection_probabilities, k=1)[0]
        return modified_copies[chosen_index]
