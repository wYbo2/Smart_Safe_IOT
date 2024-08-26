from tkinter import *
from tkinter import messagebox

top=Tk() #create the root / base window

def respond_to_click():
    messagebox.showinfo("My message box","My message") #use a message box to display a message

B=Button(top,text="Click me!",command=respond_to_click) #create a button with text
                                       #with specifying a function to respond to a button click

B.pack() #put the button into the window
top.mainloop() #start the event loop
