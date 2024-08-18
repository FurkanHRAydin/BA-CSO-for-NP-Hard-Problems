class Nurse:
    def __init__(self, name, num_days, availability, preferences, skills):
        self.name = name
        self.schedule = ['None'] * num_days  # Initial leerer Schichtplan für jeden Tag
        self.availability = availability  # Verfügbare Schichten für jeden Tag
        self.preferences = preferences  # Bevorzugte Schichten
        self.skills = skills  # Fähigkeiten der Krankenschwester

    def assign_shift(self, day, shift):
        """
        Zuweisen einer Schicht an einem bestimmten Tag.
        """
        self.schedule[day] = shift

    def get_shift(self, day):
        """
        Gibt die zugewiesene Schicht für einen bestimmten Tag zurück.
        """
        return self.schedule[day]
