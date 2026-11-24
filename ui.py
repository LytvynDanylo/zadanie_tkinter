import math
import tkinter as tk
from tkinter import messagebox, ttk
from formulas import (
    celsius_to_fahrenheit,
    generate_temperatures,
    meters_to_miles,
    generate_distances,
    array_operations
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

        self.temperature_frame = ttk.Frame(self.input_frame)
        ttk.Label(self.temperature_frame, text="Teplota (°C):").grid(
            row=0, column=0, padx=(0, 8)
        )
        self.input_field = ttk.Entry(self.temperature_frame, width=14)
        self.input_field.grid(row=0, column=1, padx=(0, 8))
        self.input_field.insert(0, "25")
        calculate_button = ttk.Button(
            self.temperature_frame, text="Vypočítať", command=self.calculate_input
        )
        calculate_button.grid(row=0, column=2, padx=(0, 8))
        self.result_label = ttk.Label(
            self.temperature_frame, text="Výsledok: —", foreground="#005a9e"
        )
        self.result_label.grid(row=0, column=3)

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
        self.canvas = tk.Canvas(
            chart_frame,
            height=420,
            background="#ffffff",
            highlightthickness=1,
            highlightbackground="#cccccc",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_chart()
        self.canvas.bind("<Configure>", lambda event: self.draw_chart())

        table_frame = ttk.Frame(notebook)
        notebook.add(table_frame, text="Tabuľka hodnôt")
        self.values_table = ttk.Treeview(
            table_frame,
            columns=("index", "input1", "input2", "result"),
            show="headings",
            height=20,
        )
        for column in ("index", "input1", "input2", "result"):
            self.values_table.heading(column, text="")
            self.values_table.column(column, width=0, anchor=tk.CENTER)
        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.values_table.yview
        )
        self.values_table.configure(yscrollcommand=scrollbar.set)
        self.values_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
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
        self.values_table.delete(*self.values_table.get_children())
        if self.formula_choice.get() == "Teplota: °C → °F":
            self.values_table.heading("index", text="Poradie")
            self.values_table.heading("input1", text="Pôvodná teplota (°C)")
            self.values_table.heading("input2", text="")
            self.values_table.heading("result", text="Vypočítaná teplota (°F)")
            self.values_table.column("index", width=90)
            self.values_table.column("input1", width=210)
            self.values_table.column("input2", width=0)
            self.values_table.column("result", width=240)
            rows = (
                (index, f"{celsius:.1f}", "", f"{fahrenheit:.1f}")
                for index, (celsius, fahrenheit) in enumerate(
                    zip(self.values, self.converted), start=1
                )
            )
        else:
            self.values_table.heading("index", text="Poradie")
            self.values_table.heading("input1", text="Vzdialenosť (m)")
            self.values_table.heading("input2", text="")
            self.values_table.heading("result", text="Vzdialenosť (americké míle)")
            self.values_table.column("index", width=80)
            self.values_table.column("input1", width=160)
            self.values_table.column("input2", width=0)
            self.values_table.column("result", width=240)
            rows = (
                (
                    index,
                    f"{meters:.1f}",
                    "",
                    f"{miles:.3f}",
                )
                for index, (meters, miles) in enumerate(
                    zip(self.distances, self.miles), start=1
                )
            )
        for row in rows:
            self.values_table.insert("", tk.END, values=row)

    def generate_new_values(self):
        self.values = generate_temperatures()
        self.converted = [celsius_to_fahrenheit(value) for value in self.values]
        self.distances = generate_distances()
        self.miles = [meters_to_miles(value) for value in self.distances]
        self.update_visualization()

    def draw_chart(self):
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 700)
        height = max(self.canvas.winfo_height(), 420)
        left, right, top, bottom = (
            70,
            75 if self.formula_choice.get() != "Teplota: °C → °F" else 20,
            55,
            55,
        )
        plot_width = width - left - right
        plot_height = height - top - bottom

        if self.formula_choice.get() == "Teplota: °C → °F":
            x_values = list(range(1, len(self.values) + 1))
            first_series = self.values
            second_series = self.converted
            y_values = first_series + second_series
            title = "Porovnanie teploty (°C) a prevedených hodnôt (°F)"
            x_label = "Poradie hodnoty"
            first_label = "Pôvodná teplota (°C)"
            second_label = "Prepočítaná teplota (°F)"
            separate_scales = False
        else:
            x_values = list(range(1, len(self.distances) + 1))
            first_series = self.distances
            second_series = self.miles
            y_values = first_series
            title = "Porovnanie vzdialenosti v metroch a amerických míľach"
            x_label = "Poradie hodnoty"
            first_label = "Vzdialenosť (m)"
            second_label = "Vzdialenosť (mi)"
            separate_scales = True

        x_min, x_max = min(x_values), max(x_values)
        x_range = x_max - x_min or 1
        minimum, maximum = min(y_values), max(y_values)
        value_range = maximum - minimum or 1

        def x(value):
            return left + (value - x_min) * plot_width / x_range

        def y(value):
            return top + (maximum - value) * plot_height / value_range

        if separate_scales:
            second_minimum, second_maximum = min(second_series), max(second_series)
            second_range = second_maximum - second_minimum or 1

            def y_second(value):
                return top + (second_maximum - value) * plot_height / second_range
        else:
            y_second = y

        self.canvas.create_text(
            width / 2,
            18,
            text=title,
            font=("Segoe UI", 12, "bold"),
        )

        for step in range(6):
            y_value = minimum + step * value_range / 5
            y_pos = y(y_value)
            self.canvas.create_line(
                left, y_pos, width - right, y_pos, fill="#dddddd"
            )
            self.canvas.create_text(
                left - 10,
                y_pos,
                text=f"{y_value:.0f}",
                anchor="e",
                font=("Segoe UI", 9),
            )
            x_value = x_min + step * x_range / 5
            x_pos = x(x_value)
            self.canvas.create_line(
                x_pos, height - bottom, x_pos, height - bottom + 5, fill="#666666"
            )
            self.canvas.create_text(
                x_pos,
                height - bottom + 17,
                text=f"{x_value:.1f}",
                font=("Segoe UI", 8),
            )

        self.canvas.create_line(
            left, height - bottom, width - right, height - bottom, fill="#666666"
        )
        self.canvas.create_line(
            left, top, left, height - bottom, fill="#666666"
        )
        if separate_scales:
            self.canvas.create_line(
                width - right, top, width - right, height - bottom, fill="#666666"
            )
            for step in range(6):
                second_value = second_minimum + step * second_range / 5
                y_pos = y_second(second_value)
                self.canvas.create_line(
                    width - right, y_pos, width - right - 5, y_pos, fill="#666666"
                )
                self.canvas.create_text(
                    width - right + 8,
                    y_pos,
                    text=f"{second_value:.1f}",
                    anchor="w",
                    font=("Segoe UI", 9),
                )
            self.canvas.create_text(
                16, height / 2, text="Vzdialenosť (m)", angle=90,
                font=("Segoe UI", 9),
            )
            self.canvas.create_text(
                width - right + 52, height / 2,
                text="Vzdialenosť (mi)", angle=90,
                font=("Segoe UI", 9),
            )
        self.canvas.create_text(
            width / 2,
            height - 18,
            text=x_label,
            font=("Segoe UI", 10),
        )

        first_points = [
            (x(x_value), y(value))
            for x_value, value in zip(x_values, first_series)
        ]
        self.canvas.create_line(
            [coordinate for point in first_points for coordinate in point],
            fill="#0078d4",
            width=2,
            smooth=False,
        )

        legend_y = top + 18
        self.canvas.create_line(
            width - 230, legend_y, width - 205, legend_y, fill="#0078d4", width=3
        )
        self.canvas.create_text(
            width - 195,
            legend_y,
            text=first_label,
            anchor="w",
            font=("Segoe UI", 9),
        )
        if second_series is not None:
            second_points = [
                (x(x_value), y_second(value))
                for x_value, value in zip(x_values, second_series)
            ]
            self.canvas.create_line(
                [coordinate for point in second_points for coordinate in point],
                fill="#d83b01",
                width=2,
                smooth=False,
            )
            self.canvas.create_line(
                width - 230,
                legend_y + 22,
                width - 205,
                legend_y + 22,
                fill="#d83b01",
                width=3,
            )
            self.canvas.create_text(
                width - 195,
                legend_y + 22,
                text=second_label,
                anchor="w",
                font=("Segoe UI", 9),
            )

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