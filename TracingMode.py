import random


class TracingMode:
    def __init__(self, c1, velocity_limit):
        self.c1 = c1  # Konstante zur Steuerung der Trägheit
        self.velocity_limit = velocity_limit  # Begrenzung der Geschwindigkeit

    def update_velocity(self, current_schedule, best_schedule, velocity):
        num_days = len(current_schedule[0])  # Anzahl der Tage
        for nurse in range(len(current_schedule)):
            for day in range(num_days):
                for shift_type, shift in current_schedule[nurse][day].items():
                    r1 = random.random()
                    velocity[nurse][day][shift_type]['assigned'] += r1 * self.c1 * (
                            best_schedule[nurse][day][shift_type]['assigned'] -
                            current_schedule[nurse][day][shift_type]['assigned']
                    )
                    # Begrenzung der Geschwindigkeit
                    if velocity[nurse][day][shift_type]['assigned'] > self.velocity_limit:
                        velocity[nurse][day][shift_type]['assigned'] = self.velocity_limit
                    elif velocity[nurse][day][shift_type]['assigned'] < -self.velocity_limit:
                        velocity[nurse][day][shift_type]['assigned'] = -self.velocity_limit
        return velocity

    @staticmethod
    def update_position(schedule, velocity):
        # Aktualisiere die Position basierend auf der Geschwindigkeit
        num_days = len(schedule[0])
        for nurse in range(len(schedule)):
            for day in range(num_days):
                for shift_type, shift in schedule[nurse][day].items():
                    schedule[nurse][day][shift_type]['assigned'] += velocity[nurse][day][shift_type]['assigned']
                    schedule[nurse][day][shift_type]['assigned'] = 1 if schedule[nurse][day][shift_type][
                                                                            'assigned'] > 0 else 0  # Sicherstellen, dass Schichtzuweisung binär bleibt (0 oder 1)
        return schedule
