import numpy as np


class Particle:
    """Particle with position and trace history."""

    def __init__(self):
        """Initialises the particle at the origin."""
        self.x = 0
        self.y = 0
        self.x_trace = [0]
        self.y_trace = [0]
        self.r2_trace = [0]


def create_particles(num_particles):
    """Make a list of new particles."""
    return [Particle() for i in range(num_particles)]


def walk(particles, step_size):
    """Move each particle one random step."""
    for p in particles:
        direction = np.random.uniform(0, 2*np.pi)

        p.x += step_size*np.cos(direction)
        p.y += step_size*np.sin(direction)

        p.x_trace.append(p.x)
        p.y_trace.append(p.y)

        r = p.x**2 + p.y**2
        p.r2_trace.append(r)

    return particles


def position_data(particles):
    """Get x/y trace tuples for each particle."""
    return [(p.x_trace, p.y_trace) for p in particles]


def r2_data(particles):
    """Get distance from origin history for each particle."""
    return [p.r2_trace for p in particles]


def generate(particles, steps, step_size):
    """Run the walk for several steps."""
    for i in range(steps):
        walk(particles, step_size)

    return position_data(particles), r2_data(particles)


# SIMULATION CONTROL

def reset_sim(num_particles):
    """Start a fresh simulation."""
    return create_particles(num_particles)