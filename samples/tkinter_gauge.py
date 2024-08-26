from tkinter import*
from math import *

top = Tk()
gauge_img = PhotoImage(file="gauge.gif")

lowest = 0.0
highest = 100.0
val = 25.0

start_x = 128
start_y = 145
leng = 100

angle = pi*(val-lowest)/(highest-lowest)
end_x = start_x-leng*cos(angle)
end_y= start_y-leng*sin(angle)

C = Canvas(top, width=256, height=256)
C.create_image(0,0, image=gauge_img, anchor=NW)
C.create_line(start_x, start_y, end_x, end_y, fill="black", width=5)
C.create_text(50, start_y+10, font="Arial 10", text=lowest)
C.create_text(216, start_y+10, font="Arial 10", text=highest)
C.create_text(start_x, start_y+50, font="Arial 20", text=val)

C.pack()
top.mainloop()

