
class Shift:
    def __init__(self, name, min_required):
        self.name = name
        self.min_required = min_required  # Minimale Anforderung an Krankenschwestern
        self.assigned_nurses = []

    def add_nurse(self, nurse):
        """
        Fügt einer Schicht eine Krankenschwester hinzu.
        """
        self.assigned_nurses.append(nurse)

    def remove_nurse(self, nurse):
        """
        Entfernt eine Krankenschwester von der Schicht, falls sie zugewiesen ist.
        """
        if nurse in self.assigned_nurses:
            self.assigned_nurses.remove(nurse)

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

    def get_current_nurse_count(self):
        """
        Gibt die aktuelle Anzahl der Krankenschwestern zurück, die dieser Schicht zugewiesen sind.
        """
        return len(self.assigned_nurses)

    def fill_shift(self, available_nurses, day, shifts):
        """
        Füllt die Schicht mit verfügbaren Krankenschwestern auf, um die Mindestanforderungen zu erfüllen.
        """
        for nurse in available_nurses:
            if self.is_understaffed() and nurse.get_shift(day) == 'None':
                nurse.assign_shift(day, self.name, shifts)
                self.add_nurse(nurse)
