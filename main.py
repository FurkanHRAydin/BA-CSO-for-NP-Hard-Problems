from CS0 import CSO
from Shift import Shift


def main():
    num_cats = 10
    num_days = 7
    shifts = [
        Shift('Früh', 2, required_skill='Skill1'),
        Shift('Spät', 2, required_skill='Skill2'),
        Shift('Nacht', 1, required_skill='Skill3')
    ]
    iterations = 1000

    smp = 5
    spc = True
    srd = 0.3
    c1 = 0.5
    velocity_limit = 0.3
    mr = 0.7

    cso = CSO(num_cats, num_days, shifts, smp, spc, srd, c1, velocity_limit, mr)
    cso.optimize(iterations)
    cso.report_best_global()
    cso.plot_fitness()


if __name__ == "__main__":
    main()
