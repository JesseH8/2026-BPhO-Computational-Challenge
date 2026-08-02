import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sim_6 as sim

def open_window(window):
    """Build and show the Task 6 electron diffraction window."""
    window.title("Task 6")
    window.attributes("-fullscreen", True)
    
    fig=Figure(figsize=(10,6),tight_layout=True)
    canvas=FigureCanvasTkAgg(fig,master=window)
    canvas.get_tk_widget().pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
    
    panel=tk.Frame(window,width=250) 
    panel.pack(side=tk.LEFT,fill=tk.Y,padx=10,pady=10)
    panel.pack_propagate(False)
    
    ax1=fig.add_subplot(121)
    ax2=fig.add_subplot(122)
    box=tk.LabelFrame(panel,text="Controls"); box.pack(fill="x")
    voltage=tk.Scale(box,from_=1000,to=5000,resolution=100,orient=tk.HORIZONTAL,label="Voltage (V)") 
    voltage.set(1000)
    voltage.pack(fill="x")
    
    highlight=tk.BooleanVar(master=window)
    tk.Checkbutton(box,text="Highlight maxima",variable=highlight).pack()
    
    def draw():
        """Recompute the diffraction pattern and graph, then redraw the canvas."""
        ax1.clear()
        ax2.clear()
        ax1.set_facecolor("black")
        ax1.set_aspect("equal")
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax1.set_title('Phosphore Screen Visualisation',fontsize=15)
        ax2.set_title(r'$1/\sqrt{V}$ vs $\sin(\phi/2)$',fontsize=15)
        ax2.set_xlabel(r'$\sin(\phi/2)$',fontsize=10)
        ax2.set_ylabel(r'$1/\sqrt{V}$',fontsize=10,labelpad=0)
        ax2.set_box_aspect(0.55)
        ax2.grid(alpha=0.3)
        
        x,xr,store=sim.maxima_radii(voltage.get())
        xc,yc,I=sim.circle_and_intensity(x,xr,highlight.get())
        
        for i in range(len(xc)): 
            ax1.plot(xc[i],yc[i],lw=0.05,color="lime",alpha=float(I[i]))
        
        X,Y=sim.plot_data(store)
        for i in range(len(X)): 
            ax2.plot(X[i],Y[i],label=f"d={store[i][0]*1e12:.0f}pm n={store[i][1]}")
        inv_sqrt_V = voltage.get()**-0.5
        ax2.plot([0,0.5], [inv_sqrt_V,inv_sqrt_V], color='gold')
        ax2.grid(alpha=0.3); ax2.legend(fontsize=5); canvas.draw_idle()
    
    tk.Button(box,text="RUN",command=draw).pack(fill="x")
    tk.Button(box,text="CLEAR",command=lambda:(ax1.clear(),ax2.clear(),canvas.draw_idle())).pack(fill="x")
    draw()
    
    #BACK BUTTON
    tk.Button(panel, text="Back to Menu", command=window.destroy).pack(side="bottom", pady=10, padx=10, anchor="w")