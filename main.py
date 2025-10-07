from matplotlib import pyplot as plt
from matplotlib.widgets import RadioButtons
import numpy as np

x_values = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, 2.5, 5, 7.5, 8.4])
y_values = np.array([0, 40, 80, 120, 145, 160, 165, 170, 175, 177, 170, 160]) #kN
y_values = y_values * 1000  #N


class Solver:
    def __init__(self):
        self.line = None
        self.modulo_young = None
        self.punti_deformazione = np.array([])
        self.punti_sforzo = np.array([])
        self.lato = 10
        self.diametro = 10
        self.sezione_iniziale = 50
        self.forma_provino = "quadrato"
        self.lunghezza_iniziale = 50

        plt.style.use('dark_background')

        self.fig, self.ax = plt.subplots(figsize=(16, 8))
        self.fig.set_facecolor("#1a1a1a")
        self.ax.set_facecolor("#1a1a1a")

        self.calculate_surface_area(self.forma_provino)
        self.update()

        self.ax_radio = plt.axes((0.02, 0.2, 0.07, 0.15), facecolor='#434b52')
        self.shape_button = RadioButtons(self.ax_radio, ('quadrato', 'cerchio'))

        self.shape_button.on_clicked(self.calculate_surface_area)

        plt.show()

    def update(self):
        self.ax.clear()
        self.convert_points()
        self.create_graph()
        self.fig.canvas.draw_idle()
        self.calculate_modulo_young()
        self.calculate_sforzo_snervamento()

    def calculate_surface_area(self, label):
        if label == "quadrato":
            self.sezione_iniziale = self.lato ** 2
        elif label == "cerchio":
            self.sezione_iniziale = self.diametro ** 2 * np.pi / 4
        self.update()

    def create_graph(self):
        self.line = self.ax.plot(self.punti_deformazione, self.punti_sforzo, "o-", color='#1989e2')

        self.ax.set_xlim(0, np.max(self.punti_deformazione) * 1.01)
        self.ax.set_ylim(0, np.max(self.punti_sforzo) * 1.01)

        self.ax.set_ylabel("Sforzo in N/mm²", color='#ffffff', size=15)
        self.ax.set_xlabel("Deformazione ε", color='#ffffff', size=15)

        self.ax.set_xticks(self.punti_deformazione)
        self.ax.set_yticks(self.punti_sforzo)

        self.ax.tick_params(axis="x", labelrotation=90, labelsize=8, color='#ffffff', labelcolor='#ffffff')
        self.ax.tick_params(axis="y", labelsize=8, color='#ffffff', labelcolor='#ffffff')

    def convert_points(self):
        self.punti_deformazione = x_values / self.lunghezza_iniziale
        self.punti_sforzo = y_values / self.sezione_iniziale

    def calculate_modulo_young(self):
        self.modulo_young = self.punti_sforzo[1] / self.punti_deformazione[1]

    def calculate_sforzo_snervamento(self):
        intercept = 0.002 * self.modulo_young
        x = np.linspace(0, np.max(self.punti_deformazione))
        y = x * self.modulo_young - intercept
        self.l_snervamento = self.ax.plot(x, y, color='#e21941')

    def find_intersection(self):
        x_points = self.punti_deformazione
        y_points = self.punti_sforzo
        # y = mx + q
        for i in range(len(x_points)):
            q = y_points[i] * (- y_points[i + 1] + x_points[i + 1]) / (x_points[i + 1] - y_points[i])




solver = Solver()
