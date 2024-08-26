from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                             #this allows a MatPlotLib graph to be added to a TKinter frame -- NEW!!
import matplotlib.pyplot as plt

top=Tk()

#the following lines of code plot a line graph...
readings=[5,6,1,3,8,9,3,5]
entries=[1,2,3,4,5,6,7,8]
my_figure=plt.figure()
my_graph=my_figure.add_subplot(1,1,1) #add graph to figure
my_graph.plot(entries,readings)
my_graph.set_xlabel('1-sec sampling',fontsize=10)
my_graph.set_ylabel('sensor values',fontsize=10)
my_graph.set_title('Matplotlib graph in TKinter')

my_canvas=FigureCanvasTkAgg(my_figure,master=top) #add figure to canvas -- NEW!!
my_canvas._tkcanvas.pack() #use this special "pack ()", to add canvas to top frame -- NEW!!

#the following lines of code add a toggle button
button_state=False
def toggle_button():
    global button_state
    if button_state==False:
        button_state=True
        my_button.config(text="Turn Off")
    else:
        button_state=False
        my_button.config(text="Turn On")

my_button=Button(top,text="Turn On",command=toggle_button)
my_button.pack() #use the usual "pack ()", to add button to top frame

top.mainloop()

