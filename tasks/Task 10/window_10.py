import tkinter as tk
from tkinter import ttk
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

import sim_10 as sim
from data_10 import electron_configurations


def open_window(window):
    """Build and run the hydrogenic orbital / multi-electron atom viewer window."""

    # WINDOW
    window.title("Task 10")
    window.attributes("-fullscreen", True)

    main = tk.Frame(window)
    main.pack(fill="both", expand=True)

    controls = tk.Frame(main, width=320, padx=10, pady=10)
    controls.pack(side="left", fill="y")

    graphs = tk.Frame(main)
    graphs.pack(side="right", fill="both", expand=True)

    # SECTIONS
    mode_box = ttk.LabelFrame(controls, text="Mode", padding=10)
    mode_box.pack(fill="x", pady=5)

    hydrogenic_box = ttk.LabelFrame(controls, text="Hydrogenic Orbital (n, l, m, Z)", padding=10)
    hydrogenic_box.pack(fill="x", pady=5)

    atom_box = ttk.LabelFrame(controls, text="Multi-electron Atom", padding=10)
    atom_box.pack(fill="x", pady=5)

    button_box = ttk.LabelFrame(controls, text="Controls", padding=10)
    button_box.pack(fill="x", pady=5)

    colour_box = ttk.LabelFrame(button_box, text="Colour", padding=10)
    colour_box.pack(fill="x", pady=5)

    slice_box = ttk.LabelFrame(controls, text="Slice Plane", padding=10)
    slice_box.pack(fill="x", pady=5)

    # FIGURES
    fig3d = Figure(figsize=(7, 6))
    canvas3d = FigureCanvasTkAgg(fig3d, graphs)
    canvas3d.get_tk_widget().pack(side="left", fill="both", expand=True)

    fig2d = Figure(figsize=(6, 6))
    ax2d = fig2d.add_subplot(111)
    canvas2d = FigureCanvasTkAgg(fig2d, graphs)
    canvas2d.get_tk_widget().pack(side="right", fill="both", expand=True)

    # ax3d is rebuilt fresh from a cleared figure each run, which is the safe way to
    # get rid of any old colorbar without risking the removal error seen before.
    ax3d_ref = {"ax": fig3d.add_subplot(111, projection="3d")}

    # MODE

    mode = tk.StringVar(value = "Hydrogenic")
    mode_button = tk.IntVar(value = 0)

    def set_mode(value):
        mode.set(value)

    hydrogenic_radio = ttk.Radiobutton(mode_box, text="Hydrogenic Orbital", variable=mode_button, value=0, command=lambda: set_mode("Hydrogenic"))
    hydrogenic_radio.pack(anchor="w")

    atom_radio = ttk.Radiobutton(mode_box, text="Multi-electron Atom", variable=mode_button, value=1, command=lambda: set_mode("Atom"))
    atom_radio.pack(anchor="w")

    # COLOUR MODE

    colour_mode = tk.StringVar(value="z")
    colour_button = tk.IntVar(value=0)

    def set_colour_mode(value):
        colour_mode.set(value)

    z_colour_radio = ttk.Radiobutton(colour_box, text="Colour by z", variable=colour_button, value=0, command=lambda: set_colour_mode("z"))
    z_colour_radio.pack(anchor="w")

    phase_colour_radio = ttk.Radiobutton(colour_box, text="Colour by phase", variable=colour_button, value=1, command=lambda: set_colour_mode("phase"))
    phase_colour_radio.pack(anchor="w")

    # HYDROGENIC

    def update_l_slider(value):
         n = int(value)
         l_slider.config(to = n - 1)

         if l_slider.get() >= n:
             l_slider.set(n - 1)
         update_m_slider(l_slider.get())


    def update_m_slider(value):
         l = int(value)
         m_slider.config(from_ = -l,to = l)

         if m_slider.get() < -l:
             m_slider.set(-l)

         if m_slider.get() > l:
             m_slider.set(l)

    tk.Label(hydrogenic_box, text="Principal Quantum Number (n)").pack(anchor="w")
    n_slider = tk.Scale(hydrogenic_box, from_=1, to=4, orient="horizontal")
    n_slider.pack(fill="x")
    n_slider.config(command=update_l_slider)
    n_slider.set(2)

    tk.Label(hydrogenic_box, text="Angular Momentum (l)").pack(anchor="w")
    l_slider = tk.Scale(hydrogenic_box, from_=0, to=3, orient="horizontal")
    l_slider.pack(fill="x")
    l_slider.config(command=update_m_slider)

    tk.Label(hydrogenic_box, text="Magnetic Quantum Number (m)").pack(anchor="w")
    m_slider = tk.Scale(hydrogenic_box, from_=-3, to=3, orient="horizontal")
    m_slider.pack(fill="x")

    tk.Label(hydrogenic_box, text="Nuclear Charge (Z)").pack(anchor="w")
    z_slider = tk.Scale(hydrogenic_box, from_=1, to=10, resolution=1, orient="horizontal")
    z_slider.pack(fill="x")
    z_slider.set(1)

    # ATOM
    tk.Label(atom_box, text="Atom").pack(anchor="w")
    atom_combobox = ttk.Combobox(atom_box, values=list(electron_configurations.keys()), state="readonly")
    atom_combobox.current(0)
    atom_combobox.pack(fill="x")

    # SLICE PLANE
    tk.Label(slice_box, text="Slice Height (z, Å)").pack(anchor="w")
    slice_slider = tk.Scale(slice_box, from_=-10, to=10, resolution=0.1, orient="horizontal")
    slice_slider.pack(fill="x")
    slice_slider.set(0)

    # Remembers the last full Run so the slider can re-slice without recomputing the isosurface.
    current = {}
    # Tracks the plane artist on ax3d so the old one can be removed before drawing a new one.
    plane_ref = {"artist": None}


    # FUNCTIONS
    def run():
        """Compute the selected orbital or atom density and redraw both plots."""
        fig3d.clf()
        ax3d = fig3d.add_subplot(111, projection="3d")
        ax3d_ref["ax"] = ax3d
        ax2d.clear()

        want_phase = mode.get() == "Hydrogenic" and colour_mode.get() == "phase"

        if mode.get() == "Hydrogenic":
            n, l, m, z = n_slider.get(), l_slider.get(), m_slider.get(), z_slider.get()
            limit = 8 * (n**2) * sim.a0 / z
            density = sim.orbital_volume(n, l, m, z, limit)
            psi = sim.orbital_wavefunction_volume(n, l, m, z, limit) if want_phase else None
        else:
            atom = atom_combobox.get()
            limit = 10 * sim.a0
            density = sim.atom_volume(atom, limit)
            psi = None

        verts, faces, psi_vals = sim.marching_surface(density, limit, psi)
        max_extent = np.max(np.abs(verts))

        if psi_vals is not None:
            # Colour by the sign of psi: red for positive phase, blue for negative phase.
            # Average the raw psi value per face first, then take its sign, so a face
            # can't land on an ambiguous blended colour at a node boundary.
            face_psi = psi_vals[faces].mean(axis=1)
            face_phase = np.where(face_psi >= 0, 1, -1)

            phase_cmap = ListedColormap(["royalblue", "crimson"])
            surf = ax3d.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], triangles=faces, cmap=phase_cmap, linewidth=0, antialiased=False, alpha=0.75)
            surf.set_array(face_phase)
            surf.set_clim(-1, 1)

            legend_handles = [Patch(facecolor="crimson", label="Positive phase"), Patch(facecolor="royalblue", label="Negative phase")]
            ax3d.legend(handles=legend_handles, loc="upper right")

        elif colour_mode.get() == "phase":
            # Phase colouring was requested but isn't available for a multi-electron atom.
            ax3d.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], triangles=faces, linewidth=0.2, alpha=0.75)

        else:
            # Colour by |z| / max extent so the top and bottom lobes match, symmetric
            # about z=0, with the equator lightest.
            z_fraction = np.abs(verts[:, 2]) / max_extent
            face_colour = z_fraction[faces].mean(axis=1)

            surf = ax3d.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], triangles=faces, cmap="RdBu", linewidth=0, antialiased=True, shade=True)
            surf.set_array(face_colour)
            surf.set_clim(0, 1)

            cbar = fig3d.colorbar(surf, ax=ax3d, shrink=0.6, pad=0.1)
            cbar.set_label("|z| / max extent")

        ax3d.set_title("Probability Density Isosurface")
        ax3d.set_xlim(-max_extent, max_extent)
        ax3d.set_ylim(-max_extent, max_extent)
        ax3d.set_zlim(-max_extent, max_extent)
        ax3d.set_xlabel("x (Å)")
        ax3d.set_ylabel("y (Å)")
        ax3d.set_zlabel("z (Å)")
        ax3d.set_box_aspect([1, 1, 1])

        slice_limit = max_extent * sim.angstrom
        current.clear()
        current.update({
            "mode": mode.get(),
            "n": n if mode.get() == "Hydrogenic" else None,
            "l": l if mode.get() == "Hydrogenic" else None,
            "m": m if mode.get() == "Hydrogenic" else None,
            "z": z if mode.get() == "Hydrogenic" else None,
            "atom": atom if mode.get() == "Atom" else None,
            "slice_limit": slice_limit,
            "max_extent": max_extent,
        })

        slice_slider.config(from_=-max_extent, to=max_extent)
        slice_slider.set(0)
        plane_ref["artist"] = None
        update_slice()

        canvas3d.draw()



    def update_slice(_event=None):
        """Redraws the 2D slice and the 3D plane marker at the slider's current height."""
        if not current:
            return

        height = slice_slider.get()
        z_offset = height * sim.angstrom

        if current["mode"] == "Hydrogenic":
            X2, Y2, density2 = sim.orbital_slice(current["n"], current["l"], current["m"], current["z"], current["slice_limit"], z_offset)
        else:
            X2, Y2, density2 = sim.atom_slice(current["atom"], current["slice_limit"], z_offset)

        extent = current["max_extent"]
        ax2d.clear()
        ax2d.imshow(density2, origin="lower", extent=[-extent, extent, -extent, extent])
        ax2d.set_title(f"Density Slice (z = {height:.1f} Å)")
        ax2d.set_xlabel("x (Å)")
        ax2d.set_ylabel("y (Å)")

        ax3d = ax3d_ref["ax"]
        if plane_ref["artist"] is not None:
            plane_ref["artist"].remove()

        grid = np.linspace(-extent, extent, 2)
        Xp, Yp = np.meshgrid(grid, grid)
        Zp = np.full_like(Xp, height)
        plane_ref["artist"] = ax3d.plot_surface(Xp, Yp, Zp, color="gray", alpha=0.25, linewidth=0)

        canvas2d.draw()
        canvas3d.draw()

    slice_slider.config(command=update_slice)



    def clear():
        """Reset both plots to a blank state."""
        fig3d.clf()
        ax3d_ref["ax"] = fig3d.add_subplot(111, projection="3d")
        ax2d.clear()
        current.clear()
        plane_ref["artist"] = None
        canvas3d.draw()
        canvas2d.draw()


    # BUTTONS
    run_button = tk.Button(button_box, text="Run", width=12, height=2, command=run)
    run_button.pack(fill="x", pady=5)

    clear_button = tk.Button(button_box, text="Clear", width=12, height=2, command=clear)
    clear_button.pack(fill="x", pady=5)

    hydrogenic_radio.invoke()
    z_colour_radio.invoke()

    #BACK BUTTON
    tk.Button(controls, text = "Back to Menu", command = window.destroy).pack(side = "bottom", pady = 10, padx = 10, anchor = "w")