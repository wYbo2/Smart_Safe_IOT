from tkinter import *
import time

top=Tk() #create the root / base window

LED_off_img=PhotoImage(file="LED_off.gif") #images can be created using Paint etc.
LED_on_img=PhotoImage(file="LED_on.gif") #and added to the Python program this way

LED_state=False #a variable to store the LED state, initially False or "off"

def toggle_LED():
    global LED_state #to use the variable LED_state, declared before this function
    if LED_state==False: #toggle the LED state
        LED_state=True
        C.itemconfig(LED_img,image=LED_on_img) #change the LED image
    else:
        LED_state=False
        C.itemconfig(LED_img,image=LED_off_img)
    print("LED state is ",LED_state) #debug print
    top.after(100,toggle_LED) #schedule the function toggle_LED to execute
                                            #after 1000 ms


C=Canvas(top,width=64,height=128) #create a canvas, specifying the height & width
LED_img=C.create_image(0,0,image=LED_off_img,anchor=NW) #add the LED image to the canvas

C.pack() #put the canvas into the window
top.after(0,toggle_LED) #schedule the function toggle_LED to execute immediately
top.mainloop() #start the event loop

