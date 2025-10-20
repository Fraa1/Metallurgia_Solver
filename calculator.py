import numpy as np


class Calculator:
    def __init__(self, df, dati, strings):
        self.intersection_point = None
        self.indice_elasticita = None
        self.sforzo_max = None
        self.punto_snervamento = None
        self.sezione_iniziale = None
        self.punti_deformazione = []
        self.punti_sforzo = []
        self.modulo_young = None

        # dati
        self.forma_sezione = dati['forma_sezione']
        self.lunghezza_iniziale = dati['lunghezza_iniziale']
        self.dimensione = dati['dimensione']
        self.units = dati['units']
        if self.units == 'gigapascal':
            self.sezione_finale = dati['sezione_finale'] / 1000000
        else:
            self.sezione_finale = dati['sezione_finale']

        self.strings = strings

        self.df = df


    def update(self):
        self.calc_sezione_iniziale()
        self.convert_points()
        self.calc_modulo_young()
        self.strings['modulo_young'].set(f'Modulo di Young: {self.modulo_young:.2f}')
        self.calc_sforzo_snervamento()
        self.strings['sforzo_snervamento'].set(f'Sforzo di Snervamento: {self.punto_snervamento:.2f}')
        self.calc_sforzo_max()
        self.strings['sforzo_max'].set(f'Sforzo Massimo: {self.sforzo_max:.2f}')
        self.calc_indice_elasticita()
        self.strings['indice_elasticita'].set(f'Indice di Elasticità: {self.indice_elasticita:.2f}')
        self.calc_coeff_strizione()
        self.strings['coeff_strizione'].set(f'Coefficiente di Strizione: {self.coeff_strizione:.2f}')

    def convert_points(self):
        x = np.array(self.df["x(mm)"])
        y = np.array(self.df["y(kN)"])
        if self.units == 'gigapascal':
            self.sezione_iniziale /= 1000000
            self.punti_sforzo = y / (self.sezione_iniziale * 1000000)
        elif self.units == 'newtonmm':
            self.punti_sforzo = y / self.sezione_iniziale * 1000

        self.punti_deformazione = x / self.lunghezza_iniziale


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
        #x = np.linspace(0, np.max(self.punti_deformazione))
        #y = x * self.modulo_young + intercept
        #self.punto_snervamento = self.find_intersection(self.modulo_young, intercept)[1]
        self.intersection_point = (self.find_intersection(self.modulo_young, intercept))
        self.punto_snervamento = self.intersection_point[1]

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
                print(x, y)
                return x, y

        print("test")
        return None

    def calc_sforzo_max(self):
        self.sforzo_max = np.max(self.punti_sforzo)

    def calc_indice_elasticita(self):
        self.indice_elasticita = self.punto_snervamento ** 2 / 2 * self.modulo_young

    def calc_coeff_strizione(self):
        self.coeff_strizione = (self.sezione_iniziale - self.sezione_finale) * 100 / self.sezione_iniziale