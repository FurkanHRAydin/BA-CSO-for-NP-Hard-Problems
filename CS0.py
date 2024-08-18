import matplotlib.pyplot as plt
import random
from Cat import Cat
from SeekinMode import SeekingMode
from TracingMode import TracingMode
from Fitness import Fitness
from Nurse import Nurse


class CSO:
    def __init__(self, num_cats, num_days, shifts, smp, spc, srd, c1, velocity_limit, mr):
        self.num_cats = num_cats
        self.num_days = num_days
        self.shifts = shifts

        benchmark_nurses = [
            {'name': 'Anna', 'availability': ['Früh', 'Spät', 'Nacht', 'None'], 'preferences': ['Früh'],
             'skills': ['Skill1']},
            {'name': 'Ben', 'availability': ['Früh', 'Spät', 'None'], 'preferences': ['Spät'], 'skills': ['Skill2']},
            {'name': 'Carla', 'availability': ['Früh', 'None', 'Nacht'], 'preferences': ['Nacht'],
             'skills': ['Skill3']},
            {'name': 'Dave', 'availability': ['Früh', 'Spät', 'Nacht'], 'preferences': ['Spät'],
             'skills': ['Skill1', 'Skill3']},
            {'name': 'Eva', 'availability': ['Früh', 'None', 'Nacht'], 'preferences': ['Nacht'], 'skills': ['Skill2']}
        ]

        self.cats = []
        for _ in range(num_cats):
            nurses = [Nurse(nurse['name'], num_days, nurse['availability'], nurse['preferences'], nurse['skills'])
                      for nurse in benchmark_nurses]
            self.cats.append(Cat(nurses))

        self.seeking_mode = SeekingMode(smp, spc, srd)  # Initialisierung des SeekingMode
        self.tracing_mode = TracingMode(c1, velocity_limit)  # Initialisierung des TracingMode
        self.mr = mr
        self.best_global_fitness = float('inf')
        self.best_global_position = [nurse.schedule[:] for nurse in self.cats[0].nurses]
        self.global_fitness_history = []
        self.iteration_best_fitness = []
        self.cat_fitness_history = []

    def run_iteration(self, iteration):
        best_fitness_in_iteration = float('inf')
        iteration_fitness = []

        for index, cat in enumerate(self.cats):
            if random.random() < self.mr:  # **SEEKING MODE** wird ausgewählt
                modified_positions = self.seeking_mode.create_and_modify_positions(cat.nurses)
                fitness_scores = [Fitness.calculate_fitness(pos, self.shifts, self.num_days) for pos in
                                  modified_positions]
                best_position = modified_positions[fitness_scores.index(min(fitness_scores))]
                cat.update_position(best_position)
            else:  # **TRACING MODE** wird ausgewählt
                best_position = self.best_global_position
                cat.velocity = self.tracing_mode.update_velocity(cat.nurses, best_position, cat.velocity)
                new_positions = self.tracing_mode.update_position(cat.nurses, cat.velocity)
                cat.update_position(new_positions)

            cat.fitness = Fitness.calculate_fitness(cat.nurses, self.shifts, self.num_days)
            iteration_fitness.append(cat.fitness)
            print(f"Iteration {iteration + 1}, Cat {index + 1} Fitness: {cat.fitness}")

            if cat.fitness < best_fitness_in_iteration:
                best_fitness_in_iteration = cat.fitness

            if cat.fitness < self.best_global_fitness:
                print(f"New Global Best Fitness found by Cat {index + 1}: {cat.fitness}")
                self.best_global_fitness = cat.fitness
                self.best_global_position = [nurse.schedule[:] for nurse in cat.nurses]

        self.iteration_best_fitness.append(best_fitness_in_iteration)
        self.global_fitness_history.append(self.best_global_fitness)
        self.cat_fitness_history.append(iteration_fitness)

        print(f"Best Fitness in Iteration {iteration + 1}: {best_fitness_in_iteration}")
        print(f"Global Best Fitness after Iteration {iteration + 1}: {self.best_global_fitness}\n")

    def optimize(self, iterations):
        for iteration in range(iterations):
            print(f"Start of Iteration {iteration + 1}")
            self.run_iteration(iteration)
            print(f"End of Iteration {iteration + 1}\n")

    def plot_fitness(self):
        # Plot für den globalen besten Fitnesswert und den besten Fitnesswert pro Iteration
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(self.global_fitness_history) + 1), self.global_fitness_history,
                 label='Best Global Fitness per Iteration', color='blue')
        plt.plot(range(1, len(self.iteration_best_fitness) + 1), self.iteration_best_fitness,
                 label='Best Fitness per Iteration', color='red')
        plt.xlabel('Iteration')
        plt.ylabel('Fitness')
        plt.title('Fitness Development Over Iterations')
        plt.legend()
        plt.grid(True)
        plt.xlim(1, len(self.global_fitness_history))
        plt.ylim(0, max(self.global_fitness_history) * 1.1)
        plt.show()

    def report_best_global(self):
        print(f"Best global fitness achieved: {self.best_global_fitness}")
        print(f"Best found schedule:")

        for i, nurse_schedule in enumerate(self.best_global_position):
            nurse_name = ['Anna', 'Ben', 'Carla', 'Dave', 'Eva'][i]
            print(f"{nurse_name}: {nurse_schedule}")

        # Zusätzliche Ausgabe zur Überprüfung
        print("\nDetailed Schedule:")
        for nurse_schedule in self.best_global_position:
            print(nurse_schedule)
