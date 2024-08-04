from Fitness import Fitness


class Cat:
    def __init__(self, num_nurses, num_days, shifts):
        self.schedule = [
            [{shift.shift_type: {'assigned': 0} for shift in shifts} for _ in range(num_days)]
            for _ in range(num_nurses)
        ]
        # Initialize the schedule as a list of lists of dictionaries
        self.velocity = [
            [{shift.shift_type: {'assigned': 0} for shift in shifts} for _ in range(num_days)]
            for _ in range(num_nurses)
        ]
        # Initialize the velocity as a list of lists of dictionaries
        self.fitness = float('inf')

    def evaluate(self, nurses, shifts):
        self.fitness = Fitness.calculate_fitness(self.schedule, nurses, shifts)
