import customtkinter as ctk
from customtkinter import filedialog
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from calculator import Calculator
from dati import LUNGHEZZA_INIZIALE
import calculator


class Plotter:

    def __init__(self, root):
        self.root = root
        root.title('Metallurgia Solver')

        self.punti_deformazione = np.array([])
        self.punti_sforzo = np.array([])

        self.df = pd.read_csv('point_data.csv', skipinitialspace=True)

        load_button = ctk.CTkButton(self.root, text='Load CSV', command=self.load_csv)
        load_button.pack(padx=10, pady=10)

        self.fig, self.ax = plt.subplots()

        plt.style.use('dark_background')

        self.fig, self.ax = plt.subplots(figsize=(16, 8))
        self.fig.set_facecolor("#1a1a1a")
        self.ax.set_facecolor("#1a1a1a")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.widget = self.canvas.get_tk_widget()
        self.widget.pack(padx=10, pady=10)

        self.update_plot()


    def load_csv(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.df = pd.read_csv(file_path, skipinitialspace=True)
            self.update_plot()

    def update_plot(self):
        if self.df is not None:
            self.convert_points()
            self.ax.clear()

            self.create_plot()

            self.canvas.draw()

    def create_plot(self):
        self.ax.plot(self.punti_deformazione, self.punti_sforzo, "o-", color='#1989e2')

        self.ax.set_xlim(0, np.max(self.punti_deformazione) * 1.01)
        self.ax.set_ylim(0, np.max(self.punti_sforzo) * 1.01)

        self.ax.set_ylabel("Sforzo in N/mm²", color='#ffffff', size=15)
        self.ax.set_xlabel("Deformazione ε", color='#ffffff', size=15)

        self.ax.set_xticks(self.punti_deformazione)
        self.ax.set_yticks(self.punti_sforzo)

        self.ax.tick_params(axis="x", labelrotation=90, labelsize=8, color='#ffffff', labelcolor='#ffffff')
        self.ax.tick_params(axis="y", labelsize=8, color='#ffffff', labelcolor='#ffffff')

    def convert_points(self):
        self.df = self.df.to_dict("list")
        x = np.array(self.df["x"])
        y = np.array(self.df["y"])
        self.punti_deformazione = x / LUNGHEZZA_INIZIALE
        self.punti_sforzo = y / calc.sezione_iniziale * 1000

calc = Calculator()

root = ctk.CTk()
app = Plotter(root)
root.mainloop()