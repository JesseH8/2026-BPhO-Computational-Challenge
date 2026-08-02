import numpy as np
from matplotlib import cm
import data_4 as data

# CONSTANTS
A = 0.01
e_eq = 2e8
dt = 5e-9


# STOPPING VOLTAGE GRAPH DATA

def metal_data(index, x_limit, y_limit):
    """Line segments for the stopping-voltage plot of a metal."""
    W = data.metal[index][1]
    cutoff = W*data.e/data.h*10**-15
    return [0, cutoff], [-W, 0], [cutoff, x_limit], [0, data.h*x_limit*10**15/data.e - W], [cutoff, cutoff], [-y_limit, y_limit]


def EM_freq_data(index, y_limit):
    """Vertical line marking the selected EM source's frequency."""
    return [data.frequencies[index][2], data.frequencies[index][2]], [-y_limit, y_limit]


# PHOTOELECTRON SIMULATION

class Electron:
    """A single emitted electron with position, velocity, and colour."""

    def __init__(self, frequency, W):
        """Sets initial position, velocity, and colour from the emitting frequency."""
        self.x = 0
        self.y = np.random.uniform(0, 0.1)
        self.W = W + np.random.uniform(0, 1)
        energy = data.h*frequency - self.W*data.e
        self.v = np.sqrt(2*energy/data.m) if energy > 0 else 0
        wavelength = 3e8/frequency*1e9
        self.colour = wavelength_to_rgb(wavelength)


def update(x, y, v, colour, V, intensity, W, frequency, hits_total, time_elapsed):
    """Advances electrons one timestep, spawns new ones, and updates current."""
    acceleration = data.e*V/(data.m*data.d)
    hits = 0
    for i in range(len(x)-1, -1, -1):
        if x[i] >= data.d:
            hits += 1
            x.pop(i); y.pop(i); v.pop(i); colour.pop(i)
        else:
            x[i] += v[i]*dt + 0.5*acceleration*dt**2
            v[i] += acceleration*dt
            if x[i] < 0:
                x.pop(i); y.pop(i); v.pop(i); colour.pop(i)
    electrons = round(dt*intensity*A/(data.h*frequency*e_eq))
    for i in range(electrons):
        particle = Electron(frequency, W)
        if particle.v > 0:
            x.append(particle.x); y.append(particle.y); v.append(particle.v); colour.append(particle.colour)
    hits_total += hits
    time_elapsed += dt
    current = hits*e_eq*data.e/dt if time_elapsed else 0
    return x, y, v, colour, hits_total, time_elapsed, current


def photon_energy_eV(frequency_hz):
    """Photon energy in eV for a given frequency."""
    return data.h*frequency_hz/data.e


def stopping_voltage(frequency_hz, work_function_eV):
    """Stopping voltage for a given frequency and work function."""
    return photon_energy_eV(frequency_hz) - work_function_eV


def wavelength_to_rgb(wavelength):
    """Converts a wavelength in nm to an approximate RGBA colour."""
    rgb = [np.interp(wavelength, data.wavelength_points, data.wavelength_colours[:, i]) for i in range(3)]
    return (*rgb, 1)