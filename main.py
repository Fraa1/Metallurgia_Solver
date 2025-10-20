from widgets import *
import pandas as pd
from matplotlib import pyplot as plt
from calculator import Calculator


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.plot = None
        self.punti_deformazione = None
        self.punti_sforzo = None
        self.calc = None

        # ctk setup
        ctk.set_appearance_mode('dark')
        plt.style.use('dark_background')
        plt.tight_layout()
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.title('Metallurgia Solver')
        self.minsize(1600, 800)

        # ctk layout
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=7, uniform='a')

        # ctk widgets
        self.control_frame = ControlFrame(self, self.load_csv, self.update_plot)

        self.df = pd.read_csv('point_data.csv', skipinitialspace=True)

        self.fig, self.ax = plt.subplots(figsize=(16, 7))
        self.fig.set_facecolor("#1a1a1a")
        self.ax.set_facecolor("#1a1a1a")

        # run
        self.mainloop()

    def load_csv(self, path):
        if path:
            self.df = pd.read_csv(path, skipinitialspace=True)

    def display_plot(self):
        self.plot = PlotDisplay(self, self.fig, self.ax, self.punti_deformazione, self.punti_sforzo, self.calc)
        self.plot.style_plot(self.control_frame.units)

    def update_plot(self, dati, strings):
        if self.df is not None:
            self.calc = Calculator(self.df, dati, strings)
            self.calc.update()
            self.punti_deformazione, self.punti_sforzo = self.calc.convert_points()

            self.ax.clear()
            self.display_plot()


if __name__ == '__main__':
    app = App()