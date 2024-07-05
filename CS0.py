import random
import matplotlib.pyplot as plt
from SeekinMode import SeekingMode
from TracingMode import TracingMode
from Cat import Cat
from Fitness import Fitness


class CSO:
    def __init__(self, num_cats, num_dimensions, smp, spc, srd, c1, velocity_limit, mr):
        self.num_cats = num_cats
        self.num_dimensions = num_dimensions
        self.cats = []
        for i in range(num_cats):
            self.cats.append(Cat(num_dimensions))
        self.seeking_mode = SeekingMode(smp, spc, srd)
        self.tracing_mode = TracingMode(c1, velocity_limit)
        self.mr = mr
        self.fitness_history = []
        self.best_global_fitness = float('inf')  # Beste globale Fitness initialisieren
        self.best_global_position = None  # Beste globale Position initialisieren

    def run_iteration(self):
        counter = 0
        for cat in self.cats:
            if random.random() < self.mr:
                # Cat is in seeking mode
                modified_positions = self.seeking_mode.create_and_modify_positions(cat.position)
                fitness_scores = []
                for pos in modified_positions:
                    fitness = Fitness.calculate_fitness(pos)
                    fitness_scores.append(fitness)
                selection_probabilities = self.seeking_mode.calculate_selection_probabilities(fitness_scores)
                selected_index = random.choices(range(len(modified_positions)), weights=selection_probabilities, k=1)[
                    0]  # Extrahiere den korrekten Index aus der Liste
                cat.position = modified_positions[selected_index]
            else:
                # Cat is in tracing mode
                best_cat = min(self.cats, key=Fitness.get_fitness)
                cat.velocity = self.tracing_mode.update_velocity(cat.position, best_cat.position, cat.velocity)
                cat.position = self.tracing_mode.update_position(cat.position, cat.velocity)

            # Evaluate fitness
            cat.fitness = Fitness.evaluate_fitness(cat)

            counter = counter + 1
            print(f"Cat {counter}: Position = {cat.position}, Fitness = {cat.fitness}")

        best_cat = min(self.cats, key=Fitness.get_fitness)
        if best_cat.fitness < self.best_global_fitness:
            self.best_global_fitness = best_cat.fitness
            self.best_global_position = best_cat.position[:]

        self.fitness_history.append(self.best_global_fitness)
        print(f"End of Iteration: Best Position = {best_cat.position}, Fitness = {best_cat.fitness}")

    def optimize(self, iterations):
        for iteration in range(iterations):
            print(f"Start of Iteration {iteration + 1}")
            self.run_iteration()
            print(f"End of Iteration {iteration + 1}")

    def plot_fitness(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.fitness_history, label='Best Fitness per Iteration')
        plt.xlabel('Iteration')
        plt.ylabel('Fitness')
        plt.title('Fitness Development Over Iterations')
        plt.legend()
        plt.grid(True)
        plt.xlim(0, len(self.fitness_history) - 1)  # Begrenze die x-Achse auf die Anzahl der Iterationen
        plt.ylim(0, max(self.fitness_history) * 1.1)  # Optionale Anpassung der y-Achse
        plt.show()

    def report_best_global(self):
        print(f"Best global fitness achieved: {self.best_global_fitness}")
        print(f"Position of best global fitness: {self.best_global_position}")
