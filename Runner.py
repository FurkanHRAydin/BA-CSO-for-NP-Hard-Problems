import random
import matplotlib.pyplot as plt
from Nurse import Nurse
from Fitness import Fitness


def random_search(num_days, shifts, num_trials):
    best_fitness = float('inf')
    best_schedule = None
    fitness_history = []
    best_schedules = []

    benchmark_nurses = [
        {'name': 'Anna', 'availability': ['Früh', 'Spät', 'Nacht'], 'preferences': ['Früh', 'Spät']},
        {'name': 'Ben', 'availability': ['Früh', 'Spät'], 'preferences': ['Spät']},
        {'name': 'Carla', 'availability': ['Früh', 'Nacht'], 'preferences': ['Nacht']},
        {'name': 'Dave', 'availability': ['Früh', 'Spät', 'Nacht'], 'preferences': ['Spät']},
        {'name': 'Eva', 'availability': ['Früh', 'Nacht'], 'preferences': ['Nacht']},
        {'name': 'Frank', 'availability': ['Früh', 'Spät', 'Nacht'], 'preferences': ['Früh']}
    ]

    for trial in range(num_trials):
        # Erzeuge einen zufälligen Schichtplan für jede Krankenschwester
        nurses = [Nurse(nurse['name'], num_days, nurse['availability'], nurse['preferences'])
                  for nurse in benchmark_nurses]

        for nurse in nurses:
            for day in range(num_days):
                nurse.schedule[day] = random.choice(['Früh', 'Spät', 'Nacht', 'None'])

        # Berechne die Fitness des zufälligen Schichtplans
        fitness = Fitness.calculate_fitness(nurses, shifts, num_days)
        fitness_history.append(fitness)

        # Speichere das beste Ergebnis dieser Iteration
        best_schedules.append((fitness, [nurse.schedule[:] for nurse in nurses]))

        # Überprüfe, ob dieser Schichtplan besser ist als der bisher beste gefundene
        if fitness < best_fitness:
            best_fitness = fitness
            best_schedule = [nurse.schedule[:] for nurse in nurses]

        print({trial}, fitness)

    return best_fitness, best_schedule, fitness_history


def plot_fitness(fitness_history, title='Fitness Development Over Random Trials'):
    plt.figure(figsize=(10, 5))
    plt.plot(fitness_history, label='Fitness per Trial', color='blue')
    plt.xlabel('Trial')
    plt.ylabel('Fitness')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()
