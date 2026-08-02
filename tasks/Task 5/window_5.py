import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sim_5 as sim

series_colors = {
    "Lyman Series": "orange",
    "Balmer Series": "red",
    "Paschen Series": "blue",
    "Brackett Series": "green",
    "Pfund Series": "black",
    "Humphreys Series": "cyan"
}

def open_window(window):

    #FUNCTIONS
    plotted_series = set()

    def run():
        initial = int(initial_level.get())
        final = int(final_level.get())
        energy, wave, freq, series = sim.transition(initial, final)
        color = series_colors.get(series, "gray")
        label = series if series not in plotted_series else None
        plotted_series.add(series)
        ax.vlines(wave, 0, energy, color = color, linestyle = ":", linewidth = 1, label = label)
        ax.plot(wave, energy, marker = "*", color = color, markersize = 4)
        ax.set_title("Bohr's model of Hydrogenic atom /n Z = 1")
        ax.set_xlabel(r"$\lambda$ /nm")
        ax.set_ylabel("Photon energy /eV")
        ax.grid(axis = "y", linestyle = ":")
        ax.legend()
        canvas.draw()

    def run_all():
        start = int(initial_level.get())
        end = int(final_level.get())
    
        original_start = initial_level.get()
        original_end = final_level.get()
    
        if start > end:
            start, end = end, start
    
        for i in range(end, start, -1):
            for j in range(i - 1, start - 1, -1):
                initial_level.delete(0, "end")
                initial_level.insert(0, str(i))
                final_level.delete(0, "end")
                final_level.insert(0, str(j))
                run()
    
        initial_level.delete(0, "end")
        initial_level.insert(0, original_start)
        final_level.delete(0, "end")
        final_level.insert(0, original_end)

    def clear():
        plotted_series.clear()
        ax.clear()
        ax.set_title("Bohr's model of Hydrogenic atom/n Z = 1")
        ax.set_xlabel(r"$\lambda$ /nm")
        ax.set_ylabel("Photon energy /eV")
        ax.grid(axis = "y", linestyle = ":")
        canvas.draw()

    #WINDOW
    window.title("Task 5")
    window.attributes("-fullscreen", True)

    left = tk.Frame(window)
    left.pack(side = "left", fill = "y")
    right = tk.Frame(window)
    right.pack(side = "right", expand = True, fill = "both")

    #SIMULATION CONTROLS
    simulation = tk.LabelFrame(left, text = "Simulation")
    simulation.pack(fill = "x", padx = 5, pady = 5)

    tk.Label(simulation, text = "Initial Level").pack()
    initial_level = tk.Entry(simulation)
    initial_level.insert(0, "2")
    initial_level.pack()

    tk.Label(simulation, text = "Final Level").pack()
    final_level = tk.Entry(simulation)
    final_level.insert(0, "1")
    final_level.pack()

    button_frame = tk.Frame(simulation)
    button_frame.pack()
    tk.Button(button_frame, text = "RUN", command = run).pack(side = "left", padx = 5)
    tk.Button(button_frame, text = "RUN ALL", command = run_all).pack(side = "left", padx = 5)
    tk.Button(button_frame, text = "CLEAR", command = clear).pack()

    #SERIES REFERENCE TABLE
    series_frame = tk.Frame(simulation)
    series_frame.pack(pady = 10)

    tk.Label(series_frame, text = "Series").grid(row = 0, column = 0)
    tk.Label(series_frame, text = "Final Level").grid(row = 0, column = 1)

    tk.Label(series_frame, text = "Lyman").grid(row = 1, column = 0)
    tk.Label(series_frame, text = "n → 1").grid(row = 1, column = 1)

    tk.Label(series_frame, text = "Balmer").grid(row = 2, column = 0)
    tk.Label(series_frame, text = "n → 2").grid(row = 2, column = 1)

    tk.Label(series_frame, text = "Paschen").grid(row = 3, column = 0)
    tk.Label(series_frame, text = "n → 3").grid(row = 3, column = 1)

    tk.Label(series_frame, text = "Brackett").grid(row = 4, column = 0)
    tk.Label(series_frame, text = "n → 4").grid(row = 4, column = 1)

    tk.Label(series_frame, text = "Pfund").grid(row = 5, column = 0)
    tk.Label(series_frame, text = "n → 5").grid(row = 5, column = 1)

    tk.Label(series_frame, text = "Humphreys").grid(row = 6, column = 0)
    tk.Label(series_frame, text = "n → 6").grid(row = 6, column = 1)

    #PLOT
    fig = Figure()
    ax = fig.add_subplot()
    ax.set_title("Hydrogen Emission Spectrum")
    ax.set_xlabel("Wavelength / nm")
    ax.set_ylabel("Photon Energy / eV")

    canvas = FigureCanvasTkAgg(fig, right)
    canvas.get_tk_widget().pack(expand = True, fill = "both")
    
    #BACK BUTTON
    tk.Button(left, text = "Back to Menu", command = window.destroy).pack(side = "bottom", pady = 10, padx = 10, anchor = "w")