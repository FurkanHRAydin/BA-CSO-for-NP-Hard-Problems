import random
import matplotlib.pyplot as plt
from SeekinMode import SeekingMode
from TracingMode import TracingMode
from Cat import Cat
from Fitness import Fitness


class CSO:
    def __init__(self, num_cats, num_nurses, num_days, shifts, smp, spc, srd, c1, velocity_limit, mr):
        self.num_cats = num_cats
        self.num_nurses = num_nurses
        self.num_days = num_days
        self.shifts = shifts
        self.cats = [Cat(num_nurses, num_days, shifts) for _ in range(num_cats)]
        self.seeking_mode = SeekingMode(smp, spc, srd)
        self.tracing_mode = TracingMode(c1, velocity_limit)
        self.mr = mr
        self.global_fitness_history = []
        self.cat_fitness_history = []
        self.best_global_fitness = float('inf')
        self.best_global_position = None

    def run_iteration(self, nurses, shifts):
        for cat_index, cat in enumerate(self.cats):
            if random.random() < self.mr:
                # Cat is in seeking mode
                print(f"Cat {cat_index} is in seeking mode")
                modified_positions = self.seeking_mode.create_and_modify_positions(cat.schedule)
                fitness_scores = [Fitness.calculate_fitness(pos, nurses, shifts) for pos in modified_positions]
                selection_probabilities = self.seeking_mode.calculate_selection_probabilities(fitness_scores)
                selected_index = random.choices(range(len(modified_positions)), weights=selection_probabilities, k=1)[0]
                cat.schedule = modified_positions[selected_index]
            else:
                # Cat is in tracing mode
                print(f"Cat {cat_index} is in tracing mode")
                best_cat = min(self.cats, key=Fitness.get_fitness)
                cat.velocity = self.tracing_mode.update_velocity(cat.schedule, best_cat.schedule, cat.velocity)
                cat.schedule = self.tracing_mode.update_position(cat.schedule, cat.velocity)

            # Evaluate fitness
            previous_fitness = cat.fitness
            cat.evaluate(nurses, shifts)
            print(f"Cat {cat_index} fitness changed from {previous_fitness} to {cat.fitness}")

        best_cat = min(self.cats, key=Fitness.get_fitness)
        if best_cat.fitness < self.best_global_fitness:
            self.best_global_fitness = best_cat.fitness
            self.best_global_position = best_cat.schedule

        self.global_fitness_history.append(self.best_global_fitness)
        self.cat_fitness_history.append(best_cat.fitness)
        print(f"Best Position Fitness = {self.best_global_fitness}, Best Cat Fitness = {best_cat.fitness}")

    def optimize(self, iterations, nurses, shifts):
        for iteration in range(iterations):
            print(f"Start of Iteration {iteration + 1}")
            self.run_iteration(nurses, shifts)
            print(f"End of Iteration {iteration + 1}")

    def plot_fitness(self):
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(self.global_fitness_history) + 1), self.global_fitness_history, label='Best Global Fitness per Iteration', color='blue')
        plt.plot(range(1, len(self.cat_fitness_history) + 1), self.cat_fitness_history, label='Best Cat Fitness per Iteration', color='red')
        plt.xlabel('Iteration')
        plt.ylabel('Fitness')
        plt.title('Fitness Development Over Iterations')
        plt.legend()
        plt.grid(True)
        plt.xlim(1, len(self.global_fitness_history))  # Start at 1 instead of 0
        plt.ylim(0, max(self.global_fitness_history) * 1.1)
        plt.show()

    def report_best_global(self):
        print(f"Best global fitness achieved: {self.best_global_fitness}")
        print(f"Position of best global fitness: {self.best_global_position}")
        self.print_schedule(self.best_global_position)

    def print_schedule(self, schedule):
        for nurse_id, nurse_schedule in enumerate(schedule):
            print(f"Nurse {nurse_id + 1}:")
            for day, day_schedule in enumerate(nurse_schedule):
                shifts = ', '.join([shift for shift, details in day_schedule.items() if details['assigned'] == 1])
                print(f"  Day {day + 1}: {shifts}")
            print()