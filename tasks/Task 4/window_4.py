import tkinter as tk
from tkinter import ttk
import numpy as np
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sim_4 as sim
import data_4 as data

def open_window(window):

    #WINDOW
    window.title("Task 4")
    window.attributes("-fullscreen", True)

    fig = Figure(figsize=(12, 8), constrained_layout=True)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    panel = tk.Frame(window, width=250)
    panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    panel.pack_propagate(False)

    #GRAPH
    ax1 = fig.add_subplot(211)

    box1 = tk.LabelFrame(panel, text="Stopping Voltage Graph")
    box1.pack(pady=10, fill="x")

    tk.Label(box1, text="Metal").pack()
    metal_box = ttk.Combobox(box1, values=[m[0] for m in data.metal], state="readonly")
    metal_box.current(0)
    metal_box.pack()

    def draw_graph():
        ax1.clear()
        ax1.set_title("Photoelectron Stopping Voltage vs Frequency")
        ax1.set_xlabel("Frequency (10¹⁵ Hz)")
        ax1.set_ylabel("Stopping Voltage (V)")
        xlim, ylim = 3, 5
        ax1.set_xlim(0, xlim)
        ax1.set_ylim(-ylim, ylim)
    
        d = sim.metal_data(metal_box.current(), xlim, ylim)
        ax1.plot(d[0], d[1], "--", color="silver")
        ax1.plot(d[2], d[3], "-", color="silver")
        ax1.plot(d[4], d[5], "-.", color="silver")
    
        for f in data.frequencies:
            fx = f[2] / 1e15
            ax1.plot([fx, fx], [-ylim, ylim], color=f[0], linestyle=f[3])
        canvas.draw_idle()

    def clear_graph():
        ax1.clear()
        canvas.draw_idle()

    tk.Button(box1, text="RUN", command=draw_graph).pack(pady=3)
    tk.Button(box1, text="CLEAR", command=clear_graph).pack()

    #SIMULATION
    ax2 = fig.add_subplot(212)
    ax2.set_aspect("equal", adjustable="datalim")
    ax2.set_xticks([])
    ax2.set_yticks([])

    box2 = tk.LabelFrame(panel, text="Simulation")
    box2.pack(pady=10, fill="x")

    frequency = tk.Scale(box2, from_=0.5, to=2.0, resolution=0.01, label="Frequency (10^15 Hz)", orient=tk.HORIZONTAL)
    frequency.set(1.0)
    frequency.pack(fill="x")

    freq_buttons = tk.Frame(box2)
    freq_buttons.pack()

    def change_frequency(amount):
        value = frequency.get() + amount
        if 0.5 <= value <= 2.0:
            frequency.set(round(value, 2))
            update_display()

    tk.Button(freq_buttons, text="−", width=3, command=lambda: change_frequency(-0.05)).pack(side=tk.LEFT, padx=2)
    tk.Button(freq_buttons, text="+", width=3, command=lambda: change_frequency(0.05)).pack(side=tk.LEFT, padx=2)

    intensity = tk.Scale(box2, from_=0, to=100, label="Intensity (W/m²)", orient=tk.HORIZONTAL)
    intensity.set(50)
    intensity.pack(fill="x")

    voltage = tk.Scale(box2, from_=-10, to=10, resolution=0.1, label="Voltage (V)", orient=tk.HORIZONTAL)
    voltage.set(0)
    voltage.pack(fill="x")

    time_limit = tk.Scale(box2, from_=1, to=60, label="Time (s)", orient=tk.HORIZONTAL)
    time_limit.set(15)
    time_limit.pack(fill="x")

    buttons = tk.Frame(box2)
    buttons.pack()

    #STOPPING VOLTAGE CALCULATION
    box3 = tk.LabelFrame(panel, text="Stopping Voltage Calculation")
    box3.pack(pady=10, fill="x")

    calc_font = ("Segoe UI", 14, "bold")
    calc_colour = "black"

    tk.Label(box3, text="V₀ = hf/e − φ", font=calc_font, fg=calc_colour).pack(pady=(8, 4))
    plugin_label = tk.Label(box3, text="", font=calc_font, fg=calc_colour)
    plugin_label.pack(pady=2)
    answer_label = tk.Label(box3, text="", font=calc_font, fg=calc_colour, wraplength=210, justify="center")
    answer_label.pack(pady=(4, 10))

    #CURRENT
    box4 = tk.LabelFrame(panel, text="Current")
    box4.pack(pady=10, fill="x")

    current_label = tk.Label(box4, text="Current = 0.00000 A", font=calc_font, fg=calc_colour)
    current_label.pack(pady=10)

    #PLOT ELEMENTS
    cathode, = ax2.plot([0, 0], [0, 0.1], lw=5, color="silver")
    anode, = ax2.plot([0.2, 0.2], [0, 0.1], lw=5, color="black")
    particles = ax2.scatter([], [], color="blue")  # initial colour; will be updated per particle

    ax2.text(0, 0.11, "Cathode", ha="center", fontsize=9)
    ax2.text(0.2, 0.11, "Anode", ha="center", fontsize=9)
    cathode_sign = ax2.text(-0.015, 0.05, "−", ha="center", va="center", fontsize=14, color="silver")
    anode_sign = ax2.text(0.215, 0.05, "", ha="center", va="center", fontsize=14, color="black")

    light_ys = [0.01, 0.03, 0.05, 0.07, 0.09]
    light_arrows = []
    for ly in light_ys:
        arrow = ax2.annotate("", xy=(-0.004, ly), xytext=(-0.05, ly), arrowprops=dict(arrowstyle="->", color="gold"))
        light_arrows.append(arrow)

    light_text = ax2.text(-0.02, 0.096, "Light", ha="center", va="center", fontsize=9, color="goldenrod")

    #UPDATE DISPLAY
    def update_display(event=None):
        name, phi = data.metal[metal_box.current()][0], data.metal[metal_box.current()][1]
        f = frequency.get()
        photon_energy = sim.photon_energy_eV(f * 1e15)
        v_stop = sim.stopping_voltage(f * 1e15, phi)

        ax2.set_title(f"Photoelectric Effect Simulation — {name}, φ = {phi:.2f} eV")
        plugin_label.config(text=f"V₀ = {photon_energy:.2f} eV − {phi:.2f} eV")

        if v_stop < 0:
            answer_label.config(text="Not enough photon energy to overcome work function")
        else:
            answer_label.config(text=f"V₀ = {v_stop:.2f} V")

        wavelength = 3e8 / (f * 1e15) * 1e9
        colour = sim.wavelength_to_rgb(wavelength)
        for arrow in light_arrows:
            arrow.arrow_patch.set_color(colour)
        light_text.set_color(colour)

        v = voltage.get()
        anode_sign.set_text("+" if v > 0 else "−" if v < 0 else "")

        canvas.draw_idle()

    metal_box.bind("<<ComboboxSelected>>", update_display)
    frequency.config(command=update_display)
    voltage.config(command=update_display)
    update_display()

    #ANIMATION
    x = []
    y = []
    v = []
    colours = []          # stores a colour for each particle
    hits_total = 0
    time_elapsed = 0
    start_time = 0
    offsets = np.empty((0, 2))
    last_current = None

    def animate():
        nonlocal hits_total, time_elapsed, x, y, v, colours
        nonlocal offsets, last_current

        if time.perf_counter() - start_time >= time_limit.get():
            return

        # sim.update now returns updated colours list
        x, y, v, colours, hits_total, time_elapsed, current = sim.update(
            x, y, v, colours, voltage.get(), intensity.get(),
            data.metal[metal_box.current()][1], frequency.get() * 1e15,
            hits_total, time_elapsed
        )

        # Update particle positions
        if x:
            if offsets.shape[0] != len(x):
                offsets = np.empty((len(x), 2))
            offsets[:, 0] = x
            offsets[:, 1] = y
            particles.set_offsets(offsets)
            # Set colours for each particle (list of RGB tuples)
            particles.set_color(colours)
        else:
            particles.set_offsets(np.empty((0, 2)))

        # Update current display
        if last_current is None or abs(current - last_current) > 1e-5:
            current_label.config(text=f"Current = {current:.5f} A")
            last_current = current

        canvas.draw_idle()
        window.after(33, animate)

    def start():
        nonlocal start_time
        start_time = time.perf_counter()
        animate()

    def reset():
        nonlocal x, y, v, colours, hits_total, time_elapsed

        if time.perf_counter() - start_time < time_limit.get():
            return

        x.clear()
        y.clear()
        v.clear()
        colours.clear()
        hits_total = 0
        time_elapsed = 0
        particles.set_offsets(np.empty((0, 2)))
        current_label.config(text="Current = 0.00000 A")
        canvas.draw_idle()

    tk.Button(buttons, text="START", command=start).pack(side=tk.LEFT, padx=2)
    tk.Button(buttons, text="RESET", command=reset).pack(side=tk.LEFT, padx=2)

    #BACK BUTTON
    tk.Button(panel, text="Back to Menu", command=window.destroy).pack(side="bottom", pady=10, padx=10, anchor="w")

    draw_graph()
    canvas.draw()
    fig.set_layout_engine(None)