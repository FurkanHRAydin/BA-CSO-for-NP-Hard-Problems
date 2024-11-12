from Shift import Shift
from Runner import initialize_cats, evaluate_cats, run_multiple_initializations, plot_best_fitness_per_iteration


def main():
    num_cats = 10  # Anzahl der Katzen
    num_days = 7  # Anzahl der Tage
    num_iterations = 1000  # Anzahl der Iterationen
    shifts = [
        Shift('Früh', 3),
        Shift('Spät', 3),
        Shift('Nacht', 2)
    ]

    # Führe die Initialisierungen durch und speichere die besten Fitnesswerte in eine Datei
    best_fitness, best_cat, best_fitness_per_iteration = run_multiple_initializations(
        num_cats, num_days, shifts, num_iterations, 'best_fitness_log.txt')

    # Gebe den besten gefundenen Schichtplan aus
    print(f"Best fitness found: {best_fitness}")
    for nurse in best_cat.nurses:
        print(f"{nurse.name}'s schedule: {nurse.schedule}")

    # Plotte die beste Fitness jeder Iteration
    plot_best_fitness_per_iteration(best_fitness_per_iteration)


if __name__ == "__main__":
    main()