from tkinter import*

top = Tk()
C= Canvas(top, bg="light yellow",height=500, width=600)

filename = PhotoImage(file="pikachu.png")
I=C.create_image(40,40, anchor=NW, image=filename)
L=C.create_line(400, 40, 400, 360, fill="red")

coord1= 440, 40, 560, 160
A= C.create_arc(coord1, start=30, extent=300, fill="black")

coord2 = 440, 200, 560, 320
O= C.create_oval(coord2, fill="light green")

P=C.create_polygon(440,360,480,360,560,460,520,460,440,360, fill="red")

C.pack()
top.mainloop()

