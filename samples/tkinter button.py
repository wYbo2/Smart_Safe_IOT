from tkinter import *

top=Tk() #create the root / base window

on_button_img=PhotoImage(file="on_button.gif") #images can be created using Paint etc.
off_button_img=PhotoImage(file="off_button.gif") #and added to the Python program this way

button_state=False #a variable to store the button state, initially False or "off"

def toggle_button():
    global button_state #to use the variable button_state, declared before this function
    if button_state==False: #toggle the button state
        button_state=True
        B.config(image=off_button_img) #change the button image
    else:
        button_state=False
        B.config(image=on_button_img)
    print("Button state is now",button_state) #debug print


B=Button(top,image=on_button_img,command=toggle_button) #create a button with image
                                       #with specifying a function to respond to a button click

B.pack() #put the button into the window
top.mainloop() #start the event loop
