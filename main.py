from CS0 import CSO
from Shift import Shift


def main():
    num_cats = 10  # Anzahl der "Katzen" im Schwarm
    num_days = 7  # Anzahl der Tage, für die ein Schichtplan erstellt wird
    shifts = [
        Shift('Früh', 1),  # Frühschicht mit mindestens 1 Krankenschwestern
        Shift('Spät', 1),  # Spätschicht mit mindestens 1 Krankenschwestern
        Shift('Nacht', 1)  # Nachtschicht mit mindestens 1 Krankenschwester
    ]
    iterations = 10000  # Anzahl der Iterationen für den CSO-Algorithmus

    smp = 5  # Anzahl der erzeugten neuen Lösungen im Seeking Mode
    spc = True  # Berücksichtigt die aktuelle Position im Seeking Mode
    srd = 0.5  # Bereich der Modifikation im Seeking Mode
    c1 = 0.5  # Gewichtung der besten Position im Tracing Mode
    velocity_limit = 0.3  # Begrenzung der Geschwindigkeit im Tracing Mode
    mr = 0.5  # Wechselwahrscheinlichkeit zwischen Seeking und Tracing Mode

    # Erstellen und Ausführen des CSO-Algorithmus
    cso = CSO(num_cats, num_days, shifts, smp, spc, srd, c1, velocity_limit, mr)
    cso.optimize(iterations)
    cso.export_best_cats('cso_data.txt')
    cso.report_best_global()
    cso.plot_fitness()



if __name__ == "__main__":
    main()
