import numpy as np

# PHYSICAL CONSTANTS
h = 6.626e-34
hbar = h / (2 * np.pi)
e_m = 9.11e-31
ev = 1.602e-19


def particle_box(L=1e-9, n_max=6, n_points=500):
    """Energy levels, wavefunctions, and uncertainties for a particle in a box."""
    n = np.arange(1, n_max + 1)
    
    energy_eV = n**2 * h**2 / (8 * e_m * L**2) / ev
    
    x = np.linspace(0, L, n_points)
    psi = np.array([np.sqrt(2 / L) * np.sin(k * np.pi * x / L) for k in n])
    prob_density = psi**2
    
    delta_x = L * np.sqrt(1/12 - 1 / (2 * (n * np.pi)**2))
    
    delta_p = n * np.pi * hbar / L
    return n, energy_eV, x, prob_density, delta_x, delta_p
