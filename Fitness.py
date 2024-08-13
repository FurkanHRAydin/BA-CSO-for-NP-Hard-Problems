from Nurse import Nurse  # Stelle sicher, dass dies hinzugefügt wird


class Fitness:
    @staticmethod
    def calculate_fitness(nurses, shifts, num_days):
        under_staffing_penalty = 100
        single_assignment_penalty = 50
        preference_penalty = 20  # Strafpunkte für die Nichtberücksichtigung von Präferenzen
        availability_penalty = 50  # Strafpunkte für Zuweisungen außerhalb der Verfügbarkeit
        total_penalty = 0

        for day in range(num_days):
            for shift in shifts:
                shift.clear_nurses()

            # Überprüfe, ob `nurses` eine Liste von `Nurse`-Objekten oder Schichtplänen ist
            if isinstance(nurses[0], Nurse):
                nurse_assignment = {nurse.name: 0 for nurse in nurses}
            else:
                nurse_assignment = {f'Nurse{i}': 0 for i in range(len(nurses))}

            for i, nurse in enumerate(nurses):
                if isinstance(nurse, Nurse):
                    shift_name = nurse.get_shift(day)
                else:
                    shift_name = nurse[day]  # Hier handelt es sich um einen Schichtplan, kein Nurse-Objekt

                # Überprüfen, ob die Schicht innerhalb der Verfügbarkeit ist
                if shift_name != 'None' and isinstance(nurse, Nurse) and shift_name not in nurse.availability:
                    total_penalty += availability_penalty

                if shift_name != 'None':
                    for shift in shifts:
                        if shift.name == shift_name:
                            # Aktualisiere das richtige Dictionary, abhängig davon, ob `nurse` ein Objekt oder eine Liste ist
                            if isinstance(nurse, Nurse):
                                shift.add_nurse(nurse)
                                nurse_assignment[nurse.name] += 1

                                # Überprüfen, ob die Schicht den Präferenzen entspricht
                                if shift_name not in nurse.preferences:
                                    total_penalty += preference_penalty
                            else:
                                shift.add_nurse(None)  # Wir fügen `None` hinzu, da wir kein `Nurse`-Objekt haben
                                nurse_assignment[f'Nurse{i}'] += 1

            for shift in shifts:
                if shift.is_understaffed():
                    total_penalty += under_staffing_penalty * (shift.min_required - len(shift.assigned_nurses))

            for nurse_name, assignment_count in nurse_assignment.items():
                if assignment_count > 1:
                    total_penalty += single_assignment_penalty * (assignment_count - 1)

        return total_penalty
