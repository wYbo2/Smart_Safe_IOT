from tkinter import *

top=Tk()

L1=Label(top,text='Height:')
L2=Label(top,text='Weight:')

E1=Entry(top,width=5)
E2=Entry(top,width=5)

CB1=Checkbutton(top,text='Keep aspect')

I=PhotoImage(file='dreamland.png')
C=Canvas(top,width=200,height=125)
C.create_image(0,0,image=I,anchor=NW)

B1=Button(top,text='Zoom in',width=8)
B2=Button(top,text='Zoom out',width=8)

L1.grid(row=0,column=0) #labels
L2.grid(row=1,column=0)

E1.grid(row=0,column=1) #entries
E2.grid(row=1,column=1)

CB1.grid(columnspan=2) #check button

C.grid(row=0,column=2,rowspan=2,columnspan=2) #canvas

B1.grid(row=2,column=2) #buttons
B2.grid(row=2,column=3)

top.mainloop()
