from widgets import *
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import ImageTk

from calculator import Calculator


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.punti_deformazione = None
        self.punti_sforzo = None

        # ctk setup
        ctk.set_appearance_mode('dark')
        self.geometry('1600x1000')
        self.title('Metallurgia Solver')
        self.minsize(800, 500)

        # ctk layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        # ctk widgets
        self.csv_button = CSVImport(self, self.load_csv)

        self.df = pd.read_csv('point_data.csv', skipinitialspace=True)
        self.calc = Calculator(self.df)

        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.set_facecolor("#1a1a1a")
        self.ax.set_facecolor("#1a1a1a")

        self.update_plot()

        # run
        self.mainloop()

    def load_csv(self, path):
        if path:
            self.csv_button.grid_forget() # hide button
            self.df = pd.read_csv(path, skipinitialspace=True)
            self.calc.df = self.df
            self.display_plot()

    def display_plot(self):
        self.create_plot()
        PlotDisplay(self, self.fig)

    def update_plot(self):
        if self.df is not None:
            self.punti_deformazione, self.punti_sforzo = self.calc.convert_points()
            self.ax.clear()

            self.create_plot()


    def create_plot(self):
        self.ax.plot(self.punti_deformazione, self.punti_sforzo, "o-", color='#1989e2')
        self.ax.plot(self.calc.calc_sforzo_snervamento()[0], self.calc.calc_sforzo_snervamento()[1], color='#e21941')

        self.ax.set_xlim(0, np.max(self.punti_deformazione) * 1.01)
        self.ax.set_ylim(0, np.max(self.punti_sforzo) * 1.01)

        self.ax.set_ylabel("Sforzo in N/mm²", color='#ffffff', size=15)
        self.ax.set_xlabel("Deformazione ε", color='#ffffff', size=15)

        self.ax.set_xticks(self.punti_deformazione)
        self.ax.set_yticks(self.punti_sforzo)

        self.ax.tick_params(axis="x", labelrotation=90, labelsize=8, color='#ffffff', labelcolor='#ffffff')
        self.ax.tick_params(axis="y", labelsize=8, color='#ffffff', labelcolor='#ffffff')

if __name__ == '__main__':
    app = App()