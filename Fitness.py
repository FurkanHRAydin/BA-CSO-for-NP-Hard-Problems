class Fitness:
    @staticmethod
    def calculate_fitness(schedule, nurses, shifts):
        hard_constraint_violations = 0
        soft_constraint_violations = 0

        # H1. Single assignment per day
        for nurse_schedule in schedule:
            for day in nurse_schedule:
                if sum(shift['assigned'] for shift in day.values()) > 1:
                    hard_constraint_violations += 5000

        # H2. Under-staffing
        for day in range(len(schedule[0])):
            for shift in shifts:
                assigned_nurses = sum(nurse_schedule[day][shift.shift_type]['assigned'] for nurse_schedule in schedule)
                if assigned_nurses < shift.min_nurses:
                    hard_constraint_violations += 500
                elif assigned_nurses > shift.max_nurses:
                    hard_constraint_violations += 500

        # H3. Shift type successions (for simplicity, example implementation)
        for nurse_schedule in schedule:
            for day in range(len(nurse_schedule) - 1):
                for shift in shifts:
                    if nurse_schedule[day][shift.shift_type]['assigned'] and any(
                            nurse_schedule[day + 1][succession]['assigned'] for succession in
                            shift.forbidden_successions):
                        hard_constraint_violations += 1000

        # Additional soft constraints can be added here...

        return hard_constraint_violations + soft_constraint_violations

    @staticmethod
    def evaluate_fitness(cat, nurses, shifts):
        cat.fitness = Fitness.calculate_fitness(cat.schedule, nurses, shifts)

    @staticmethod
    def get_fitness(cat):
        return cat.fitness
