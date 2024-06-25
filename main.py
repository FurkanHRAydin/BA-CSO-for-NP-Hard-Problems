import random


class Cat:
    def __init__(self, num_dimensions):
        # Zufällige Anfangsposition und anfängliche Geschwindigkeit von null
        self.position = [random.uniform(-10, 10) for _ in range(num_dimensions)]
        self.velocity = [0.0 for _ in range(num_dimensions)]

    def update_position(self):
        # Aktualisiere die Position der Katze basierend auf der Geschwindigkeit
        self.position = [self.position[i] + self.velocity[i] for i in range(len(self.position))]


def calculate_fitness(position):
    # Berechne die Fitness als die Summe der Quadrate der Positionskoordinaten
    return sum(x ** 2 for x in position)


def seeking_mode(cat, smp, srd):
    best_position = cat.position[:]
    best_fitness = calculate_fitness(cat.position)

    # Erzeuge mehrere Kandidaten um die aktuelle Position und wähle den besten aus
    for _ in range(smp):
        candidate_position = [p + random.uniform(-srd, srd) for p in cat.position]
        candidate_fitness = calculate_fitness(candidate_position)
        if candidate_fitness < best_fitness:
            best_fitness = candidate_fitness
            best_position = candidate_position[:]

    cat.position = best_position


def tracing_mode(cat, best_position, c1):
    # Passe die Geschwindigkeit an, um der besten bekannten Position zu folgen
    for i in range(len(cat.position)):
        r1 = random.random()
        cat.velocity[i] += c1 * r1 * (best_position[i] - cat.position[i])


def run_cso(num_cats, num_dimensions, iterations, smp, srd, c1):
    # Erstelle einen Schwarm von Katzen
    cats = [Cat(num_dimensions) for _ in range(num_cats)]
    best_cat = min(cats, key=lambda x: calculate_fitness(x.position))

    # Ausführen der Simulation für eine gegebene Anzahl von Iterationen
    for iteration in range(iterations):
        for cat in cats:
            if random.random() < 0.5:
                seeking_mode(cat, smp, srd)
            else:
                tracing_mode(cat, best_cat.position, c1)
            cat.update_position()
            # Finde neue beste Katze, wenn möglich
            if calculate_fitness(cat.position) < calculate_fitness(best_cat.position):
                best_cat = cat

        # Ausgabe der besten Katze und deren Fitnesswert nach jeder Iteration
        best_fitness = calculate_fitness(best_cat.position)
        formatted_position = [round(x, 2) for x in best_cat.position]
        print(f"Iteration {iteration + 1}: Beste Position = {formatted_position}, Fitness = {round(best_fitness, 2)}")

    return best_cat.position


def main():
    num_cats = 10
    num_dimensions = 5
    iterations = 100
    smp = 5  # Anzahl der Suchversuche im Seeking Mode
    srd = 1.0  # Suchradius für den Seeking Mode
    c1 = 2.0  # Beschleunigungsfaktor für den TracingMode

    best_position = run_cso(num_cats, num_dimensions, iterations, smp, srd, c1)
    formatted_best_position = [round(x, 2) for x in best_position]
    print("Endgültig beste gefundene Position:", formatted_best_position)


if __name__ == "__main__":
    main()
