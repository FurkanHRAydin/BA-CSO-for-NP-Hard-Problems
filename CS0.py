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
            {'name': 'Anna', 'availability': ['Früh', 'Spät', 'Nacht'], 'preferences': ['Früh', 'Spät']},
            {'name': 'Ben', 'availability': ['Früh', 'Spät'], 'preferences': ['Spät']},
            {'name': 'Carla', 'availability': ['Früh', 'Nacht'], 'preferences': ['Nacht']},
            {'name': 'Dave', 'availability': ['Früh', 'Spät', 'Nacht'], 'preferences': ['Spät']},
            {'name': 'Eva', 'availability': ['Früh', 'Nacht'], 'preferences': ['Nacht']},
            {'name': 'Frank', 'availability': ['Früh', 'Spät', 'Nacht'], 'preferences': ['Früh']}
        ]

        self.cats = []
        for _ in range(num_cats):
            nurses = [Nurse(nurse['name'], num_days, nurse['availability'], nurse['preferences'])
                      for nurse in benchmark_nurses]
            self.cats.append(Cat(nurses))

        self.seeking_mode = SeekingMode(smp, spc, srd)
        self.tracing_mode = TracingMode(c1, velocity_limit)
        self.mr = mr
        self.best_global_fitness = float('inf')
        self.best_global_position = [nurse.schedule[:] for nurse in self.cats[0].nurses]
        self.global_fitness_history = []
        self.iteration_best_fitness = []
        self.cat_fitness_history = []

        # Neue Listen, um Iterationsdaten zu speichern
        self.best_fitness_per_iteration = []
        self.best_cats_per_iteration = []

    def run_iteration(self, iteration):
        best_fitness_in_iteration = float('inf')
        iteration_fitness = []
        best_cats_in_iteration = []  # Liste der besten Katzen in der aktuellen Iteration

        for index, cat in enumerate(self.cats):
            if random.random() < self.mr:
                modified_positions = self.seeking_mode.create_and_modify_positions(cat.nurses)
                fitness_scores = [Fitness.calculate_fitness(pos, self.shifts, self.num_days) for pos in
                                  modified_positions]
                best_position = modified_positions[fitness_scores.index(min(fitness_scores))]
                cat.update_position(best_position)
            else:
                best_position = self.best_global_position
                cat.velocity = self.tracing_mode.update_velocity(cat.nurses, best_position, cat.velocity)
                new_positions = self.tracing_mode.update_position(cat.nurses, cat.velocity)
                cat.update_position(new_positions)

            cat.fitness = Fitness.calculate_fitness(cat.nurses, self.shifts, self.num_days)
            iteration_fitness.append(cat.fitness)

            print(f"Iteration {iteration + 1}, Cat {index + 1} Fitness: {cat.fitness}")

            if cat.fitness < best_fitness_in_iteration:
                best_fitness_in_iteration = cat.fitness
                best_cats_in_iteration = [index + 1]  # Speichere die Katze mit der besten Fitness
            elif cat.fitness == best_fitness_in_iteration:
                best_cats_in_iteration.append(index + 1)  # Füge Katze zur Liste der besten Katzen hinzu

            if cat.fitness < self.best_global_fitness:
                print(f"New Global Best Fitness found by Cat {index + 1}: {cat.fitness}")
                self.best_global_fitness = cat.fitness
                self.best_global_position = [nurse.schedule[:] for nurse in cat.nurses]

        self.iteration_best_fitness.append(best_fitness_in_iteration)
        self.global_fitness_history.append(self.best_global_fitness)
        self.cat_fitness_history.append(iteration_fitness)

        # Speichere die Ergebnisse der aktuellen Iteration
        self.best_fitness_per_iteration.append(best_fitness_in_iteration)
        self.best_cats_per_iteration.append(best_cats_in_iteration)

        print(f"Best Cats in Iteration {iteration + 1}: {best_cats_in_iteration}")
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
            nurse_name = ['Anna', 'Ben', 'Carla', 'Dave', 'Eva', 'Frank'][i]
            print(f"{nurse_name}: {nurse_schedule}")

        # Zusätzliche Ausgabe zur Überprüfung
        print("\nDetailed Schedule:")
        for nurse_schedule in self.best_global_position:
            print(nurse_schedule)

        # Ausgabe der besten Katzen in der letzten Iteration
        best_cats_last_iteration = [i + 1 for i, fitness in enumerate(self.cat_fitness_history[-1])
                                    if fitness == self.best_global_fitness]
        print(f"\nBest Cats in the Last Iteration: {best_cats_last_iteration}")

    def get_iteration_data(self):
        """
        Gibt die gespeicherten Iterationsdaten zurück, um sie später zu verwenden.
        """
        return self.best_fitness_per_iteration, self.best_cats_per_iteration

    def export_best_cats(self, filename):
        """
        Exportiert die besten Katzen jeder Iteration zusammen mit der globalen besten Fitness in eine .txt-Datei.
        """
        try:
            with open(filename, 'w') as file:
                for i, (best_cats, best_fitness, global_fitness) in enumerate(zip(self.best_cats_per_iteration, self.best_fitness_per_iteration, self.global_fitness_history), start=1):
                    file.write(f"Iteration {i} - Best Fitness: {best_fitness}\n")
                    file.write(f"Best Cats: {best_cats}\n")
                    file.write(f"Global Best Fitness: {global_fitness}\n")
                    file.write("\n")
            print(f"Beste Katzen und globale beste Fitness wurden erfolgreich in {filename} exportiert.")
        except Exception as e:
            print(f"Fehler beim Exportieren der besten Katzen: {e}")