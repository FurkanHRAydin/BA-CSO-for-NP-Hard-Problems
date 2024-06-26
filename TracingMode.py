import random


class TracingMode:
    def __init__(self, c1, velocity_limit):
        self.c1 = c1
        self.velocity_limit = velocity_limit

    def update_velocity(self, current_position, best_position, velocity):
        num_dimensions = len(current_position)
        for d in range(num_dimensions):
            r1 = random.random()
            velocity[d] += r1 * self.c1 * (best_position[d] - current_position[d])
            if velocity[d] > self.velocity_limit:
                velocity[d] = self.velocity_limit
            elif velocity[d] < -self.velocity_limit:
                velocity[d] = -self.velocity_limit
        return velocity

    @staticmethod
    def update_position(position, velocity):
        # Aktualisiere die Position basierend auf der Geschwindigkeit
        num_dimensions = len(position)
        for d in range(num_dimensions):
            position[d] += velocity[d]
        return position

