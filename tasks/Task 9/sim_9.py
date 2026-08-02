import numpy as np

h = 6.62607015e-34
c = 299792458
m_e = 9.1093837e-31
e = 1.602e-19


#UNIT CONVERSIONS

def joules(E):
    """Converts an energy in eV to joules."""
    return E * e


def wavelength_0(photon_E):
    """Incident photon wavelength from its energy."""
    return (h * c) / photon_E


def wavelength_fin(photon_E, theta, electron_E, electron_angle):
    """Scattered photon wavelength from its energy."""
    return (h * c) / photon_energy_final(photon_E, theta, electron_E, electron_angle)


#ELECTRON KINEMATICS

def electron_momentum(electron_E):
    """Relativistic momentum of the electron from its kinetic energy."""
    total_energy = electron_E + m_e * c**2
    return np.sqrt(total_energy**2 - (m_e * c**2)**2) / c


def electron_components(electron_E, electron_angle):
    """x and y momentum components of the electron."""
    momentum = electron_momentum(electron_E)
    px = momentum * np.cos(electron_angle)
    py = momentum * np.sin(electron_angle)
    return px, py


#COMPTON SCATTERING

def photon_energy_final(photon_E, theta, electron_E, electron_angle):
    """Scattered photon energy from conservation of energy and momentum."""
    Ee_tot = electron_E + m_e * c**2
    p_e = electron_momentum(electron_E)
    Qx = p_e * c * np.cos(electron_angle)
    Qy = p_e * c * np.sin(electron_angle)
    numerator = photon_E * (Ee_tot - Qx)
    denominator = Ee_tot - Qx * np.cos(theta) - Qy * np.sin(theta) + photon_E * (1 - np.cos(theta))
    return numerator / denominator


def compton_shift(photon_E, theta, electron_E, electron_angle):
    """Change in photon wavelength due to scattering."""
    return wavelength_fin(photon_E, theta, electron_E, electron_angle) - wavelength_0(photon_E)


def fractional_shift(photon_E, theta, electron_E, electron_angle):
    """Compton shift as a fraction of the initial wavelength."""
    return compton_shift(photon_E, theta, electron_E, electron_angle) / wavelength_0(photon_E)


#RECOIL

def recoil_energy(photon_E, theta, electron_E, electron_angle):
    """Kinetic energy of the recoiling electron after scattering."""
    initial_photon = photon_E
    final_photon = photon_energy_final(photon_E, theta, electron_E, electron_angle)
    initial_electron = electron_E + m_e * c**2
    final_electron = initial_photon + initial_electron - final_photon
    return final_electron - m_e * c**2


def recoil_speed(photon_E, theta, electron_E, electron_angle):
    """Speed of the recoiling electron after scattering."""
    K = recoil_energy(photon_E, theta, electron_E, electron_angle)
    gamma = 1 + K / (m_e * c**2)
    return c * np.sqrt(1 - 1 / gamma**2)


def recoil_angle(photon_E, theta, electron_E, electron_angle):
    """Direction of the recoiling electron after scattering."""
    photon_p_initial = h / wavelength_0(photon_E)
    photon_p_final = photon_energy_final(photon_E, theta, electron_E, electron_angle) / c
    electron_px, electron_py = electron_components(electron_E, electron_angle)
    px = photon_p_initial + electron_px - photon_p_final * np.cos(theta)
    py = electron_py - photon_p_final * np.sin(theta)
    return np.arctan2(py, px)


#DATA GENERATION

def compton_data(photon_E, electron_E, electron_angle):
    """Fractional shift, recoil speed, and recoil angle across scattering angles."""
    theta = np.linspace(0.001, np.pi, 500)
    shift = fractional_shift(photon_E, theta, electron_E, electron_angle)
    speed = recoil_speed(photon_E, theta, electron_E, electron_angle)
    angle = recoil_angle(photon_E, theta, electron_E, electron_angle)
    
    return theta, shift, speed, angle