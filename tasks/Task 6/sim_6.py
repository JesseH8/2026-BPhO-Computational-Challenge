import numpy as np

d = [123e-12,213e-12] #Atomic spacings in m
r = 0.065 #Radius of glass sphere with the phosphor screen in m
m = 9.109e-31 #Mass of an electron in kg
h = 6.626e-34 #Planck's constant
e = 1.602e-19 #charge of an electron /C


def maxima_radii(V):
    """Radii of the diffraction maxima on the phosphor screen at voltage V."""
    x_centre = list(np.linspace(0,0.01,100)) 
    x = [] 
    x_real = [[0,0.00001,'N/A']]
    for i in range(len(x_centre)):
        x.append([x_centre[i],0.01*i])
        
    maxima_for_graph = [] 
    
    for i in range(len(d)):
        n = 1 
        flag = True 
        while flag:
            #Redundancy for arcsin
            arg = n*h/(2*d[i]*(2*m*e*V)**0.5)
            if np.absolute(arg) > 1: 
                flag = False
                break
            
            
            X = r*np.sin(2*np.arcsin(arg))
            
            
            maxima_for_graph.append([d[i],n])
            
            #Raise flag if radius is beyond average phosphore screen
            if X > r*70/100: 
                flag = False
            else:
                
                x.append([X,n])
                x_real.append([X,n,d[i]])
                n += 1
    
    
    x.sort(key=lambda item: item[0])
    x_real.sort(key=lambda item: item[0])
    
    return x,x_real,maxima_for_graph


def circle_and_intensity(x,x_real,highlight):
    """Circle coordinates and intensities making up the diffraction pattern image."""
    theta = np.linspace(0,2*np.pi,100)
    intensity = []
    x_circle = []
    y_circle = []
    
    #Split phosphore screen into 2000 circles which differ in intensities
    R = np.linspace(0,r,2000)
    nearest_x = x[0][0]
    x_index = 0
    
    #To flag when the last radius is reached
    x_last_index = len(x_real)-1
    last_index = False
    for i in range(len(R)):
        if not last_index and np.absolute(nearest_x - R[i]) > np.absolute(x_real[x_index+1][0] - R[i]):
            x_index += 1
            nearest_x = x_real[x_index][0]
            if x_index == x_last_index:
                last_index = True
        
        #Calculate intensity and plot
        intensity_ = 0
        for j in range(len(x_real)):
            intensity_ += 1/(1+72*np.absolute(x_real[j][0]-R[i])+x_real[j][1])**2.5
        intensity_ = np.tanh(intensity_)
        
        #If on maxima, draw another circle with higher intensity to highlight max
        if np.absolute(R[i] - nearest_x) < 0.0001 and highlight:
            intensity_ = 1/(1+x_real[x_index][1])
        
        x_circle.append(R[i]*np.cos(theta))
        y_circle.append(R[i]*np.sin(theta))
        intensity.append(intensity_)
        
    return x_circle, y_circle, intensity


def plot_data(maxima_for_graph):
    """1/sqrt(V) and diffraction angle data for each maxima at two voltages."""
    voltage = [1e3,5e3]
    x = []
    y = []
    for i in range(len(maxima_for_graph)):
        a = []
        b = []
        for j in range(len(voltage)):
            A = 1/(voltage[j])**0.5
            B = maxima_for_graph[i][1]*h/(2*maxima_for_graph[i][0]*(2*m*e*voltage[j])**0.5)
            
            a.append(A)
            b.append(B)
        x.append(b)
        y.append(a)
    return x,y