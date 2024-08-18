import random

shift_to_num = {'None': 0, 'Früh': 1, 'Spät': 2, 'Nacht': 3}
num_to_shift = {v: k for k, v in shift_to_num.items()}


class TracingMode:
    def __init__(self, c1, velocity_limit):
        self.c1 = c1
        self.velocity_limit = velocity_limit

    def update_velocity(self, current_nurses, best_position, velocity):
        """
        Aktualisiert die Geschwindigkeit der Krankenschwestern in der aktuellen Position,
        basierend auf der besten gefundenen Position.
        """
        new_velocity = velocity.copy()
        for i in range(len(current_nurses)):
            for day in range(len(current_nurses[i].schedule)):
                r1 = random.random()
                change = r1 * self.c1 * (
                        shift_to_num[best_position[i][day]] - shift_to_num[current_nurses[i].schedule[day]]
                )
                new_velocity[i][day] += change
                new_velocity[i][day] = max(min(new_velocity[i][day], self.velocity_limit), -self.velocity_limit)
        return new_velocity

    def update_position(self, current_nurses, velocity):
        """
        Aktualisiert die Positionen der Krankenschwestern basierend auf der aktuellen Geschwindigkeit.
        """
        num_nurses = len(current_nurses)
        new_positions = []
        for i in range(num_nurses):
            new_schedule = current_nurses[i].schedule[:]
            for day in range(len(new_schedule)):
                shift_num = shift_to_num[new_schedule[day]] + int(velocity[i][day])
                shift_num = max(0, min(shift_num, 3))
                new_schedule[day] = num_to_shift[shift_num]
            new_positions.append(new_schedule)

        return new_positions
