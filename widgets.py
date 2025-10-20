import os.path
import numpy as np
import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ControlFrame(ctk.CTkFrame):
    def __init__(self, parent, import_func, update_func):
        super().__init__(master=parent)

        self.forma_sezione = None

        self.grid(row=0, column=0, sticky='nsew')
        self.import_func = import_func
        self.update_func = update_func

        self.rowconfigure((0, 1, 2), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        self.update_plot_button = ctk.CTkButton(self, text='Update Plot', command=self.get_dati)
        self.load_csv_button = ctk.CTkButton(self, text='Load CSV', command=self.import_csv)
        self.csv_string = ctk.StringVar(value='no CSV file loaded')
        self.loaded_csv_label = ctk.CTkLabel(self, textvariable=self.csv_string)

        # entries
        self.lungh_iniz_entry = ctk.CTkEntry(self, 200, 30, placeholder_text='Lunghezza Iniziale')
        self.sez_finale_entry = ctk.CTkEntry(self, 200, 30, placeholder_text='Sezione Finale')
        self.dimensione_entry = None

        # radio button
        self.radio_question_string = ctk.CTkLabel(
            self, text='Forma Sezione', font=('TkDefaultFont', 16), fg_color='#1f6aa5', corner_radius=8
        )
        self.radio_var = ctk.StringVar()
        self.radio1 = ctk.CTkRadioButton(
            self, text='Quadrata', value='quadrata', variable=self.radio_var,command=self.set_forma_sezione
        )
        self.radio2 = ctk.CTkRadioButton(
            self, text='Circolare', value='circolare', variable=self.radio_var, command=self.set_forma_sezione
        )
        self.radio1.select()
        self.set_forma_sezione()

        # place in grid
        self.radio_question_string.grid(row=0, column=0)
        self.radio1.grid(row=1, column=0)
        self.radio2.grid(row=2, column=0)

        self.lungh_iniz_entry.grid(row=0, column=1)
        self.sez_finale_entry.grid(row=1, column=1)

        self.load_csv_button.grid(row=0, column=2)
        self.loaded_csv_label.grid(row=1, column=2)
        self.update_plot_button.grid(row=2, column=2)


    def import_csv(self):
        csv_path = filedialog.askopenfilename()
        if csv_path:
            self.csv_string.set(f'LOADED {os.path.split(csv_path)[1]}')
        self.import_func(csv_path)

    def set_forma_sezione(self):
        if self.dimensione_entry:
            self.dimensione_entry.grid_forget()
        self.forma_sezione = self.radio_var.get()
        if self.forma_sezione == 'quadrata':
            self.dimensione_entry = ctk.CTkEntry(self, 200, 30, placeholder_text='Lato')
            self.dimensione_entry.grid(row=2, column=1)
        elif self.forma_sezione == 'circolare':
            self.dimensione_entry = ctk.CTkEntry(self, 200, 30, placeholder_text='Diametro')
            self.dimensione_entry.grid(row=2, column=1)

    def get_dati(self):
        dati = {
            'forma_sezione': self.forma_sezione,
            'lunghezza_iniziale': int(self.lungh_iniz_entry.get()),
            'dimensione': int(self.dimensione_entry.get()),
            'sezione_finale': int(self.sez_finale_entry.get())
        }

        self.update_func(dati)


class PlotDisplay(Canvas):
    def __init__(self, parent, fig, ax, punti_deformazione, punti_sforzo, calc):
        super().__init__(master=parent, background=BACKGROUND, bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=1, sticky='nsew')

        self.fig = fig
        self.ax = ax
        self.punti_deformazione = punti_deformazione
        self.punti_sforzo = punti_sforzo
        self.calc = calc

        self.style_plot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.widget = self.canvas.get_tk_widget()
        self.widget.pack(fill=ctk.BOTH, expand=True)

    def style_plot(self):
        self.ax.plot(self.punti_deformazione, self.punti_sforzo, "o-", color=CTK_BLUE)
        self.ax.plot(self.calc.calc_sforzo_snervamento()[0], self.calc.calc_sforzo_snervamento()[1], color=VIOLET)

        self.ax.set_xlim(0, np.max(self.punti_deformazione) * 1.01)
        self.ax.set_ylim(0, np.max(self.punti_sforzo) * 1.01)

        self.ax.set_ylabel("Sforzo in N/mm²", size=15)
        self.ax.set_xlabel("Deformazione ε", size=15)

        self.ax.set_xticks(self.punti_deformazione)
        self.ax.set_yticks(self.punti_sforzo)

        self.ax.tick_params(axis="x", labelrotation=90, labelsize=8)
        self.ax.tick_params(axis="y", labelsize=8)

