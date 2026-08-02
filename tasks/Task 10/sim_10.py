import numpy as np
from scipy.constants import physical_constants
from scipy.special import genlaguerre, factorial, sph_harm_y
from scipy.ndimage import map_coordinates
from skimage.measure import marching_cubes

from data_10 import orbital_map, electron_configurations, zeff

a0 = physical_constants["Bohr radius"][0]
angstrom = 1e-10
n_points = 70


def cart_to_sphere(x, y, z):
    """Converts cartesian to spherical coordinates."""
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(np.clip(z / (r + 1e-300), -1, 1))
    phi = np.arctan2(y, x)
    return r, theta, phi


def radial_wave(n, l, r, zeff):
    """Calculates the radial part of the wavefunction."""
    rho = (2 * zeff * r) / (n * a0)
    norm = (2 * zeff / (n * a0)) ** 1.5 * np.sqrt(factorial(n - l - 1) / (2 * n * factorial(n + l)))
    laguerre = genlaguerre(n - l - 1, 2 * l + 1)(rho)
    return norm * rho**l * np.exp(-rho / 2) * laguerre


def angular_wave(l, m, theta, phi):
    """Calculates the angular part of the wavefunction."""
    if m == 0:
        return sph_harm_y(l, 0, theta, phi).real
    elif m > 0:
        return np.sqrt(2) * (-1) ** m * sph_harm_y(l, m, theta, phi).real
    else:
        return np.sqrt(2) * (-1) ** m * sph_harm_y(l, -m, theta, phi).imag


def wavefunction(n, l, m, x, y, z, zeff):
    """Calculates the wavefunction at a set of points."""
    r, theta, phi = cart_to_sphere(x, y, z)
    return radial_wave(n, l, r, zeff) * angular_wave(l, m, theta, phi)


def probability_density(n, l, m, x, y, z, zeff):
    """Calculates the probability density at a set of points."""
    return wavefunction(n, l, m, x, y, z, zeff) ** 2


def atom_density(atom, x, y, z):
    """Calculates the total density for a multi-electron atom."""
    total = 0
    for orbital_name, num_electrons in electron_configurations[atom]:
        n, l, m = orbital_map[orbital_name]
        total += num_electrons * probability_density(n, l, m, x, y, z, zeff[atom])
    return total


def make_grid(limit, points):
    """Builds a square or cubic coordinate grid centred on the origin."""
    axis = np.linspace(-limit, limit, points)
    return axis


def orbital_slice(n, l, m, zeff, limit, z_offset=0):
    """Returns a 2D density slice of an orbital at a chosen z height."""
    axis = make_grid(limit, n_points * 2)
    X, Y = np.meshgrid(axis, axis)
    return X, Y, probability_density(n, l, m, X, Y, z_offset, zeff)


def atom_slice(atom, limit, z_offset=0):
    """Returns a 2D density slice of an atom at a chosen z height."""
    axis = make_grid(limit, n_points * 5)
    X, Y = np.meshgrid(axis, axis)
    return X, Y, atom_density(atom, X, Y, z_offset)


def orbital_volume(n, l, m, zeff, limit):
    """Returns a 3D density grid for an orbital."""
    axis = make_grid(limit, n_points)
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")
    return probability_density(n, l, m, X, Y, Z, zeff)


def orbital_wavefunction_volume(n, l, m, zeff, limit):
    """Returns a 3D wavefunction grid for an orbital, without squaring."""
    axis = make_grid(limit, n_points)
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")
    return wavefunction(n, l, m, X, Y, Z, zeff)


def atom_volume(atom, limit):
    """Returns a 3D density grid for an atom."""
    axis = make_grid(limit, n_points)
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")
    return atom_density(atom, X, Y, Z)


def marching_surface(density, limit, psi=None):
    """Extracts an isosurface mesh from a density grid, in Angstroms."""
    level = 0.10 * density.max()
    verts, faces, _, _ = marching_cubes(density, level=level)

    psi_vals = None
    if psi is not None:
        psi_vals = map_coordinates(psi, verts.T, order=1)

    spacing = (2 * limit) / (n_points - 1)
    verts = (verts * spacing - limit) / angstrom
    return verts, faces, psi_vals