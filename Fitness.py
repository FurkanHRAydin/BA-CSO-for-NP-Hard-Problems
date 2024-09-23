from Nurse import Nurse  # Stelle sicher, dass dies hinzugefügt wird


class Fitness:
    @staticmethod
    def calculate_fitness(nurses, shifts, num_days):
        under_staffing_penalty = 100
        preference_penalty = 10  # Strafpunkte für die Nichtberücksichtigung von Präferenzen
        availability_penalty = 50  # Strafpunkte für Zuweisungen außerhalb der Verfügbarkeit
        consecutive_shift_penalty = 30  # Strafpunkte für zu viele aufeinanderfolgende gleiche Schichten
        day_off_penalty = 30  # Strafpunkte für fehlende freie Tage
        total_penalty = 0

        for day in range(num_days):
            for shift in shifts:
                shift.clear_nurses()

            # Überprüfe, ob `nurses` eine Liste von `Nurse`-Objekten oder Schichtplänen ist
            if isinstance(nurses[0], Nurse):  # Überprüfe, ob es sich um ein Objekt der Klasse Nurse handelt
                nurse_assignment = {nurse.name: 0 for nurse in nurses}
            else:
                nurse_assignment = {f'Nurse{i}': 0 for i in range(len(nurses))}

            for i, nurse in enumerate(nurses):
                if isinstance(nurse,
                              Nurse):  # Nur wenn `nurse` ein Nurse-Objekt ist, rufe die Methode `get_shift` auf
                    shift_name = nurse.get_shift(day)
                    prev_shift = nurse.get_shift(day - 1) if day > 0 else None
                else:
                    shift_name = nurse[day]  # Falls `nurse` eine Liste ist, arbeite mit den Schichtplänen
                    prev_shift = nurse[day - 1] if day > 0 else None

                # Überprüfen, ob die Schicht innerhalb der Verfügbarkeit ist
                if shift_name != 'None' and isinstance(nurse, Nurse) and shift_name not in nurse.availability:
                    total_penalty += availability_penalty

                # Strafe für zu viele aufeinanderfolgende gleiche Schichten
                if prev_shift == shift_name and shift_name != 'None':
                    total_penalty += consecutive_shift_penalty

                if shift_name != 'None':
                    for shift in shifts:
                        if shift.name == shift_name:
                            # Verwende die `assign_shift` Methode, um die Schicht zuzuweisen
                            if isinstance(nurse, Nurse):
                                nurse.assign_shift(day, shift_name, shifts)
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

            for shift in shifts:
                if shift.is_understaffed():
                    # Hole die verfügbaren Krankenschwestern, die keine Schicht an diesem Tag haben
                    available_nurses = [nurse for nurse in nurses if
                                        isinstance(nurse, Nurse) and nurse.get_shift(day) == 'None']

                    # Fülle die Schicht auf, indem du die verfügbaren Krankenschwestern zuweist
                    shift.fill_shift(available_nurses, day, shifts)



        # Überprüfen, ob jede Krankenschwester mindestens einen freien Tag hat
        for nurse in nurses:
            if isinstance(nurse, Nurse) and 'None' not in nurse.schedule:
                total_penalty += day_off_penalty  # Strafe, wenn kein freier Tag vorhanden ist

        return total_penalty