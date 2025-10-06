from matplotlib import pyplot as plt
import numpy as np

x_values = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, 2.5, 5, 7.5, 8.4])
y_values = np.array([0, 40, 80, 120, 145, 160, 165, 170, 175, 177, 170, 160]) #kN
y_values = y_values * 1000  #N


class Solver:
    def __init__(self):
        self.modulo_young = None
        self.punti_deformazione = np.array([])
        self.punti_sforzo = np.array([])
        self.sezione_iniziale = None
        self.forma_provino = "quadrato"
        self.lunghezza_iniziale = 50

        self.calculate_surface_area()
        self.convert_points()
        self.create_graph()

        self.calculate_modulo_young()
        self.calculate_sforzo_snervamento()

        plt.show()

    def calculate_surface_area(self):
        if self.forma_provino == "quadrato":
            lato = 10
            self.sezione_iniziale = lato ** 2
        elif self.forma_provino == "cerchio":
            diametro = 10
            self.sezione_iniziale = diametro ** 2 * np.pi / 4


    def create_graph(self):
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.plot(self.punti_deformazione, self.punti_sforzo)

        plt.xlim([0, np.max(self.punti_deformazione) * 1.01])
        plt.ylim([0, np.max(self.punti_sforzo) * 1.1])

        ax.set_ylabel("Sforzo in N/mm²")
        ax.set_xlabel("Deformazione")

        ax.set_xticks(self.punti_deformazione)
        ax.set_yticks(self.punti_sforzo)

        ax.tick_params(axis="x", labelrotation=90, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)

    def convert_points(self):
        self.punti_deformazione = x_values / self.lunghezza_iniziale
        self.punti_sforzo = y_values / self.sezione_iniziale

    def calculate_modulo_young(self):
        self.modulo_young = self.punti_sforzo[1] / self.punti_deformazione[1]
        print(self.modulo_young)

    def calculate_sforzo_snervamento(self):
        pass


solver = Solver()
