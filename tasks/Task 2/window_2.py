import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import sim_2 as sim

def open_window(window):

    #FUNCTIONS
    animation = None
    start_time = None

    def run():
        nonlocal animation, start_time
        start_time = time.time()
        animation = sim.BrownianSim(
            num_small = n_small.get(),
            large_mass = mass_ratio.get() * sim.m_air,
            small_radius = r_small.get(),
            large_radius = r_large.get(),
            box_size = limit.get())
        ax.clear()
        ax.set_xlim(-limit.get(), limit.get())
        ax.set_ylim(-limit.get(), limit.get())
        ax.set_xlabel("x/mm")
        ax.set_ylabel("y/mm")
        ax.set_aspect("equal")
        ax.set_title("Task 2")
        update()

    def update():
        if time.time() - start_time >= time_slider.get():
            return
        animation.update()
        ax.clear()
        ax.set_xlim(-limit.get(), limit.get())
        ax.set_ylim(-limit.get(), limit.get())
        ax.set_aspect("equal")
        ax.set_title("Brownian Motion")
        positions = animation.small_particle_positions()
        ax.scatter(positions[:, 0], positions[:, 1], s = np.pi*r_small.get()**2)
        x, y = animation.large_particle_circle()
        ax.plot(x, y, color = "red")
        ax.plot(animation.X, animation.Y, color = "orange")
        canvas.draw()
        window.after(10, update)

    def clear():
        ax.clear()
        ax.set_xlim(-limit.get(), limit.get())
        ax.set_ylim(-limit.get(), limit.get())
        ax.set_aspect("equal")
        ax.set_title("Brownian Motion")
        ax.set_xlabel("x/mm")
        ax.set_ylabel("y/mm")
        canvas.draw()

    #WINDOW
    window.title("Task 2")
    window.attributes("-fullscreen", True)

    fig = Figure(figsize = (8, 8))
    canvas = FigureCanvasTkAgg(fig, master = window)
    canvas.get_tk_widget().pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

    panel = tk.Frame(window)
    panel.pack(side = tk.LEFT, fill = tk.Y, padx = 10, pady = 10)

    #SIMULATION PARAMETERS
    ax = fig.add_subplot(111)
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    ax.set_aspect("equal")
    ax.set_title("Brownian Motion")

    box1 = tk.LabelFrame(panel, text = "Simulation Parameters")
    box1.pack(pady = 10, fill = "x")

    tk.Label(box1, text = "Number of Small Particles").pack()
    n_small = tk.Scale(box1, from_ = 100, to = 1000, orient = tk.HORIZONTAL)
    n_small.set(500)
    n_small.pack()

    tk.Label(box1, text = "Mass Ratio (Large/Small)").pack()
    mass_ratio = tk.Scale(box1, from_ = 1, to = 50, orient = tk.HORIZONTAL)
    mass_ratio.set(10)
    mass_ratio.pack()

    tk.Label(box1, text = "Small Particle Radius").pack()
    r_small = tk.Scale(box1, from_ = 0.1, to = 2, orient = tk.HORIZONTAL, resolution = 0.1)
    r_small.set(0.5)
    r_small.pack()

    tk.Label(box1, text = "Large Particle Radius").pack()
    r_large = tk.Scale(box1, from_ = 0.5, to = 5, orient = tk.HORIZONTAL, resolution = 0.1)
    r_large.set(2)
    r_large.pack()

    tk.Label(box1, text = "Boundary Limit").pack()
    limit = tk.Scale(box1, from_ = 10, to = 40, orient = tk.HORIZONTAL)
    limit.set(20)
    limit.pack()

    #ANIMATION CONTROLS
    box2 = tk.LabelFrame(panel, text = "Animation Controls")
    box2.pack(pady = 10, fill = "x")

    tk.Label(box2, text = "Total Time (s)").pack()
    time_slider = tk.Scale(box2, from_ = 1, to = 60, orient = tk.HORIZONTAL)
    time_slider.set(15)
    time_slider.pack()

    controls = tk.Frame(box2)
    controls.pack(pady = 5)
    tk.Button(controls, text = "RUN", command = run).pack(side = tk.LEFT, padx = 2)
    tk.Button(controls, text = "CLEAR", command = clear).pack(side = tk.LEFT, padx = 2)

    #BACK BUTTON
    tk.Button(panel, text = "Back to Menu", command = window.destroy).pack(side = "bottom", pady = 10, padx = 10, anchor = "w")