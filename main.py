import CS0


def main():
    num_cats = 10
    num_dimensions = 3
    iterations = 100
    cso = CS0.CSO(num_cats, num_dimensions, smp=5, spc=True, srd=0.1, c1=0.2, velocity_limit=0.3, mr=0.5)
    cso.optimize(iterations)
    cso.report_best_global()
    cso.plot_fitness()


if __name__ == "__main__":
    main()
