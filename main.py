from CS0 import CSO
from Nurse import Nurse
from Shift import Shift


def main():
    num_cats = 10
    num_nurses = 5
    num_days = 7
    shifts = [
        Shift(shift_type="Early", min_nurses=1, max_nurses=2, optimal_nurses=1, forbidden_successions=["Night"]),
        Shift(shift_type="Late", min_nurses=1, max_nurses=2, optimal_nurses=1, forbidden_successions=["Early"]),
        Shift(shift_type="Night", min_nurses=1, max_nurses=2, optimal_nurses=1, forbidden_successions=["Late", "Early"])
    ]

    nurses = [Nurse(name=f"Nurse{i}", skills=["Skill1"], contract="FullTime") for i in range(num_nurses)]

    smp = 10
    spc = True
    srd = 0.7
    c1 = 0.6
    velocity_limit = 0.2
    mr = 0.5

    cso = CSO(num_cats, num_nurses, num_days, shifts, smp, spc, srd, c1, velocity_limit, mr)
    iterations = 100
    cso.optimize(iterations, nurses, shifts)
    cso.report_best_global()
    cso.plot_fitness()


if __name__ == "__main__":
    main()