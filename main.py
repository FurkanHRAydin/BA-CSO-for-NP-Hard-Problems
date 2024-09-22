from Shift import Shift
from Runner import random_search, plot_fitness


def main():
    num_cats = 10  # Anzahl der Katzen (dieser Wert wird hier nicht wirklich genutzt)
    num_days = 7  # Anzahl der Tage
    shifts = [
        Shift('Früh', 1),
        Shift('Spät', 1),
        Shift('Nacht', 1)
    ]

    # Führe eine zufällige Suche durch
    best_fitness, best_schedule, fitness_history = random_search(num_days, shifts, num_trials=1000)

    # Gebe das beste gefundene Ergebnis aus
    print(f"Best fitness found by random search: {best_fitness}")
    for i, nurse_schedule in enumerate(best_schedule):
        nurse_name = ['Anna', 'Ben', 'Carla', 'Dave', 'Eva', 'Frank'][i]
        print(f"{nurse_name}: {nurse_schedule}")

    plot_fitness(fitness_history)


if __name__ == "__main__":
    main()
