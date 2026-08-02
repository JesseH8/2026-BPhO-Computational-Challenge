import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASK_DIR = os.path.join(BASE_DIR, "tasks")
THUMBNAIL_DIR = os.path.dirname(os.path.abspath(__file__)) 

tasks = {
    1: ("Random Walk", "window_1"),
    2: ("Brownian Motion", "window_2"),
    3: ("Black Body Radiation", "window_3"),
    4: ("Photoelectric Effect", "window_4"),
    5: ("Hydrogen Emission Spectrum", "window_5"),
    6: ("Electron Diffraction", "window_6"),
    7: ("Particle in a Box", "window_7"),
    8: ("Classical vs Quantum Probability", "window_8"),
    9: ("Compton Scattering", "window_9"),
    10: ("Orbitals", "window_10")
}

def thumbnail_path(number):
    """Returns path to thumbnail_X.png for a given task number, or None if it doesn't exist."""
    path = os.path.join(THUMBNAIL_DIR, f"thumbnail_{number}.png")
    return path if os.path.exists(path) else None