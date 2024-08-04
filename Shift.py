class Shift:
    def __init__(self, shift_type, min_nurses, max_nurses, optimal_nurses, forbidden_successions):
        self.shift_type = shift_type
        self.min_nurses = min_nurses
        self.max_nurses = max_nurses
        self.optimal_nurses = optimal_nurses  # Added optimal_nurses attribute
        self.forbidden_successions = forbidden_successions