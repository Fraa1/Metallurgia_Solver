import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CSVImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column=0, columnspan=2, row=0, sticky='nsew')
        self.import_func = import_func

        ctk.CTkButton(self, text='Load CSV', command=self.import_csv).pack(expand=True)

    def import_csv(self):
        path = filedialog.askopenfilename()
        self.import_func(path)

class PlotDisplay(Canvas):
    def __init__(self, parent, fig):
        super().__init__(master=parent, background=BACKGROUND, bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=0, column=1, sticky='nsew')

        self.fig = fig
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.widget = self.canvas.get_tk_widget()
        self.widget.pack(expand=True)
