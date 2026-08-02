import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sim_1 as sim

colours = ["blue", "red", "green", "grey", "orange", "cyan", "magenta", "brown", "black", "purple"]

def open_window(window):
    # FUNCTIONS
    def dead_run():
        data = sim.generate(sim.create_particles(num_particles.get()), steps.get(), step_size.get())
        for i, ((x, y), r2) in enumerate(zip(data[0], data[1])):
            ax.plot(x, y, color = colours[i])
            ax.plot(x[-1], y[-1], 'o', color = colours[i], markersize = 8, markeredgecolor = "black")
            ax2.plot(range(len(r2)), r2, color = colours[i], alpha = 0.6)

        ax2.plot(range(steps.get()), [step_size.get()**2 * i for i in range(steps.get())],
                 color = "black", linestyle = "--", label = "Theory")
        ax2.legend(loc="upper left")  
        canvas.draw()

    def live_run():
        clear()
        data = sim.generate(sim.create_particles(num_particles.get()), steps.get(), step_size.get())

        def update(frame):
            ax.clear()
            ax2.clear()
            for i, ((x, y), r2) in enumerate(zip(data[0], data[1])):
                ax.plot(x[:frame + 1], y[:frame + 1], color = colours[i], alpha = 0.6)
                ax.plot(x[frame], y[frame], 'o', color = colours[i], markersize = 8, markeredgecolor = "black")
                ax2.plot(range(frame + 1), r2[:frame + 1], color = colours[i], alpha = 0.4)
            # Theory line – now with a label
            ax2.plot(range(frame + 1), [step_size.get()**2 * i for i in range(frame + 1)],
                     color = "black", linestyle = ":", label = "Theory")
            ax2.legend(loc="upper left")
            # Adjust axes limits
            current_x = []
            current_y = []
            for x, y in data[0]:
                current_x.extend(x[:frame + 1])
                current_y.extend(y[:frame + 1])
            max_x = max(abs(max(current_x)), abs(min(current_x)))
            max_y = max(abs(max(current_y)), abs(min(current_y)))
            size = max(max_x, max_y) * 1.1 + step_size.get()
            ax.set_xlim(-size, size)
            ax.set_ylim(-size, size)
            ax.set_aspect("equal")
            ax.set_xlabel("x displacement / m")
            ax.set_ylabel("y displacement / m")
            ax.set_title("Random walk")
            ax2.set_xlabel("Steps")
            ax2.set_ylabel("Squared Distance from Origin")
            ax2.set_title("Squared Distance from Origin vs Steps")
            canvas.draw()
            if frame < steps.get() - 1:
                window.after(1, update, frame + 1)

        update(0)

    def clear():
        ax.clear()
        ax2.clear()
        ax.set_aspect("equal")
        ax.set_xlabel("x displacement / m")
        ax.set_ylabel("y displacement / m")
        ax.set_title("Random walk")
        ax2.set_xlabel("Steps")
        ax2.set_ylabel("Squared displacement / m²")
        ax2.set_title("Squared Displacement vs Steps")
        # No legend here – will be added when new data is plotted
        canvas.draw()

    # WINDOW
    window.title("Task 1")
    window.attributes("-fullscreen", True)

    panel = tk.Frame(window)
    panel.pack(side = tk.LEFT, fill = tk.Y, padx = 10, pady = 10)

    # CONTROLS
    tk.Label(panel, text = "Num particles").pack()
    num_particles = tk.Scale(panel, from_ = 1, to = 10, orient = "horizontal")
    num_particles.set(3)
    num_particles.pack()

    tk.Label(panel, text = "Steps").pack()
    steps = tk.Scale(panel, from_ = 50, to = 5000, orient = "horizontal")
    steps.set(1000)
    steps.pack()

    tk.Label(panel, text = "Step size").pack()
    step_size = tk.Scale(panel, from_ = 0.1, to = 5, resolution = 0.1, orient = "horizontal")
    step_size.set(1.0)
    step_size.pack()

    tk.Button(panel, text = "LIVE RUN", width = 15, height = 2, command = live_run).pack(pady = 5)
    tk.Button(panel, text = "DEAD RUN", width = 15, height = 2, command = dead_run).pack(pady = 5)
    tk.Button(panel, text = "CLEAR", width = 15, height = 2, command = clear).pack()

    # PLOT
    fig = Figure(figsize = (7, 9))
    ax = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    fig.subplots_adjust(hspace = 0.35)
    ax.set_position([0.1, 0.35, 0.8, 0.55])
    ax2.set_position([0.1, 0.08, 0.8, 0.18])
    ax.set_aspect("equal")
    ax.set_xlabel("x displacement / m")
    ax.set_ylabel("y displacement / m")
    ax.set_title("Random walk")
    ax2.set_xlabel("Steps")
    ax2.set_ylabel("Squared displacement / m²")
    ax2.set_title("Squared Displacement vs Steps")

    canvas = FigureCanvasTkAgg(fig, master = window)
    canvas.get_tk_widget().pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)

    # BACK BUTTON
    tk.Button(panel, text = "Back to Menu", command = window.destroy).pack(side = "bottom", pady = 10, padx = 10, anchor = "w")