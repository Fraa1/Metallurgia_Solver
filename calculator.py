from dati import *
import numpy as np


class Calculator:
    def __init__(self):
        self.sezione_iniziale = None

        self.update()

    def update(self):
        self.calc_sezione_iniziale()

    def calc_sezione_iniziale(self):
        if FORMA_SEZIONE == "quadrata":
            self.sezione_iniziale = LATO ** 2
        elif FORMA_SEZIONE == "circolare":
            self.sezione_iniziale = DIAMETRO ** 2 * np.pi / 4