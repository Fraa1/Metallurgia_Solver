from matplotlib import pyplot as plt
from matplotlib.widgets import RadioButtons
import numpy as np


x_values = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, 2.5, 5, 7.5, 8.4])
y_values = np.array([0, 40, 80, 120, 145, 160, 165, 170, 175, 177, 170, 160]) #kN
y_values = y_values * 1000  #N

class Solver:
    def __init__(self):
        self.coeff_strizione = None
        self.indice_elasticita = None
        self.punto_snervamento = None
        self.modulo_young = None
        self.sforzo_max = None
        self.punti_deformazione = np.array([])
        self.punti_sforzo = np.array([])
        self.lato = 10
        self.diametro = 10
        self.sezione_iniziale = 50
        self.sezione_finale = 85
        self.forma_provino = "Quadrata"
        self.lunghezza_iniziale = 50

        plt.style.use('dark_background')

        self.fig, self.ax = plt.subplots(figsize=(16, 8))
        self.fig.set_facecolor("#1a1a1a")
        self.ax.set_facecolor("#1a1a1a")

        # texts
        self.text_forma_sezione = self.fig.text(0.014, .95, 'Forma della sezione', size=10)
        self.text_modulo_young = self.fig.text(0.13, .9, f'Modulo di Young: ', size=15)
        self.text_sforzo_snervamento = self.fig.text(0.13, .94, f'Sforzo di snervamento: ', size=15)
        self.text_max_sforzo = self.fig.text(0.4, 0.9, 'Sforzo Max: ', size=15)
        self.text_indice_elasticita = self.fig.text(0.4, 0.94, 'Indice elasticità: ', size=15)
        self.text_coeff_strizione = self.fig.text(0.67, 0.9, 'Coefficiente Strizione: ', size=15)

        self.calculate_surface_area(self.forma_provino)

        self.ax_radio = plt.axes((0.02, 0.84, 0.07, 0.1), facecolor='#434b52')
        self.shape_button = RadioButtons(self.ax_radio, ('Quadrata', 'Circolare'))

        self.shape_button.on_clicked(self.calculate_surface_area)

        plt.show()

    def update(self):
        self.ax.clear()
        self.convert_points()
        self.fig.canvas.draw_idle()
        self.calculate_modulo_young()
        self.calculate_sforzo_snervamento()
        self.calculate_sforzo_max()
        self.calculate_indice_elasticita()
        if self.sezione_finale:
            self.calculate_coeff_strizione()
            self.text_coeff_strizione.set_text(f'Coefficiente Strizione: {self.coeff_strizione:.2f}%')
        self.create_graph()
        self.text_modulo_young.set_text(f'Modulo di Young: {self.modulo_young:.2f}')
        self.text_sforzo_snervamento.set_text(f'Sforzo di snervamento: {self.punto_snervamento:.2f}')
        self.text_max_sforzo.set_text(f'Sforzo Max: {self.sforzo_max:.2f}')
        self.text_indice_elasticita.set_text(f'Indice elasticità: {self.indice_elasticita:.2f}')

    def calculate_surface_area(self, label):
        if label == "Quadrata":
            self.sezione_iniziale = self.lato ** 2
        elif label == "Circolare":
            self.sezione_iniziale = self.diametro ** 2 * np.pi / 4
        self.update()

    def create_graph(self):
        line = self.ax.plot(self.punti_deformazione, self.punti_sforzo, "o-", color='#1989e2')

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
        intercept = - 0.002 * self.modulo_young
        x = np.linspace(0, np.max(self.punti_deformazione))
        y = x * self.modulo_young + intercept
        self.ax.plot(x, y, color='#e21941')
        self.punto_snervamento = self.find_intersection(self.modulo_young, intercept)

    def find_intersection(self, m_s, q_s):
        x_points = self.punti_deformazione
        y_points = self.punti_sforzo
        # y = mx + q
        for i in range(1, len(x_points) - 1):
            # calculate equation of every line
            q = (- y_points[i + 1] * x_points[i] + x_points[i + 1] * y_points[i]) / (x_points[i + 1] - x_points[i])
            m = (y_points[i + 1] - y_points[i]) / (x_points[i + 1] - x_points[i])

            # find all the intersections
            if m - m_s == 0:
                continue
            else:
                x = (q_s - q) / (m - m_s)
                y = m_s * x + q_s

            # filter the only valid intersection and correct for float point error
            if y_points[i + 1] * 1.001 >= y >= y_points[i] * 0.999:
                return y
        return None

    def calculate_sforzo_max(self):
        self.sforzo_max = np.max(self.punti_sforzo)

    def calculate_indice_elasticita(self):
        self.indice_elasticita = self.punto_snervamento ** 2 / 2 * self.modulo_young

    def calculate_coeff_strizione(self):
        self.coeff_strizione = (self.sezione_iniziale - self.sezione_finale) * 100 / self.sezione_iniziale


solver = Solver()
