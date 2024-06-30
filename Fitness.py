class Fitness:

    @staticmethod
    def calculate_fitness(position):
        total = 0
        for coord in position:
            total += coord ** 2
        return total

    @staticmethod
    def evaluate_fitness(cat):
        total = 0
        for coord in cat.position:
            total += coord ** 2
        return total

    @staticmethod
    def get_fitness(cat):
        return cat.fitness
