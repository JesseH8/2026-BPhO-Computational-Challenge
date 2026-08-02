# constants
h = 6.63e-34
c = 3.00e8
eV = 1.60e-19


#UNIT CONVERSIONS

def wavelength(photon_energy):
    """Converts a photon energy in eV to a wavelength in nm."""
    energy_joules = photon_energy * eV
    return (h * c / energy_joules) * 1e9


def frequency(photon_energy):
    """Converts a photon energy in eV to a frequency in Hz."""
    energy_joules = photon_energy * eV
    return energy_joules / h

#ENERGY LEVELS

def energy_level(n, Z = 1):
    """Energy of a hydrogen-like atom at level n."""
    return -13.6 * Z**2 / n**2


def transition_energy(n_initial, n_final, Z = 1):
    """Energy released dropping from n_initial to n_final."""
    initial = energy_level(n_initial, Z)
    final = energy_level(n_final, Z)
    return initial - final

#SPECTRAL DATA

def spectrum_data(max_level):
    """Wavelengths and energies of all transitions, grouped by series."""
    series = {
        "Lyman Series": (1, [], []),
        "Balmer Series": (2, [], []),
        "Paschen Series": (3, [], []),
        "Brackett Series": (4, [], []),
        "Pfund Series": (5, [], []),   
        "Humphreys Series": (6, [], [])}
    
    for initial in range(2, max_level + 1):
        for final in range(1, initial):
            energy = transition_energy(initial, final)
            wave = wavelength(energy)
            if final in [1, 2, 3, 4]:
                name = get_series(final)
                series[name][1].append(wave)
                series[name][2].append(energy)
    return series

def transition(initial_level, final_level):
    """Energy, wavelength, frequency, and series name for a transition."""
    energy = transition_energy(initial_level, final_level)
    wave = wavelength(energy)
    freq = frequency(energy)
    series = get_series(final_level)
    return energy, wave, freq, series

def possible_transitions(max_level, Z = 1):
    """All transitions down to each level up to max_level."""
    transitions = []
    for initial in range(2, max_level + 1):
        for final in range(1, initial):
            energy = transition_energy(initial, final, Z)
            wave = wavelength(energy)
            transitions.append([initial, final, energy, wave])
    return transitions

def get_series(final_level):
    """Name of the spectral series for a given final level."""
    match final_level:
        case 1:
            return "Lyman Series"
        case 2:
            return "Balmer Series"
        case 3:
            return "Paschen Series"
        case 4:
            return "Brackett Series"
        case 5:
            return "Pfund Series"
        case 6:
            return "Humphreys Series"
        case _:
            return "Unknown Series"