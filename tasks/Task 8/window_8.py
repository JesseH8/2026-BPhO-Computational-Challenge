import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sim_8 as sim

def open_window(window):
    
    window.title("Task 8")
    window.attributes("-fullscreen", True)

    fig=Figure(figsize=(10,6),tight_layout=True)
    canvas=FigureCanvasTkAgg(fig,master=window)
    canvas.get_tk_widget().pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
    
    panel=tk.Frame(window,width=250) 
    panel.pack(side=tk.LEFT,fill=tk.Y,padx=10,pady=10)
    panel.pack_propagate(False)
    
    ax1=fig.add_subplot(2,2,(1,2))
    ax2=fig.add_subplot(223)
    ax3=fig.add_subplot(224)
    
    relative_angles, quantum_p = sim.graph(np.linspace(0,180,1000))
    
    def update(value=None):
        ax1.clear()
        ax2.clear()
        ax3.clear()
        
        ax2.set_aspect('equal')
        ax3.set_aspect('equal')
        ax1.set_xlim(0, 180)
        ax1.set_ylim(0, 1)
        ax2.set_xlim(-1.2,1.2)
        ax2.set_ylim(-1.2,1.2)
        ax3.set_xlim(-1.2,1.2)
        ax3.set_ylim(-1.2,1.2)
        ax2.set_xticks([])
        ax3.set_xticks([])
        ax2.set_yticks([])
        ax3.set_yticks([])
        ax1.set_title('Probability of Mismatch vs Relative Angle')
        ax1.set_xlabel(r'$\theta - \phi$')
        ax1.set_ylabel('P(Mismatch)')
        ax2.set_title('Detector A')
        ax3.set_title('Detector B')
        
        classical_p1 = sim.classical_graph1(theta.get())
        classical_p2 = sim.classical_graph2(theta.get())
        ax1.plot(np.concatenate((relative_angles,np.flip(relative_angles))), 
                 np.concatenate((classical_p1,classical_p2)), 
                 color='blue',label='Classical')
        ax1.plot(relative_angles, quantum_p, color='red',label='Quantum')
        ax1.legend()
        
        relative_angle = np.absolute(theta.get()-phi.get())
        if relative_angle > 180:
            relative_angle = 360 - relative_angle
        ax1.plot([relative_angle,relative_angle],[0,1],color='gold')
        relative_angle, quantum_prob = sim.graph(relative_angle)
        classical_prob = sim.classical_mismatch_probability(theta.get(), phi.get())
        ax1.plot([0,relative_angle],[classical_prob,classical_prob],color='gold')
        ax1.plot([0,relative_angle],[quantum_prob,quantum_prob],color='gold')
        
        textstr = f'''Classical Mismatch Probability = {round(classical_prob,3)}
Quantum Mismatch Probability = {round(sim.quantum_mismatch_probability(theta.get(),phi.get()),3)}'''
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=10,verticalalignment='top', bbox=props)
        
        i_vector, j_vector = sim.basis_vectors(theta.get(), 1)
        ax2.annotate('', xytext=(0,0), xy=(i_vector[0],i_vector[1]),
                     arrowprops=dict(arrowstyle="->",edgecolor='green',facecolor='green'))
        ax2.annotate('', xytext=(0,0), xy=(j_vector[0],j_vector[1]),
                     arrowprops=dict(arrowstyle="->",edgecolor='green',facecolor='green'))
        am2 = sim.AngleAnnotation([0,0], i_vector, [0,1], ax=ax2, size=80, text=r"$\theta$", color="black")
        ax2.plot([0,0],[0,1],color='black',linestyle='--')
        
        i_vector, j_vector = sim.basis_vectors(phi.get(), 1)
        ax3.annotate('', xytext=(0,0), xy=(i_vector[0],i_vector[1]),
                     arrowprops=dict(arrowstyle="->",edgecolor='purple',facecolor='purple'))
        ax3.annotate('', xytext=(0,0), xy=(j_vector[0],j_vector[1]),
                     arrowprops=dict(arrowstyle="->",edgecolor='purple',facecolor='purple'))
        am3 = sim.AngleAnnotation([0,0], i_vector, [0,1], ax=ax3, size=80, text=r"$\phi$", color="black")
        ax3.plot([0,0],[0,1],color='black',linestyle='--')
        
        canvas.draw_idle()
        
    box=tk.LabelFrame(panel,text="Controls"); box.pack(fill="x")
    theta=tk.Scale(box,from_=0,to=360,resolution=1,orient=tk.HORIZONTAL,
                   label=r'θ in degrees',command=update)
    theta.set(90)
    theta.pack(fill='x')
    phi=tk.Scale(box,from_=0,to=360,resolution=1,orient=tk.HORIZONTAL,
                 label=r'φ in degrees',command=update) 
    phi.set(90)    
    phi.pack(fill='x')
    
    def clear():
        theta.set(90)
        phi.set(90)
        update()
    
    tk.Button(box,text="CLEAR",command=clear).pack(fill="x")
    
    update()
    
    
    #BACK BUTTON
    tk.Button(panel, text="Back to Menu", command=window.destroy).pack(side="bottom", pady=10, padx=10, anchor="w")