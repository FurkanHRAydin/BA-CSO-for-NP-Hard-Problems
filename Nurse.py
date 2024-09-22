
import random
class Nurse:
    def __init__(self, name, num_days, availability, preferences):
        self.name = name
        self.schedule = ['None'] * num_days  # Initialisiere den Zeitplan mit 'None' für jeden Tag
        self.availability = availability
        self.preferences = preferences

    def assign_shift(self, day, shift_name, shifts):
        """
        Weist einer Krankenschwester eine Schicht an einem bestimmten Tag zu,
        falls sie noch keiner Schicht an diesem Tag zugewiesen wurde.
        Falls sie bereits zugewiesen wurde, versuche, einen Konflikt zu lösen.
        """
        if self.schedule[day] == 'None':
            self.schedule[day] = shift_name
        else:
            # Konfliktlösung: Zuweisung der ursprünglichen Schicht beibehalten oder ersetzen
            self.resolve_conflict(day, shift_name, shifts)

    def resolve_conflict(self, day, new_shift_name, shifts):
        """
        Konfliktlösung, wenn bereits eine Schicht zugewiesen wurde.
        Hier kannst du verschiedene Strategien anwenden, z.B. Präferenzbasiert entscheiden.
        """
        current_shift = self.schedule[day]

        # 1. Behalte die aktuelle Zuweisung bei, wenn sie bevorzugt ist.
        if current_shift in self.preferences:
            pass  # Behalte die aktuelle Zuweisung bei

        # 2. Ersetze die aktuelle Zuweisung durch die neue Schicht, wenn diese bevorzugt wird.
        elif new_shift_name in self.preferences:
            self.schedule[day] = new_shift_name

        # 3. Wenn keine der Schichten bevorzugt wird, wähle die Schicht, die in der Verfügbarkeit ist.
        elif new_shift_name in self.availability and current_shift not in self.availability:
            self.schedule[day] = new_shift_name

        # 4. Falls sowohl die aktuelle Schicht als auch die neue Schicht verfügbar sind,
        # entscheide basierend auf der geringeren aktuellen Belegung.
        elif new_shift_name in self.availability and current_shift in self.availability:
            current_shift_obj = next(shift for shift in shifts if shift.name == current_shift)
            new_shift_obj = next(shift for shift in shifts if shift.name == new_shift_name)

            # Wähle die Schicht mit der geringeren aktuellen Belegung
            if current_shift_obj.get_current_nurse_count() > new_shift_obj.get_current_nurse_count():
                self.schedule[day] = new_shift_name

        # 5. Wenn keine Verfügbarkeits- oder Präferenzübereinstimmung besteht, behalte die aktuelle Schicht bei.
        else:
            pass  # Behalte die aktuelle Zuweisung bei, da sie vielleicht trotzdem besser passt.

    def get_shift(self, day):
        """
        Gibt die zugewiesene Schicht für einen bestimmten Tag zurück.
        """
        return self.schedule[day]
