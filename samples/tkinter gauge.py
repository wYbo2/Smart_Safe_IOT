from tkinter import *
from math import *

top=Tk() #create the root / base window

gauge_img=PhotoImage(file="gauge.gif") #images can be created using Paint etc.
                                        #and added to the Python program this way

lowest=0.0 #the lower limit
highest=100.0 #the upper limit
val=25.0 #the reading to display in gauge

start_x=128 #the pointer's centre
start_y=145
leng=100 #the pointer's length

angle=pi*(val-lowest)/(highest-lowest) #the pointer's angle, measure from 9 o'clock
end_x=start_x-leng*cos(angle) #calculate the pointer's end position
end_y=start_y-leng*sin(angle)

C=Canvas(top,width=256,height=256) #create a canvas, specifying the height & width
C.create_image(0,0,image=gauge_img,anchor=NW) #add the gauge image to the canvas 
C.create_line(start_x,start_y,end_x,end_y,fill="black",width=5) #add the pointer (a line) to the canvas 
C.create_text(50,start_y+10,font="Arial 10",text=lowest) #add the lower limit (a text) to the canvas
C.create_text(216,start_y+10,font="Arial 10",text=highest) #add the upper limit (a text) to the canvas
C.create_text(start_x,start_y+50,font="Arial 20",text=val) #add the reading (a text) to the canvas

C.pack() #put the canvas into the window
top.mainloop() #start the event loop
