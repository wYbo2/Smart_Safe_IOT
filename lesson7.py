from tkinter import *
 
top = Tk()

on_button_img = PhotoImage(file="on_button.gif")
off_button_img = PhotoImage(file="off_button.gif")

button_state = False
def toggle_button():
    global button_state
    if button_state== False:
        button_state = True
        B.config(image=off_button_img)
    else:
        button_state=False
        B.config(image=on_button_img)
    print("Button state is now", button_state)

B = Button(top, image= on_button_img, command=toggle_button)
B.pack()
top.mainloop()
