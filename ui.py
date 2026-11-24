import math
import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from formulas import (
    celsius_to_fahrenheit,
    generate_temperatures,
    meters_to_miles,
    generate_distances,
    array_operations,
)


class PhysicsFormulaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fyzikálne vzorce")
        self.root.geometry("1000x820")
        self.root.minsize(780, 680)

        self.values = generate_temperatures()
        self.converted = [celsius_to_fahrenheit(value) for value in self.values]
        self.distances = generate_distances()
        self.miles = [meters_to_miles(value) for value in self.distances]

        title = ttk.Label(
            root,
            text="Výpočty fyzikálnych vzorcov",
            font=("Segoe UI", 15, "bold"),
        )
        title.pack(pady=(12, 8))

        selector_frame = ttk.Frame(root)
        selector_frame.pack(pady=6)
        ttk.Label(selector_frame, text="Vyberte vzorec:").pack(
            side=tk.LEFT, padx=(0, 8)
        )
        self.formula_choice = tk.StringVar(value="Teplota: °C → °F")
        formula_selector = ttk.Combobox(
            selector_frame,
            textvariable=self.formula_choice,
            values=(
                "Teplota: °C → °F",
                "Vzdialenosť: metre → americké míle",
            ),
            state="readonly",
            width=34,
        )
        formula_selector.pack(side=tk.LEFT)
        formula_selector.bind("<<ComboboxSelected>>", self.on_formula_changed)

        self.input_frame = ttk.Frame(root)
        self.input_frame.pack(pady=6)

        self.temperature_frame = ttk.LabelFrame(
            self.input_frame,
            text="Prevod teploty: °C → °F",
        )
        ttk.Label(self.temperature_frame, text="Teplota (°C):").grid(
            row=0, column=0, padx=(8, 4), pady=8
        )
        self.input_field = ttk.Entry(self.temperature_frame, width=12)
        self.input_field.grid(row=0, column=1, padx=4, pady=8)
        self.input_field.insert(0, "25")
        ttk.Button(
            self.temperature_frame,
            text="Prepočítať",
            command=self.calculate_input,
        ).grid(row=0, column=2, padx=(8, 8), pady=8)
        self.result_label = ttk.Label(
            self.temperature_frame, text="Výsledok: —", foreground="#005a9e"
        )
        self.result_label.grid(row=0, column=3, padx=8, pady=8)

        self.distance_frame = ttk.LabelFrame(
            self.input_frame,
            text="Prevod vzdialenosti: metre → americké míle",
        )
        ttk.Label(self.distance_frame, text="Vzdialenosť (m):").grid(
            row=0, column=0, padx=(8, 4), pady=8
        )
        self.distance_field = ttk.Entry(self.distance_frame, width=12)
        self.distance_field.grid(row=0, column=1, padx=4, pady=8)
        self.distance_field.insert(0, "1000")
        ttk.Button(
            self.distance_frame,
            text="Prepočítať",
            command=self.calculate_distance,
        ).grid(row=0, column=2, padx=(8, 8), pady=8)
        self.distance_result_label = ttk.Label(
            self.distance_frame, text="Výsledok: —", foreground="#005a9e"
        )
        self.distance_result_label.grid(row=0, column=3, padx=8, pady=8)
        self.distance_field.bind("<KeyRelease>", self.on_distance_changed)
        self.temperature_frame.pack()

        ttk.Button(
            root,
            text="Generovať nové náhodné hodnoty",
            command=self.generate_new_values,
        ).pack(pady=4)

        self.summary_label = ttk.Label(root)
        self.summary_label.pack(pady=(0, 4))

        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        chart_frame = ttk.Frame(notebook)
        notebook.add(chart_frame, text="Graf")
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.chart = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.draw_chart()

        table_frame = ttk.Frame(notebook)
        notebook.add(table_frame, text="Tabuľka hodnôt")
        self.table_canvas = tk.Canvas(table_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.table_canvas.yview
        )
        self.table_canvas.configure(yscrollcommand=scrollbar.set)
        self.table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_content = ttk.Frame(self.table_canvas)
        self.table_window = self.table_canvas.create_window(
            (0, 0), window=self.table_content, anchor="nw"
        )
        self.table_content.bind(
            "<Configure>",
            lambda event: self.table_canvas.configure(
                scrollregion=self.table_canvas.bbox("all")
            ),
        )
        self.table_canvas.bind(
            "<Configure>",
            lambda event: self.table_canvas.itemconfigure(
                self.table_window, width=event.width
            ),
        )

        self.update_visualization()
        self.input_field.bind("<Return>", lambda event: self.calculate_input())
        self.distance_field.bind("<Return>", lambda event: self.calculate_distance())

    def on_formula_changed(self, _event=None):
        if self.formula_choice.get() == "Teplota: °C → °F":
            self.distance_frame.pack_forget()
            self.temperature_frame.pack()
        else:
            self.temperature_frame.pack_forget()
            self.distance_frame.pack()
        self.update_visualization()

    def on_distance_changed(self, _event=None):
        if self.formula_choice.get() != "Teplota: °C → °F":
            self.refresh_values_table()
            self.draw_chart()

    def update_visualization(self):
        self.update_summary()
        self.refresh_values_table()
        self.draw_chart()

    def update_summary(self):
        if self.formula_choice.get() == "Teplota: °C → °F":
            operations = array_operations(self.values)
            summary = (
                f"Pole: {len(self.values)} hodnôt  |  Priemer: "
                f"{operations['average']:.2f} °C  |  Minimum: "
                f"{operations['minimum']:.1f} °C  |  "
                f"Maximum: {operations['maximum']:.1f} °C"
            )
        else:
            operations = array_operations(self.distances)
            summary = (
                f"Pole vzdialeností: {len(self.distances)} hodnôt  |  Priemer: "
                f"{operations['average']:.2f} m  |  Minimum: "
                f"{operations['minimum']:.1f} m  |  "
                f"Maximum: {operations['maximum']:.1f} m"
            )
        self.summary_label.config(text=summary)

    def refresh_values_table(self):
        for child in self.table_content.winfo_children():
            child.destroy()

        if self.formula_choice.get() == "Teplota: °C → °F":
            headers = (
                "Poradie",
                "Pôvodná teplota (°C)",
                "Vypočítaná teplota (°F)",
            )
            rows = (
                (index, f"{celsius:.1f}", f"{fahrenheit:.1f}")
                for index, (celsius, fahrenheit) in enumerate(
                    zip(self.values, self.converted), start=1
                )
            )
        else:
            headers = (
                "Poradie",
                "Vzdialenosť (m)",
                "Vzdialenosť (americké míle)",
            )
            rows = (
                (index, f"{meters:.1f}", f"{miles:.3f}")
                for index, (meters, miles) in enumerate(
                    zip(self.distances, self.miles), start=1
                )
            )

        for column, header in enumerate(headers):
            self.table_content.grid_columnconfigure(
                column, weight=1, uniform="table_columns"
            )
            tk.Label(
                self.table_content,
                text=header,
                font=("Segoe UI", 10, "bold"),
                background="#e8eef5",
                borderwidth=1,
                relief=tk.SOLID,
                padx=8,
                pady=5,
            ).grid(row=0, column=column, sticky="nsew")

        for row_index, row in enumerate(rows, start=1):
            for column, value in enumerate(row):
                tk.Label(
                    self.table_content,
                    text=value,
                    font=("Segoe UI", 10),
                    background="#ffffff" if row_index % 2 else "#f5f7fa",
                    borderwidth=1,
                    relief=tk.SOLID,
                    padx=8,
                    pady=4,
                ).grid(row=row_index, column=column, sticky="nsew")

    def generate_new_values(self):
        self.values = generate_temperatures()
        self.converted = [celsius_to_fahrenheit(value) for value in self.values]
        self.distances = generate_distances()
        self.miles = [meters_to_miles(value) for value in self.distances]
        self.update_visualization()

    def draw_chart(self):
        self.figure.clear()

        if self.formula_choice.get() == "Teplota: °C → °F":
            x_values = list(range(1, len(self.values) + 1))
            axes = self.figure.add_subplot(111)
            axes.plot(
                x_values,
                self.values,
                color="#0078d4",
                label="Pôvodná teplota (°C)",
            )
            axes.plot(
                x_values,
                self.converted,
                color="#d83b01",
                label="Prepočítaná teplota (°F)",
            )
            axes.set_title("Porovnanie teploty (°C) a prevedených hodnôt (°F)")
            axes.set_xlabel("Poradie hodnoty")
            axes.set_ylabel("Teplota")
            axes.grid(True, linestyle="--", alpha=0.4)
            axes.legend()
            self.figure.tight_layout()
        else:
            x_values = list(range(1, len(self.distances) + 1))
            axes = self.figure.add_subplot(111)
            miles_axes = axes.twinx()
            axes.set_zorder(miles_axes.get_zorder() + 1)
            axes.patch.set_visible(False)

            miles_line, = miles_axes.plot(
                x_values,
                self.miles,
                color="#d83b01",
                linestyle="--",
                linewidth=2,
                label="Vzdialenosť (mi)",
            )
            meters_line, = axes.plot(
                x_values,
                self.distances,
                color="#0078d4",
                linestyle="None",
                marker="o",
                markersize=5,
                markeredgecolor="white",
                markeredgewidth=0.6,
                label="Vzdialenosť (m)",
                zorder=5,
            )

            axes.set_title("Porovnanie vzdialenosti v metroch a amerických míľach")
            axes.set_xlabel("Poradie hodnoty")
            axes.set_ylabel("Vzdialenosť (m)")
            miles_axes.set_ylabel("Vzdialenosť (mi)")
            axes.grid(True, linestyle="--", alpha=0.4)
            axes.legend(
                (meters_line, miles_line),
                (meters_line.get_label(), miles_line.get_label()),
            )
            self.figure.tight_layout()

        self.chart.draw_idle()

    def calculate_input(self):
        text = self.input_field.get().strip().replace(",", ".")
        try:
            celsius = float(text)
        except ValueError:
            messagebox.showerror(
                "Neplatný vstup",
                "Zadajte platné číslo, napríklad 25 alebo -3.5.",
            )
            return

        if not math.isfinite(celsius):
            messagebox.showerror("Neplatný vstup", "Zadajte konečné číslo.")
            return

        fahrenheit = celsius_to_fahrenheit(celsius)
        self.result_label.config(
            text=f"Výsledok: {celsius:.2f} °C = {fahrenheit:.2f} °F"
        )

    def calculate_distance(self):
        try:
            meters = float(self.distance_field.get().strip().replace(",", "."))
        except ValueError:
            messagebox.showerror(
                "Neplatný vstup",
                "Zadajte platnú vzdialenosť v metroch.",
            )
            return

        if not math.isfinite(meters) or meters < 0:
            messagebox.showerror(
                "Neplatný vstup",
                "Vzdialenosť musí byť nezáporné konečné číslo.",
            )
            return

        miles = meters_to_miles(meters)
        self.distance_result_label.config(
            text=f"Výsledok: {meters:.2f} m = {miles:.3f} mi"
        )
        self.refresh_values_table()
        self.draw_chart()