import random
import numpy as np
import matplotlib.pyplot as plt
from Nurse import Nurse
from Fitness import Fitness
from Cat import Cat  # Deine Cat-Klasse


def initialize_cats(num_cats, num_days):
    """
    Diese Funktion initialisiert 'num_cats' Katzen mit zufälligen Schichtplänen.
    Sie bewertet jede Katze mithilfe der Fitnessfunktion.
    """
    benchmark_nurses = [
        {'name': 'Anna', 'preferences': ['Früh', 'Spät']},
        {'name': 'Ben', 'preferences': ['Spät']},
        {'name': 'Carla', 'preferences': ['Nacht']},
        {'name': 'Dave', 'preferences': ['Spät']},
        {'name': 'Eva', 'preferences': ['Nacht']},
        {'name': 'Frank', 'preferences': ['Früh']},
        {'name': 'Grace', 'preferences': ['Früh', 'Nacht']},
        {'name': 'Helen', 'preferences': ['Spät']},
        {'name': 'Ian', 'preferences': ['Früh']},
        {'name': 'John', 'preferences': ['Nacht', 'Spät']}
    ]

    cats = []  # Liste der Katzen
    for _ in range(num_cats):
        # Initialisiere Krankenschwestern für jede Katze
        nurses = [Nurse(nurse['name'], num_days, nurse['preferences'])
                  for nurse in benchmark_nurses]

        # Erzeuge einen zufälligen Schichtplan für jede Krankenschwester
        for nurse in nurses:
            for day in range(num_days):
                nurse.schedule[day] = random.choice(['Früh', 'Spät', 'Nacht', 'None'])

        # Füge die Katze zur Liste hinzu
        cats.append(Cat(nurses))

    return cats


def evaluate_cats(cats, shifts, num_days):
    """
    Bewertet jede Katze basierend auf ihrem Schichtplan mit der Fitnessfunktion.
    Gibt die beste Katze (mit dem niedrigsten Fitnesswert) und deren Schichtplan zurück.
    """
    best_fitness = float('inf')
    best_cat = None
    fitness_history = []

    for cat in cats:
        # Berechne die Fitness für jede Katze
        fitness = Fitness.calculate_fitness(cat.nurses, shifts, num_days)
        fitness_history.append(fitness)

        # Überprüfen, ob diese Katze die beste ist
        if fitness < best_fitness:
            best_fitness = fitness
            best_cat = cat

    return best_cat, best_fitness, fitness_history


def run_multiple_initializations(num_cats, num_days, shifts, num_iterations, fitness_log_filename):
    """
    Führt mehrere Initialisierungen durch und speichert die besten Fitnesswerte jeder Iteration.
    Gibt den besten gefundenen Schichtplan am Ende aus.
    Zusätzlich werden die besten Fitnesswerte in einer Datei gespeichert.
    """
    best_fitness_overall = float('inf')
    best_cat_overall = None
    best_fitness_per_iteration = []

    with open(fitness_log_filename, 'w') as file:
        for iteration in range(num_iterations):
            # Initialisiere Katzen
            cats = initialize_cats(num_cats, num_days)

            # Bewerte die Katzen und finde den besten Schichtplan
            best_cat, best_fitness, fitness_history = evaluate_cats(cats, shifts, num_days)

            # Schreibe nur den besten Fitnesswert dieser Iteration in die Datei
            file.write(f"Iteration {iteration + 1}: Best Fitness = {best_fitness}\n")

            # Speichere nur die beste Fitness dieser Iteration
            best_fitness_per_iteration.append(best_fitness)

            # Aktualisiere den besten globalen Schichtplan, falls eine Katze eine bessere Fitness hat
            if best_fitness < best_fitness_overall:
                best_fitness_overall = best_fitness
                best_cat_overall = best_cat

    return best_fitness_overall, best_cat_overall, best_fitness_per_iteration


import numpy as np
import matplotlib.pyplot as plt


def plot_best_fitness_per_iteration(best_fitness_per_iteration, step=20, use_moving_average=False, window_size=20):
    """
    Plottet die beste Fitness jeder Iteration:
    - Zeigt nur jeden `step`-ten Wert für Übersichtlichkeit an.
    - Optionale Glättung durch gleitenden Durchschnitt.

    Parameter:
    - best_fitness_per_iteration: Liste der Fitnesswerte pro Iteration
    - step: Schrittgröße für die Anzeige (z.B. 10 für jede 10. Iteration)
    - use_moving_average: Bool, ob ein gleitender Durchschnitt verwendet werden soll
    - window_size: Größe des Fensters für den gleitenden Durchschnitt
    """
    plt.figure(figsize=(10, 5))

    # Option 1: Plotten nur jeder `step`-ten Iteration und den letzten Wert
    reduced_iterations = list(range(0, len(best_fitness_per_iteration), step))
    reduced_fitness = [best_fitness_per_iteration[i] for i in reduced_iterations]

    # Sicherstellen, dass der letzte Punkt aufgenommen wird
    if reduced_iterations[-1] != len(best_fitness_per_iteration) - 1:
        reduced_iterations.append(len(best_fitness_per_iteration) - 1)
        reduced_fitness.append(best_fitness_per_iteration[-1])

    # Option 2: Glättung mit gleitendem Durchschnitt
    if use_moving_average:
        fitness_smoothed = np.convolve(best_fitness_per_iteration, np.ones(window_size) / window_size, mode='valid')
        plt.plot(fitness_smoothed, label='Ohne Optimierung (geglättet)', color='red')
    else:
        plt.plot(reduced_iterations, reduced_fitness, label='Ohne Optimierung', color='red', marker='o', markersize=2)

    plt.xlabel('Iteration')
    plt.ylabel('Fitness')

    # Anzeige nur alle 100 Iterationen auf der x-Achse
    plt.xticks(range(0, len(best_fitness_per_iteration) + 1, 100))

    plt.legend()
    plt.grid(True)
    plt.show()
