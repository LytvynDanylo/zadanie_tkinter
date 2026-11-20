import random
import math
import tkinter as tk
from tkinter import messagebox, ttk


def celsius_to_fahrenheit(value):
    """Convert a Celsius temperature to Fahrenheit."""
    return value * 1.8 + 32


def generate_temperatures(count=60, seed=None):
    """Generate an array of random Celsius temperatures."""
    rng = random.Random(seed)
    return [round(rng.uniform(-20.0, 40.0), 1) for _ in range(count)]


def pressure_from_force(force, area):
    """Calculate pressure in pascals from force and area."""
    if area <= 0:
        raise ValueError("Area must be greater than zero.")
    return force / area


def generate_forces(count=60, seed=None):
    """Generate an array of random forces in newtons."""
    rng = random.Random(seed)
    return [round(rng.uniform(10.0, 1000.0), 1) for _ in range(count)]


def array_operations(values):
    """Return at least two operations performed on the value array."""
    return {
        "sorted": sorted(values),
        "average": sum(values) / len(values),
        "minimum": min(values),
        "maximum": max(values),
    }


class PhysicsFormulaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fyzikálne vzorce")
        self.root.geometry("1000x820")
        self.root.minsize(780, 680)

        self.values = generate_temperatures()
        self.converted = [celsius_to_fahrenheit(value) for value in self.values]
        self.forces = generate_forces()

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
                "Tlak: p = F / S",
            ),
            state="readonly",
            width=24,
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

        self.pressure_frame = ttk.LabelFrame(
            self.input_frame,
            text="Tlak: p = F / S",
        )
        ttk.Label(self.pressure_frame, text="Sila (N):").grid(
            row=0, column=0, padx=(8, 4), pady=8
        )
        self.force_field = ttk.Entry(self.pressure_frame, width=12)
        self.force_field.grid(row=0, column=1, padx=4, pady=8)
        self.force_field.insert(0, "100")
        ttk.Label(self.pressure_frame, text="Plocha (m²):").grid(
            row=0, column=2, padx=(12, 4), pady=8
        )
        self.area_field = ttk.Entry(self.pressure_frame, width=12)
        self.area_field.grid(row=0, column=3, padx=4, pady=8)
        self.area_field.insert(0, "0.01")
        ttk.Button(
            self.pressure_frame,
            text="Vypočítať tlak",
            command=self.calculate_pressure,
        ).grid(row=0, column=4, padx=(8, 12), pady=8)
        self.pressure_result_label = ttk.Label(
            self.pressure_frame, text="p = —", foreground="#005a9e"
        )
        self.pressure_result_label.grid(row=0, column=5, padx=8, pady=8)
        self.area_field.bind("<KeyRelease>", self.on_pressure_parameter_changed)
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
        self.area_field.bind("<Return>", lambda event: self.calculate_pressure())

    def on_formula_changed(self, _event=None):
        if self.formula_choice.get() == "Teplota: °C → °F":
            self.pressure_frame.pack_forget()
            self.temperature_frame.pack()
        else:
            self.temperature_frame.pack_forget()
            self.pressure_frame.pack()
        self.update_visualization()

    def on_pressure_parameter_changed(self, _event=None):
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
            operations = array_operations(self.forces)
            summary = (
                f"Pole síl: {len(self.forces)} hodnôt  |  Priemer: "
                f"{operations['average']:.2f} N  |  Minimum: "
                f"{operations['minimum']:.1f} N  |  "
                f"Maximum: {operations['maximum']:.1f} N"
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
            self.values_table.heading("input1", text="Sila (N)")
            self.values_table.heading("input2", text="Plocha (m²)")
            self.values_table.heading("result", text="Vypočítaný tlak (Pa)")
            self.values_table.column("index", width=80)
            self.values_table.column("input1", width=160)
            self.values_table.column("input2", width=160)
            self.values_table.column("result", width=200)
            area = self.get_area()
            if area is None:
                return
            rows = (
                (
                    index,
                    f"{force:.1f}",
                    f"{area:.4f}",
                    f"{pressure_from_force(force, area):.2f}",
                )
                for index, force in enumerate(self.forces, start=1)
            )
        for row in rows:
            self.values_table.insert("", tk.END, values=row)

    def get_area(self):
        try:
            area = float(self.area_field.get().strip().replace(",", "."))
        except ValueError:
            return None
        if not math.isfinite(area) or area <= 0:
            return None
        return area

    def generate_new_values(self):
        self.values = generate_temperatures()
        self.converted = [celsius_to_fahrenheit(value) for value in self.values]
        self.forces = generate_forces()
        self.update_visualization()

    def draw_chart(self):
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 700)
        height = max(self.canvas.winfo_height(), 420)
        left, right, top, bottom = 70, 20, 55, 55
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
        else:
            area = self.get_area()
            if area is None:
                self.canvas.create_text(
                    width / 2,
                    height / 2,
                    text="Zadajte plochu väčšiu ako 0 m².",
                    font=("Segoe UI", 12),
                )
                return
            x_values = list(range(1, len(self.forces) + 1))
            first_series = self.forces
            second_series = [
                pressure_from_force(force, area)
                for force in self.forces
            ]
            y_values = first_series + second_series
            title = f"Porovnanie sily (N) a tlaku (Pa), plocha = {area:g} m²"
            x_label = "Poradie hodnoty"
            first_label = "Pôvodná sila (N)"
            second_label = "Vypočítaný tlak (Pa)"

        x_min, x_max = min(x_values), max(x_values)
        x_range = x_max - x_min or 1
        minimum, maximum = min(y_values), max(y_values)
        value_range = maximum - minimum or 1

        def x(value):
            return left + (value - x_min) * plot_width / x_range

        def y(value):
            return top + (maximum - value) * plot_height / value_range

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
                (x(x_value), y(value))
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

    def calculate_pressure(self):
        try:
            force = float(self.force_field.get().strip().replace(",", "."))
            area = float(self.area_field.get().strip().replace(",", "."))
        except ValueError:
            messagebox.showerror(
                "Neplatný vstup",
                "Zadajte číselné hodnoty sily a plochy.",
            )
            return

        if (
            not math.isfinite(force)
            or not math.isfinite(area)
            or force < 0
            or area <= 0
        ):
            messagebox.showerror(
                "Neplatný vstup",
                "Sila musí byť nezáporná a plocha väčšia ako nula.",
            )
            return

        pressure = pressure_from_force(force, area)
        self.pressure_result_label.config(text=f"p = {pressure:.2f} Pa")
        self.refresh_values_table()
        self.draw_chart()


def main():
    root = tk.Tk()
    app = PhysicsFormulaApp(root)
    root.mainloop()
    return app


if __name__ == "__main__":
    main()
