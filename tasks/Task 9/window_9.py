import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sim_9 as sim

colours = [
    "blue",
    "red",
    "green",
    "purple",
    "orange",
    "black"
]

run_number = 0


def open_window(window):

    window.title("Task 9")
    window.attributes("-fullscreen", True)

    # MAIN LAYOUT
    main = tk.Frame(window)
    main.pack(fill="both", expand=True)

    panel = tk.Frame(main, width=300)
    panel.pack(side="left", fill="y", padx=10, pady=10)

    graph_frame = tk.Frame(main)
    graph_frame.pack(side="right", fill="both", expand=True)

    # PHOTON BOX
    photon_box = tk.LabelFrame(panel, text="Photon", padx=10, pady=10)
    photon_box.pack(fill="x", pady=5)

    tk.Label(photon_box, text="Photon Energy (keV)").pack()
    photon_entry = tk.Entry(photon_box)
    photon_entry.insert(0, "100")
    photon_entry.pack(pady=5)

    # ELECTRON BOX
    electron_box = tk.LabelFrame(panel, text="Electron", padx=10, pady=10)
    electron_box.pack(fill="x", pady=5)

    tk.Label(electron_box, text="Initial Electron Energy (keV)").pack()
    electron_entry = tk.Entry(electron_box)
    electron_entry.insert(0, "0")
    electron_entry.pack(pady=5)

    tk.Label(electron_box, text="Initial Electron Angle (degrees)").pack()
    electron_angle_slider = tk.Scale(electron_box, from_=0, to=360, orient="horizontal", length=220)
    electron_angle_slider.set(0)
    electron_angle_slider.pack(pady=5)

    # SIMULATION BOX
    simulation_box = tk.LabelFrame(panel, text="Simulation", padx=10, pady=10)
    simulation_box.pack(fill="x", pady=5)

    run_button = tk.Button(simulation_box, text="Run", width=15)
    run_button.pack(pady=5)

    clear_button = tk.Button(simulation_box, text="Clear", width=15)
    clear_button.pack(pady=5)

    # LEGEND BOX
    legend_box = tk.LabelFrame(panel, text="Legend", padx=10, pady=10)
    legend_box.pack(fill="x", pady=5)

    legend_frame = tk.Frame(legend_box)
    legend_frame.pack()

    # GRAPHS
    fig = Figure(figsize=(10, 18))

    ax1 = fig.add_subplot(311)
    ax1.set_title("Fractional Wavelength Shift vs Photon Scattering Angle")
    ax1.set_xlabel("Photon Scattering Angle θ (degrees)")
    ax1.set_ylabel("Δλ / λ")
    ax1.grid()

    ax2 = fig.add_subplot(312)
    ax2.set_title("Electron Recoil Speed vs Photon Scattering Angle")
    ax2.set_xlabel("Photon Scattering Angle θ (degrees)")
    ax2.set_ylabel("Electron Speed v (m/s)")
    ax2.grid()

    ax3 = fig.add_subplot(313)
    ax3.set_title("Electron Recoil Angle vs Photon Scattering Angle")
    ax3.set_xlabel("Photon Scattering Angle θ (degrees)")
    ax3.set_ylabel("Electron Recoil Angle φ (degrees)")
    ax3.grid()

    fig.subplots_adjust(hspace=0.45, top=0.97, bottom=0.03)

    canvas = FigureCanvasTkAgg(fig, graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # FUNCTIONS
    global run_number

    def run_sim():
        global run_number
        
        photon_E = sim.joules(float(photon_entry.get()) * 1e3)
        electron_E = sim.joules(float(electron_entry.get()) * 1e3)
        electron_angle = np.radians(electron_angle_slider.get())
        
        theta, shift, speed, angle = sim.compton_data(photon_E, electron_E, electron_angle)
        theta = np.degrees(theta)
        angle = np.degrees(angle)
        
        colour = colours[run_number % len(colours)]
        ax1.plot(theta, shift, color=colour)
        ax2.plot(theta, speed, color=colour)
        ax3.plot(theta, angle, color=colour)
        
        label = f"Photon {photon_entry.get()} keV, Electron KE {electron_entry.get()} keV, Angle {electron_angle_slider.get()}°"
        legend_label = tk.Label(legend_frame, text=label, fg=colour, anchor="w")
        legend_label.pack(fill="x")
        run_number += 1
        
        ax1.set_title("Fractional Wavelength Shift vs Photon Scattering Angle")
        ax1.set_xlabel("Photon Scattering Angle θ (degrees)")
        ax1.set_ylabel("Δλ / λ")
        ax1.grid()
        ax2.set_title("Electron Recoil Speed vs Photon Scattering Angle")
        ax2.set_xlabel("Photon Scattering Angle θ (degrees)")
        ax2.set_ylabel("Electron Speed v (m/s)")
        ax2.grid()
        ax3.set_title("Electron Recoil Angle vs Photon Scattering Angle")
        ax3.set_xlabel("Photon Scattering Angle θ (degrees)")
        ax3.set_ylabel("Electron Recoil Angle φ (degrees)")
        ax3.grid()
        canvas.draw()

    def clear_sim():
        global run_number

        ax1.clear()
        ax2.clear()
        ax3.clear()

        for widget in legend_frame.winfo_children():
            widget.destroy()

        run_number = 0

        ax1.set_title("Fractional Wavelength Shift vs Photon Scattering Angle")
        ax1.set_xlabel("Photon Scattering Angle θ (degrees)")
        ax1.set_ylabel("Δλ / λ")
        ax1.grid()

        ax2.set_title("Electron Recoil Speed vs Photon Scattering Angle")
        ax2.set_xlabel("Photon Scattering Angle θ (degrees)")
        ax2.set_ylabel("Electron Speed v (m/s)")
        ax2.grid()

        ax3.set_title("Electron Recoil Angle vs Photon Scattering Angle")
        ax3.set_xlabel("Photon Scattering Angle θ (degrees)")
        ax3.set_ylabel("Electron Recoil Angle φ (degrees)")
        ax3.grid()

        canvas.draw()

    run_button.config(command=run_sim)
    clear_button.config(command=clear_sim)

    # BACK BUTTON
    tk.Button(panel, text="Back to Menu", command=window.destroy).pack(side="bottom", pady=10, padx=10, anchor="w")