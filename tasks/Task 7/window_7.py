import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sim_7 as sim

n_points = 500


def open_window(window):
    
    window.title("Task 7")
    window.attributes("-fullscreen", True)
    
    # Main frame
    main = tk.Frame(window)
    main.pack(fill="both", expand=True)
    
    # Control panel
    panel = tk.Frame(main)
    panel.pack(side="left", fill="y", padx=10, pady=10)
    
    # Graph area
    graphs_column = tk.Frame(main)
    graphs_column.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
    # Energy controls
    energy_controls = tk.LabelFrame(panel, text="Energy Levels", padx=10, pady=10)
    energy_controls.pack(pady=10, fill="x")
    tk.Label(energy_controls, text="Box Length (nm)").pack()
    energy_length_box = tk.Entry(energy_controls)
    energy_length_box.insert(0, "1")
    energy_length_box.pack(fill="x")
    tk.Label(energy_controls, text="Quantum Number n").pack()
    quantum_number_box = tk.Entry(energy_controls)
    quantum_number_box.insert(0, "6")
    quantum_number_box.pack(fill="x")
    
    # Probability controls
    prob_controls = tk.LabelFrame(panel, text="Probability Density", padx=10, pady=10)
    prob_controls.pack(pady=10, fill="x")
    tk.Label(prob_controls, text="Box Length (nm)").pack()
    prob_length_box = tk.Entry(prob_controls)
    prob_length_box.insert(0, "1")
    prob_length_box.pack(fill="x")
    tk.Label(prob_controls, text="Minimum Quantum Number").pack()
    n_min_box = tk.Entry(prob_controls)
    n_min_box.insert(0, "1")
    n_min_box.pack(fill="x")
    tk.Label(prob_controls, text="Maximum Quantum Number").pack()
    n_max_box = tk.Entry(prob_controls)
    n_max_box.insert(0, "3")
    n_max_box.pack(fill="x")
    
    # Graph figure
    fig = Figure(figsize=(8, 8))
    canvas = FigureCanvasTkAgg(fig, graphs_column)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Energy graph
    ax1 = fig.add_subplot(211)
    ax1.set_title("Energy Levels")
    
    # Probability graph
    ax2 = fig.add_subplot(212)
    ax2.set_title("Probability Density")
    
    def run_energy_plot():
        L = float(energy_length_box.get()) * 1e-9
        n_max = int(quantum_number_box.get())
        n, energy_eV, x, prob_density, delta_x, delta_p = sim.particle_box(L, n_max, n_points)
        ax1.plot(n, energy_eV, "o-", label=f"L={L * 1e9:.2g} nm")
        ax1.set_xlabel("Quantum number n")
        ax1.set_ylabel("Energy (eV)")
        ax1.set_title("Energy Levels")
        ax1.grid()
        ax1.legend()
        canvas.draw()
    
    def clear_energy_plot():
        ax1.clear()
        ax1.set_title("Energy Levels")
        canvas.draw()
    
    def run_probability_plot():
        L = float(prob_length_box.get()) * 1e-9
        n_min = int(n_min_box.get())
        n_max = int(n_max_box.get())
        if n_min > n_max:
            n_min, n_max = n_max, n_min
        n, energy_eV, x, prob_density, delta_x, delta_p = sim.particle_box(L, n_max, n_points)
        ax2.clear()
        for i, quantum_number in enumerate(n):
            if quantum_number >= n_min:
                ax2.plot(x * 1e9, prob_density[i], label=f"n={quantum_number}")
        ax2.set_xlabel("Position (nm)")
        ax2.set_ylabel(r"$|\psi|^2$")
        ax2.set_title("Probability Density")
        ax2.grid()
        ax2.legend()
        canvas.draw()
    
    def clear_probability_plot():
        ax2.clear()
        ax2.set_title("Probability Density")
        canvas.draw()
    
    # Energy buttons
    energy_run_button = tk.Button(energy_controls, text="Run", command=run_energy_plot)
    energy_run_button.pack(pady=(10, 0))
    energy_clear_button = tk.Button(energy_controls, text="Clear", command=clear_energy_plot)
    energy_clear_button.pack(pady=(5, 0))
    
    # Probability buttons
    prob_run_button = tk.Button(prob_controls, text="Run", command=run_probability_plot)
    prob_run_button.pack(pady=(10, 0))
    prob_clear_button = tk.Button(prob_controls, text="Clear", command=clear_probability_plot)
    prob_clear_button.pack(pady=(5, 0))
    
    # BACK BUTTON
    tk.Button(panel, text="Back to Menu", command=window.destroy).pack(side="bottom", pady=10, padx=10, anchor="w")