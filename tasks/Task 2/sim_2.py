import numpy as np

# Physical constants
m_air = (28.97e-3) / (6.022e23)
C = 1
kn = 15
small_speed = 500 / 1000


class Particle:
    """A single particle with position, velocity, mass, and radius."""

    def __init__(self, x, y, vx, vy, m, r):
        """Set up the particle's initial state."""
        self.x = np.array(x, dtype=float)
        self.y = np.array(y, dtype=float)
        self.vx = np.array(vx, dtype=float)
        self.vy = np.array(vy, dtype=float)
        self.m = m
        self.r = r

    def move(self, dt):
        """Advance the particle's position by one timestep."""
        self.x += self.vx * dt
        self.y += self.vy * dt


class BrownianSim:
    """Simulates Brownian motion of a large particle among many small particles."""

    circle_angles = np.linspace(0, 2 * np.pi, 100)

    def __init__(self, num_small, large_mass, small_radius, large_radius, box_size):
        """Set up the simulation parameters and create the particles."""
        self.t = 0
        self.T = 0

        self.N = num_small
        self.m = m_air
        self.M = large_mass

        self.r = small_radius
        self.R = large_radius

        self.v = small_speed * np.random.uniform(0.5, 1.5)
        self.V = 0

        self.C = C
        self.Kn = kn

        self.dt = 0.05 * self.Kn * self.r / self.v
        self.a = box_size

        self.X = [0]
        self.Y = [0]

        self.large_particle = self.create_large_particle()
        self.small_particles = self.create_small_particles()

    #PARTICLE SETUP

    def random_v(self, v):
        """Pick a random velocity direction at speed v."""
        theta = np.random.uniform(0, 2 * np.pi)
        return v * np.cos(theta), v * np.sin(theta)

    def create_large_particle(self):
        """Create the large particle at the centre of the box."""
        return Particle(0, 0, *self.random_v(self.V),
                        self.M, self.R)

    def create_small_particles(self):
        """Scatter small particles randomly, avoiding the large particle."""
        particles = []
        while len(particles) < self.N:
            x_random = np.random.uniform(-self.a, self.a)
            y_random = np.random.uniform(-self.a, self.a)
            if (x_random ** 2 + y_random ** 2) > (self.R + self.r) ** 2:
                particles.append(Particle(x_random, y_random,
                                          *self.random_v(self.v),
                                          self.m, self.r))
        return particles

    #SIMULATION STEP

    def update(self):
        """Advance the simulation by one timestep."""
        self.t += self.dt
        self.T += self.dt

        self.large_particle.move(self.dt)
        self.wall_collision(self.large_particle)

        for particle in self.small_particles:
            particle.move(self.dt)
            self.wall_collision(particle)
            self.collision(self.large_particle, particle)

        self.X.append(self.large_particle.x)
        self.Y.append(self.large_particle.y)

        if self.T > (self.Kn * self.r / self.v):
            self.T = 0
            for particle in self.small_particles:
                particle.vx, particle.vy = self.random_v(self.v)

    #COLLISION HANDLING

    def collision(self, large_particle, small_particle):
        """Resolve an elastic collision between the large and a small particle."""
        u = np.array([small_particle.vx, small_particle.vy])
        U = np.array([large_particle.vx, large_particle.vy])

        d = np.sqrt((small_particle.x - large_particle.x) ** 2 +
                    (small_particle.y - large_particle.y) ** 2)

        if d == 0:
            return

        dhat = np.array([small_particle.x - large_particle.x,
                         small_particle.y - large_particle.y]) / d

        if d <= small_particle.r + large_particle.r:
            overlap = (small_particle.r + large_particle.r - d) / 2

            r1 = [large_particle.x, large_particle.y] - overlap * dhat
            r2 = [small_particle.x, small_particle.y] + overlap * dhat

            large_particle.x = r1[0]
            large_particle.y = r1[1]
            small_particle.x = r2[0]
            small_particle.y = r2[1]

            if np.dot(u - U, dhat) < 0:
                V = (large_particle.m * U + small_particle.m * u) / (large_particle.m + small_particle.m)
                large_particle.vx, large_particle.vy = V - self.C * (U - V)
                small_particle.vx, small_particle.vy = V - self.C * (u - V)

    def wall_collision(self, particle):
        """Bounce a particle off the box walls."""
        if particle.x > self.a - particle.r:
            particle.x = self.a - particle.r
            particle.vx *= -1

        if particle.x < -self.a + particle.r:
            particle.x = -self.a + particle.r
            particle.vx *= -1

        if particle.y > self.a - particle.r:
            particle.y = self.a - particle.r
            particle.vy *= -1

        if particle.y < -self.a + particle.r:
            particle.y = -self.a + particle.r
            particle.vy *= -1

    #DATA ACCESS

    def small_particle_positions(self):
        """Get the x/y positions of all small particles."""
        return np.array([[particle.x, particle.y] for particle in self.small_particles])

    def large_particle_circle(self):
        """Get the x/y coordinates outlining the large particle's circle."""
        x = self.large_particle.x + self.large_particle.r * np.cos(self.circle_angles)
        y = self.large_particle.y + self.large_particle.r * np.sin(self.circle_angles)
        return x, y