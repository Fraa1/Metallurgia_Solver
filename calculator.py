import numpy as np


class Calculator:
    def __init__(self, df, dati):
        self.indice_elasticita = None
        self.sforzo_max = None
        self.punto_snervamento = None
        self.sezione_iniziale = None
        self.punti_deformazione = []
        self.punti_sforzo = []
        self.modulo_young = None

        self.forma_sezione = dati['forma_sezione']
        self.lunghezza_iniziale = dati['lunghezza_iniziale']
        self.dimensione = dati['dimensione']
        self.sezione_finale = dati['sezione_finale']

        self.df = df


    def update(self):
        self.calc_sezione_iniziale()
        self.convert_points()
        self.calc_modulo_young()
        self.calc_sforzo_snervamento()
        self.calc_sforzo_max()
        self.calc_indice_elasticita()
        self.calc_coeff_strizione()

    def convert_points(self):
        x = np.array(self.df["x"])
        y = np.array(self.df["y"])
        self.punti_deformazione = x / self.lunghezza_iniziale
        self.punti_sforzo = y / self.sezione_iniziale * 1000

        return self.punti_deformazione, self.punti_sforzo

    def calc_sezione_iniziale(self):
        if self.forma_sezione == "quadrata":
            self.sezione_iniziale = self.dimensione ** 2
        elif self.forma_sezione == "circolare":
            self.sezione_iniziale = self.dimensione ** 2 * np.pi / 4

    def calc_modulo_young(self):
        self.modulo_young = self.punti_sforzo[1] / self.punti_deformazione[1]

    def calc_sforzo_snervamento(self):
        intercept = - 0.002 * self.modulo_young
        x = np.linspace(0, np.max(self.punti_deformazione))
        y = x * self.modulo_young + intercept
        self.punto_snervamento = self.find_intersection(self.modulo_young, intercept)
        return x, y

    # m_s = pendenza retta (modulo Young), m_q = intercetta
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

    def calc_sforzo_max(self):
        self.sforzo_max = np.max(self.punti_sforzo)

    def calc_indice_elasticita(self):
        self.indice_elasticita = self.punto_snervamento ** 2 / 2 * self.modulo_young

    def calc_coeff_strizione(self):
        self.coeff_strizione = (self.sezione_iniziale - self.sezione_finale) * 100 / self.sezione_iniziale