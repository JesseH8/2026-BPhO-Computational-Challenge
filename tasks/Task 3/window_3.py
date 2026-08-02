import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sim_3 as sim

def open_window(window):

    window.title("Task 3")
    window.attributes("-fullscreen", True)

    fig = Figure(figsize = (8, 8))
    canvas = FigureCanvasTkAgg(fig, master = window)
    canvas.get_tk_widget().pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

    panel = tk.Frame(window)
    panel.pack(side = tk.LEFT, fill = tk.Y, padx = 10, pady = 10)

    ax1 = fig.add_subplot(211)
    ax1.set_title("Black-Body Radiation Spectrum")
    ax1.set_xlabel("Wavelength (μm)")
    ax1.set_ylabel(r"Spectral radiance, $B_\lambda$ (W m$^{-3}$ sr$^{-1}$)")

    temp_temp_pos = 0
    temp_temp_neg = 0

    def black_body_plot(T):
        data = sim.black_body_data(T)
        ax1.plot(*data, label = f"{T:.0f} K")
        ax1.legend()
        canvas.draw()

    def black_body_run():
        black_body_plot(float(temperature.get()))

    def temp_plus():
        nonlocal temp_temp_pos
        temp_temp_pos += 0.05
        black_body_plot(float(temperature.get()) * (1 + temp_temp_pos))

    def temp_minus():
        nonlocal temp_temp_neg
        temp_temp_neg += 0.05
        black_body_plot(float(temperature.get()) * (1 - temp_temp_neg))

    def black_body_clear():
       ax1.clear()
       ax1.set_title("Black-Body Radiation Spectrum")
       ax1.set_xlabel("Wavelength (μm)")
       ax1.set_ylabel(r"Spectral radiance, $B_\lambda$ (W m$^{-3}$ sr$^{-1}$)")
       canvas.draw()

    box1 = tk.LabelFrame(panel, text = "Black Body")
    box1.pack(pady = 10, fill = "x")

    tk.Label(box1, text = "Temperature (K)").pack()

    temperature = tk.Entry(box1)
    temperature.insert(0, "3000")
    temperature.pack()

    adjust = tk.Frame(box1)
    adjust.pack()

    tk.Button(adjust, text = "-5%", command = temp_minus).pack(side = tk.LEFT, padx = 2)
    tk.Button(adjust, text = "+5%", command = temp_plus).pack(side = tk.LEFT, padx = 2)

    tk.Button(box1, text = "RUN", command = black_body_run).pack(pady = 3)
    tk.Button(box1, text = "CLEAR", command = black_body_clear).pack()

    limit_reached = False

    def heat_capacity_run():
        nonlocal limit_reached

        theta_D = float(debye_temp.get())
        theta_E = 0.75 * theta_D

        if not limit_reached:
            ax2.plot(sim.limit(), label = "Dulong–Petit limit ($3R$)", linestyle = "--")
            limit_reached = True

        T, data = sim.debye_data(theta_D)
        ax2.plot(T, data, label = f"Debye model ($θ_D$ = {theta_D:.0f} K)")

        T, data = sim.einstein_data(theta_D)
        ax2.plot(T, data, label = f"Einstein model ($θ_E$ = {theta_E:.0f} K)")

        ax2.legend()
        canvas.draw()

    def heat_capacity_clear():
        nonlocal limit_reached

        ax2.clear()
        ax2.set_title("Heat Capacity Models")
        ax2.set_xlabel("Temperature (K)")
        ax2.set_ylabel(r"Molar heat capacity, $C_V$ (J mol$^{-1}$ K$^{-1}$)")
        limit_reached = False
        canvas.draw()

    ax2 = fig.add_subplot(212)
    ax2.set_title("Heat Capacity Models")
    ax2.set_xlabel("Temperature (K)")
    ax2.set_ylabel(r"Molar heat capacity, $C_V$ (J mol$^{-1}$ K$^{-1}$)")

    box2 = tk.LabelFrame(panel, text = "Heat Capacity")
    box2.pack(pady = 10, fill = "x")

    tk.Label(box2, text = "Debye Temperature (K)").pack()

    debye_temp = tk.Entry(box2)
    debye_temp.insert(0, "428")
    debye_temp.pack()

    tk.Button(box2, text = "RUN", command = heat_capacity_run).pack(pady = 3)
    tk.Button(box2, text = "CLEAR", command = heat_capacity_clear).pack()

    common = tk.LabelFrame(box2, text = "Common Debye Temperatures")
    common.pack(pady = 5, fill = "x")

    common_debye = [
        ("Material", "θD (K)"),
        ("Aluminium", 428),
        ("Beryllium", 1440),
        ("Cadmium", 209),
        ("Caesium", 38),
        ("Carbon (diamond)", 2230),
        ("Chromium", 630),
        ("Copper", 343),
        ("Germanium", 374),
        ("Gold", 170),
        ("Iron", 470),
        ("Lead", 105),
        ("Manganese", 410),
        ("Nickel", 450),
        ("Platinum", 240),
        ("Silicon", 645)
    ]

    for row, data in enumerate(common_debye):
        for col, value in enumerate(data):
            tk.Label(common, text = value).grid(row = row, column = col, padx = 5, sticky = "w")

    tk.Button(
        panel,
        text = "Back to Menu",
        command = window.destroy
    ).pack(side = "bottom", pady = 10, padx = 10, anchor = "w")