import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import *
import psutil
import numpy as np
import networkx as nx

'''
We configure a Tkinter window, and the associated objects required to draw the network and graph.
'''
root = Tk()
defaultFont = tk.font.nametofont('TkDefaultFont')
frame= Frame(root).pack(fill= BOTH, padx= 0, pady=0)
root.title("Contact process")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
fig = plt.figure(frameon=True, figsize=(screen_width/100,screen_height/100), dpi=102)
canvas = FigureCanvasTkAgg(fig, root)

'''
Keybinds:
button_0    :   Display a graph that shows the number of infection over time.
scroll      :   Increase/decrease the rate of infection.
F11         :   Toggle fullscreen.
'''
root.bind("<F11>", lambda e: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Button-1>", lambda event: globals().__setitem__('display_infections', not display_infections))
root.bind("<MouseWheel>", lambda event: globals().__setitem__('r', max(0, r + 0.1 if event.delta > 0 else r - 0.1)))

'''
Main variables:
G                   :   The graph on which we run the contact process.
dt                  :   The timestep in ms at which we update the graph.
T                   :   The final time in ms the simulation
r                   :   The initial infection rate per second
display_infection   :   Bool that determines whether or not a graph is displayed that shows recent infections.
inf                 :   A list of infected nodes
inf_count           :   Stores the number of infected nodes at each timestep
'''
scale = 35
G = nx.grid_2d_graph((int)(screen_height/scale), (int)(screen_width/scale)) 
dt, T, r = 500, 1000000, 0.5
global display_infections; display_infections = False
inf = {list(G)[i] : 1 for i in range(len(list(G)))}
pos = {(x,y):(y,-x) for x,y in G.nodes()}
inf_count = []

def generate_poisson_events(rate, time_duration):
    '''
    rate            :   The rate of the Poisson process
    time_duration   :   The time interval in which to generate events.
    Runs the poisson process and returns the time of the last hit. If not hits occur, returns -1.
    '''
    num_events = np.random.poisson(rate * time_duration)
    event_times = np.sort(np.random.uniform(0, time_duration, num_events))
    if num_events > 0:
       return np.max(event_times)
    return -1

def contact_process(graph, dt, rate):
    '''
    graph     :   The graph on which we do the contact process
    dt        :   The simulation timestep
    rate      :   The rate of the contact process
    Updates the inf array to represent the contact process and append the number of infection at this time to inf_count
    '''
    for i in graph.nodes():
        recov_time = generate_poisson_events(1/1000, dt)
        inf_time = -1
        for j in nx.all_neighbors(graph, i):
            if inf[j] == 1:
                inf_time = max(inf_time, generate_poisson_events(rate/1000, dt))
        if inf_time >= 0 or recov_time >= 0:
            inf[i] = 0 if recov_time > inf_time else 1
    inf_count.append(sum(1 for value in inf.values() if value == 1))

'''Generates colours for networkx to draw infected nodes red, and healthy ones blue'''
def generate_colour_map(inf):
    return ['#BF211E' if value == 1 else '#1f77b4' for value in inf.values()]


def timeStep(current_time):
    '''
    current_time    :   The time at which we want to display the contact process
    This function clears the previous figure does the following three things
    1.  Draw a label that show the current rate
    2.  Draw G
    3.  If display_infections is true, draw a graph that shows the number of infections
    '''
    plt.clf()
    r_label = Label(root, text=f"Rate (λ): {r:.2f}", font=("Open Sans", 36), fg="black", bg="white", bd=5, relief="solid")
    r_label.place(relx=0.5, rely=0.03, anchor="n")
    r_label.config(text=f"Rate (λ): {r:.2f}")
    
    col = generate_colour_map(inf)
    ax = plt.gca() 
    ax.set_xlim([min(x for x, y in pos.values()) + 1, max(x for x, y in pos.values()) - 1])
    ax.set_ylim([min(y for x, y in pos.values()) + 1, max(y for x, y in pos.values()) - 1])
    ax.set_axis_off() 
    nx.draw(G, pos, ax=ax, node_size=screen_width/(0.1*scale), node_color=col, with_labels=False, edgecolors='black', linewidths=1.5, node_shape='s')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0) 

    if(display_infections):
        plt.subplot(1, 2, 1, facecolor=(1, 1, 1, 0.8))
        plt.plot(inf_count[max(0, len(inf_count) - 100): len(inf_count) - 1],linewidth=5)
        plt.ylim(0, len(G.nodes()))
        plt.xlabel("time (ms)", labelpad=-35, loc='center', fontsize=18), plt.ylabel("infections", labelpad=-35, loc='center', fontsize=18)
        plt.title("Infected sites over time", pad=-20, loc='center', y=0.95, fontsize=36)
        plt.gca().tick_params(labelsize=0)  
        for spine in plt.gca().spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(5)

    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

'''
Main loop:
Runs the contact and visualises the contact process until time T.
'''
for i in range((int)(T/dt)):
    if not (1 in inf.values()):
        break
    root.update_idletasks()
    root.update()
    contact_process(G, dt, r)
    root.after(0, timeStep(i*dt))
root.mainloop()