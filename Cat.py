import random
class Cat:
    def __init__(self, nurses):
        self.nurses = nurses
        self.velocity = [[random.uniform(-1, 1) for _ in nurse.schedule] for nurse in nurses]  # Zufällige Startgeschwindigkeiten
        self.fitness = float('inf')

    def update_position(self, new_positions):
        """
        Aktualisiert die Position (Schichtplan) basierend auf neuen Positionsdaten.
        """
        for nurse, new_schedule in zip(self.nurses, new_positions):
            if isinstance(new_schedule, list):  # Sicherstellen, dass der neue Schichtplan eine Liste ist
                nurse.schedule = new_schedule
            else:
                print(f"Fehler: {nurse.name} hat keinen gültigen Schichtplan.")
                print(f"Erhaltener Schichtplan: {new_schedule}")
                nurse.schedule = ['None'] * len(nurse.schedule)  # Fallback-Lösung