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

    def run_iteration(self):
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
            self.fitness_history.append(min(cat.fitness for cat in self.cats))

    def optimize(self, iterations):
        for iteration in range(iterations):
            self.run_iteration()
            # Print best cat's position and fitness after each iteration
            best_cat = min(self.cats, key=Fitness.get_fitness)
            print(f"Iteration {iteration + 1}: Best Position = {best_cat.position}, Fitness = {best_cat.fitness}")

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
