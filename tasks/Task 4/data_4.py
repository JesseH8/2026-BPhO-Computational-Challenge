import numpy as np

# PHYSICAL CONSTANTS
m = 9.109e-31    # electron mass (kg)
e = 1.602e-19    # elementary charge (C)
h = 6.626e-34    # Planck constant (J s)
d = 0.2          # plate separation (m)
dt = 5e-9        # simulation timestep (s)

# METALS: (name, work function in eV)
# METALS: (name, work function in eV)
# METALS: (name, work function in eV)
metal = [
    ("Caesium", 2.14),
    ("Sodium", 2.28),
    ("Calcium", 2.87),
    ("Aluminium", 4.08),
    ("Zinc", 4.33),
    ("Iron", 4.50),
    ("Copper", 4.70),
    ("Silver", 4.73),
    ("Gold", 5.10),
    ("Nickel", 5.15),
    ("Platinum", 6.35),
]

# EM SOURCES: (colour, wavelength in nm, frequency in Hz, linestyle)
frequencies = [
    ("violet", 400, 7.50e14, "-"),
    ("blue",   450, 6.67e14, "--"),
    ("cyan",   495, 6.06e14, "-."),
    ("green",  530, 5.66e14, ":"),
    ("gold",   580, 5.17e14, "-"),
    ("orange", 620, 4.84e14, "--"),
    ("red",    700, 4.28e14, "-."),
    ("purple", 300, 1.00e15, ":"),
]

# WAVELENGTH-TO-COLOUR MAPPING (nm -> RGB)
wavelength_points = np.array([200, 300, 380, 450, 495, 570, 590, 620, 750])
wavelength_colours = np.array([
    [0.4, 0.0, 0.5],   # UV
    [0.5, 0.0, 1.0],   # near UV
    [0.56, 0.0, 1.0],  # violet
    [0.0, 0.0, 1.0],   # blue
    [0.0, 1.0, 1.0],   # cyan
    [0.0, 1.0, 0.0],   # green
    [1.0, 1.0, 0.0],   # yellow
    [1.0, 0.5, 0.0],   # orange
    [1.0, 0.0, 0.0],   # red
])