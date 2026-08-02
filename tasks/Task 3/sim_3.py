import numpy as np
from scipy.integrate import quad

h = 6.626e-34  # Planck constant
c = 2.998e8  # speed of light
k_B = 1.381e-23  # Boltzmann constant
R = 8.314  # gas constant


#PHYSICAL MODELS

def black_body(lam, T):
    """Planck's black body spectral radiance."""
    return (2*h*c**2/lam**5)/(np.exp(h*c/(lam*k_B*T))-1)

def einstein(T, theta_E):
    """Einstein model of heat capacity."""
    x = theta_E/T
    return 3*R*(x**2*np.exp(x))/(np.exp(x)-1)**2

def debye(T, theta_D):
    """Debye model of heat capacity."""
    def f(x):
        """Debye integrand."""
        return x**4*np.exp(x)/(np.exp(x)-1)**2
    return np.array([9*R*(t/theta_D)**3*quad(f, 0, theta_D/t)[0] for t in T])

def limit():
    """Dulong-Petit high-temperature heat capacity limit."""
    return np.array([3*R for i in range(1000)])

#DATA GENERATION

def einstein_data(theta_D):
    """Get temperature and Einstein heat capacity data for a Debye temperature."""
    theta_E = 0.75 * theta_D
    T = np.linspace(1, 1000, 500)
    return T, einstein(T, theta_E)

def debye_data(theta):
    """Get temperature and Debye heat capacity data for a Debye temperature."""
    T = np.linspace(1, 1000, 500)
    return T, debye(T, theta)

def black_body_data(T):
    """Get wavelength and black body radiance data at temperature T."""
    lam = np.linspace(1e-7, 5e-6, 2000)
    return lam * 1e6, black_body(lam, T)