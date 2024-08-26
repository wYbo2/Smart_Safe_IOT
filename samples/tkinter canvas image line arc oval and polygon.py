from tkinter import *

top=Tk() #create the root / base window

C=Canvas(top,bg="light blue",height=500,width=600) #create a canvas, specifying the background color, height & width

filename=PhotoImage(file="pikachu.png") #images can be added to the Python program this way
I=C.create_image(40,40,anchor=NW,image=filename) #add the image to the canvas

L=C.create_line(400,40,400,360,fill="red") #add a line to the canvas

coord1=440,40,560,160 #boundary for the arc below
A=C.create_arc(coord1,start=30,extent=300,fill="yellow") #add an arc to the canvas, angle is measured from 3 o'clock

coord2=440,200,560,320 #boundary for the oval below
O=C.create_oval(coord2,fill="light green") #add an oval (actually a circle) to the canvas

P=C.create_polygon(440,360,480,360,560,460,520,460,440,360,fill="red") #add a polygon to the canvas

C.pack() #put the canvas into the window
top.mainloop() #start the event loop


