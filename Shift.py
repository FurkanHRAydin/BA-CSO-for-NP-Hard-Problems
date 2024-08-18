class Shift:
    def __init__(self, name, min_required, required_skill=None):
        self.name = name
        self.min_required = min_required  # Minimale Anforderung an Krankenschwestern
        self.assigned_nurses = []
        self.required_skill = required_skill  # Neuer Parameter für erforderliche Fähigkeiten

    def add_nurse(self, nurse):
        """
        Fügt einer Schicht eine Krankenschwester hinzu.
        """
        self.assigned_nurses.append(nurse)

    def is_understaffed(self):
        """
        Überprüft, ob die Schicht unterbesetzt ist.
        """
        return len(self.assigned_nurses) < self.min_required

    def clear_nurses(self):
        """
        Löscht die Liste der zugewiesenen Krankenschwestern für einen neuen Tag.
        """
        self.assigned_nurses = []
