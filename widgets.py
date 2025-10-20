import os.path
import numpy as np
import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ControlFrame(ctk.CTkFrame):
    def __init__(self, parent, import_func, update_func):
        super().__init__(master=parent)

        self.units = None
        self.forma_sezione = None

        self.grid(row=0, column=0, sticky='nsew')
        self.import_func = import_func
        self.update_func = update_func

        self.rowconfigure((0, 1, 2), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.columnconfigure((4, 5), weight=2, uniform='a')

        self.update_plot_button = ctk.CTkButton(self, text='Update Plot', command=self.send_data)
        self.load_csv_button = ctk.CTkButton(self, text='Load CSV', command=self.import_csv)
        self.csv_string = ctk.StringVar(value='no CSV file loaded')
        self.loaded_csv_label = ctk.CTkLabel(self, textvariable=self.csv_string)

        # entries
        self.lungh_iniz_entry = ctk.CTkEntry(self, 200, 30, placeholder_text='Lunghezza Iniziale in mm')
        self.sez_finale_entry = ctk.CTkEntry(self, 200, 30, placeholder_text='Sezione Finale in mm²')
        self.dimensione_entry = None

        # radio button forma
        self.radio_forma_string = ctk.CTkLabel(
            self, text='Forma Sezione', font=('TkDefaultFont', 16), fg_color=CTK_BLUE, corner_radius=8
        )
        self.forma_var = ctk.StringVar()
        self.radio1 = ctk.CTkRadioButton(
            self, text='Quadrata', value='quadrata', variable=self.forma_var,command=self.set_forma_sezione
        )
        self.radio2 = ctk.CTkRadioButton(
            self, text='Circolare', value='circolare', variable=self.forma_var, command=self.set_forma_sezione
        )
        self.radio1.select()
        self.set_forma_sezione()

        # radio button unità
        self.radio_units_string = ctk.CTkLabel(
            self, text='Unità di Misura', font=('TkDefaultFont', 16), fg_color=CTK_BLUE, corner_radius=8
        )
        self.units_var = ctk.StringVar()
        self.radio3 = ctk.CTkRadioButton(
            self, text='N/mm²', value='newtonmm', variable=self.units_var, command=self.set_units
        )
        self.radio4 = ctk.CTkRadioButton(
            self, text='GigaPascal', value='gigapascal', variable=self.units_var, command=self.set_units
        )
        self.radio3.select()
        self.set_units()

        # results
        self.modulo_young_string = ctk.StringVar(value='Modulo di Young: ')
        self.modulo_young_label = ctk.CTkLabel(self, textvariable= self.modulo_young_string)
        self.sforzo_snervamento_string = ctk.StringVar(value='Sforzo Snervamento: ')
        self.sforzo_snervamento_label = ctk.CTkLabel(self, textvariable= self.sforzo_snervamento_string)
        self.sforzo_max_string = ctk.StringVar(value='Sforzo Massimo: ')
        self.sforzo_max_label = ctk.CTkLabel(self, textvariable= self.sforzo_max_string)
        self.indice_elasticita_string = ctk.StringVar(value='Indice di Elasticità: ')
        self.indice_elasticita_label = ctk.CTkLabel(self, textvariable= self.indice_elasticita_string)
        self.coeff_strizione_string = ctk.StringVar(value='Coefficiente di Strizione: ')
        self.coeff_strizione_label = ctk.CTkLabel(self, textvariable= self.coeff_strizione_string)

        # place in grid
        self.radio_forma_string.grid(row=0, column=0)
        self.radio1.grid(row=1, column=0)
        self.radio2.grid(row=2, column=0)

        self.lungh_iniz_entry.grid(row=0, column=1)
        self.sez_finale_entry.grid(row=1, column=1)

        self.load_csv_button.grid(row=0, column=2)
        self.loaded_csv_label.grid(row=1, column=2)
        self.update_plot_button.grid(row=2, column=2)

        self.radio_units_string.grid(row=0, column=3)
        self.radio3.grid(row=1, column=3)
        self.radio4.grid(row=2, column=3)

        self.modulo_young_label.grid(row=0, column=4, sticky='w')
        self.sforzo_snervamento_label.grid(row=1, column=4, sticky='w')
        self.sforzo_max_label.grid(row=2, column=4, sticky='w')
        self.indice_elasticita_label.grid(row=0, column=5, sticky='w')
        self.coeff_strizione_label.grid(row=1, column=5, sticky='w')


    def import_csv(self):
        csv_path = filedialog.askopenfilename()
        if csv_path:
            self.csv_string.set(f'LOADED {os.path.split(csv_path)[1]}')
        self.import_func(csv_path)

    def set_forma_sezione(self):
        if self.dimensione_entry:
            self.dimensione_entry.grid_forget()
        self.forma_sezione = self.forma_var.get()
        if self.forma_sezione == 'quadrata':
            self.dimensione_entry = ctk.CTkEntry(self, 200, 30, placeholder_text='Lato in mm')
            self.dimensione_entry.grid(row=2, column=1)
        elif self.forma_sezione == 'circolare':
            self.dimensione_entry = ctk.CTkEntry(self, 200, 30, placeholder_text='Diametro in mm')
            self.dimensione_entry.grid(row=2, column=1)

    def set_units(self):
        self.units = self.units_var.get()

    def send_data(self):
        dati = {
            'forma_sezione': self.forma_sezione,
            'lunghezza_iniziale': int(self.lungh_iniz_entry.get()),
            'dimensione': int(self.dimensione_entry.get()),
            'sezione_finale': int(self.sez_finale_entry.get()),
            'units': self.units
        }
        strings = {
            'modulo_young': self.modulo_young_string,
            'sforzo_snervamento': self.sforzo_snervamento_string,
            'sforzo_max': self.sforzo_max_string,
            'indice_elasticita': self.indice_elasticita_string,
            'coeff_strizione': self.coeff_strizione_string
        }

        self.update_func(dati, strings)


class PlotDisplay(Canvas):
    def __init__(self, parent, fig, ax, punti_deformazione, punti_sforzo, calc):
        super().__init__(master=parent, background=BACKGROUND, bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=1, sticky='nsew')

        self.fig = fig
        self.ax = ax
        self.punti_deformazione = punti_deformazione
        self.punti_sforzo = punti_sforzo
        self.calc = calc

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.widget = self.canvas.get_tk_widget()
        self.widget.pack(fill=ctk.BOTH, expand=True)

    def style_plot(self, units):
        # blue line
        self.ax.plot(self.punti_deformazione, self.punti_sforzo, "o-", color=CTK_BLUE)
        # red line
        x = np.array([0.002, self.calc.intersection_point[0]])
        y = np.array([0, self.calc.intersection_point[1]])
        if units == 'gigapascal':
            y *= 1000000
        self.ax.plot(x, y, "o-", color=RED)

        self.ax.set_xlim(0, np.max(self.punti_deformazione) * 1.01)
        self.ax.set_ylim(0, np.max(self.punti_sforzo) * 1.01)

        if units == 'gigapascal':
            self.ax.set_ylabel("Sforzo in Gigapascal", size=15)
        elif units == 'newtonmm':
            self.ax.set_ylabel("Sforzo in N/mm²", size=15)
        self.ax.set_xlabel("Deformazione ε", size=15)

        self.ax.set_xticks(self.punti_deformazione)
        self.ax.set_yticks(self.punti_sforzo)

        self.ax.tick_params(axis="x", labelrotation=90, labelsize=8)
        self.ax.tick_params(axis="y", labelsize=8)

