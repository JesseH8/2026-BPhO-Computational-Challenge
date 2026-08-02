import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from matplotlib.transforms import IdentityTransform


#MISMATCH PROBABILITIES

def classical_mismatch_probability(theta,phi):
    """Classical prediction for polarizer mismatch probability."""
    theta = np.deg2rad(theta)
    phi = np.deg2rad(phi)
    return (1-np.cos(theta)**2*np.cos(phi)**2-np.sin(theta)**2*np.sin(phi)**2)


def quantum_mismatch_probability(theta,phi):
    """Quantum prediction for polarizer mismatch probability."""
    theta = np.deg2rad(theta)
    phi = np.deg2rad(phi)
    return (np.sin(theta-phi)**2) #phi and theta are interchangeable


def basis_vectors(angle, magnitude):
    """Perpendicular i/j basis vectors at a given angle."""
    angle = np.deg2rad(angle)
    i_vector = [magnitude*np.sin(angle),magnitude*np.cos(angle)]
    j_vector = [magnitude*np.sin(angle-np.pi/2),magnitude*np.cos(angle-np.pi/2)]
    return i_vector,j_vector


#GRAPH DATA

def graph(relative_angle):
    """Quantum mismatch probability as a function of relative angle."""
    theta = relative_angle/2
    phi = -relative_angle/2
    quantum_p = quantum_mismatch_probability(theta, phi)
    return relative_angle, quantum_p


def classical_graph1(theta):
    """Classical mismatch probability as phi sweeps upward from theta."""
    phi = np.linspace(theta, theta + 180, 1000)
    classical_p = classical_mismatch_probability(theta,phi)
    return classical_p


def classical_graph2(theta):
    """Classical mismatch probability as phi sweeps downward from theta."""
    phi = np.linspace(theta, theta - 180, 1000)
    classical_p = np.flip(classical_mismatch_probability(theta,phi))
    return classical_p


#Class found on matplotlib for labelling angles
class AngleAnnotation(Arc):
    """Draws an arc and places a text label centered inside an angle."""
    def __init__(self, xy, p1, p2, size=75, unit="points", ax=None, text="", textposition="inside", text_kw=None, **kwargs):
        """Sets up the arc and its text label."""
        self.ax = ax or plt.gca()
        self._xy = xy
        self.p1 = p1
        self.p2 = p2
        self.size = size
        self.unit = unit
        self.textposition = textposition
        
        # Initialize the arc base class
        super().__init__(xy, 1, 1, angle=0, theta1=0, theta2=0, **kwargs)
        self.set_transform(IdentityTransform())
        self.ax.add_patch(self)
        
        # Set up text label options
        kw = dict(horizontalalignment="center", verticalalignment="center")
        if text_kw is not None:
            kw.update(text_kw)
        self.text = self.ax.text(0, 0, text, **kw)

    def get_transform(self):
        """Gets the arc's display transform."""
        return super().get_transform()

    def draw(self, renderer):
        """Redraws the arc and label, updating for the current view."""
        # Automatically updates angles and handles window rescaling
        self._update_arc()
        super().draw(renderer)
        self._update_text()
        self.text.draw(renderer)

    def _update_arc(self):
        """Recomputes the arc's angles and size from data coordinates."""
        # Convert coordinates from data space to screen display pixel space
        tr = self.ax.transData
        xy = tr.transform(self._xy)
        p1 = tr.transform(self.p1)
        p2 = tr.transform(self.p2)
        
        # Calculate angles relative to the screen plane
        a1 = np.arctan2(*(p1 - xy)[::-1])
        a2 = np.arctan2(*(p2 - xy)[::-1])
        if a2 < a1:
            a2 += 2 * np.pi
            
        self.theta1 = np.degrees(a1)
        self.theta2 = np.degrees(a2)
        self.center = xy
        self.width = self.height = self.size

    def _update_text(self):
        """Recenters the text label on the current arc."""
        # Places text perfectly in the middle of the generated arc
        a = np.deg2rad((self.theta1 + self.theta2) / 2)
        r = self.size / 2
        if self.textposition == "outside":
            r += 10
        dx, dy = r * np.cos(a), r * np.sin(a)
        x, y = self.center + np.array([dx, dy])
        self.text.set_position(self.ax.transData.inverted().transform((x, y)))