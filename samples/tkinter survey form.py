from tkinter import *
from tkinter import messagebox

top=Tk()

instr=Label(top,text="Fill in details required and click submit:")
instr.pack(anchor=W,pady=5) #align to the left, with 5 pixels padding above & below

name=Label(top,text="Name:")
name.pack(anchor=W,pady=5)

v1=StringVar()
name_entry=Entry(top,bd=5,textvariable=v1) #5-pixel border, & the entry will be stored into v1, a string variable
name_entry.pack(anchor=W,padx=15,pady=5) #15-pixel indentation from left

gender=Label(top,text="Gender:")
gender.pack(anchor=W,pady=5)

v2=IntVar()
male=Radiobutton(top,text="male",variable=v2,value=1) #v2=1 if male selected
male.pack(anchor=W,padx=15,pady=1)
female=Radiobutton(top,text="female",variable=v2,value=2) #v2=2 if female selected
female.pack(anchor=W,padx=15,pady=1)

age=Label(top,text="Age range:")
age.pack(anchor=W,pady=5)

age_listbox=Listbox(top,width=5,height=4,bd=5,selectmode=SINGLE) #the width & height are in terms of number of characters
                                                                    #SINGLE means only one item can be selected
for item in ["13-18","19-30","31-50","> 50"]: #use a for loop to add all items in the list to the list box
    age_listbox.insert(END,item)
age_listbox.pack(anchor=W,padx=15,pady=5)

hobbies=Label(top,text="Hobbies(choose 1 or more):")
hobbies.pack(anchor=W,pady=5)

v4=IntVar()
v5=IntVar()
v6=IntVar()
book=Checkbutton(top,text="Book ",variable=v4,onvalue=1,offvalue=0,height=2,width=5) #v4=1 if "Book " selected, 0 otherwise
music=Checkbutton(top,text="Music",variable=v5,onvalue=1,offvalue=0,height=2,width=5) #similarly v5 for Music
movie=Checkbutton(top,text="Movie",variable=v6,onvalue=1,offvalue=0,height=2,width=5) #and v6 for Movie
book.pack(anchor=W,padx=15,pady=1)
music.pack(anchor=W,padx=15,pady=1)
movie.pack(anchor=W,padx=15,pady=1)

def on_submit():
    print("v1=",v1.get(),"  <- name") #the entry, radio buttons selection, list box selection, check buttons selection are displayed
    print("v2=",v2.get(),"  <- 1:male, 2:female") #get is used to get all the results, except for listbox which uses 'curselection'
    print(age_listbox.curselection(),"  <- 1:13-18, 2:19-30, 3:31-50, 4:>50")
    print("v4=",v4.get(),"  <- 1:like Book")
    print("v5=",v5.get(),"  <- 1:like Music")
    print("v6=",v6.get(),"  <- 1:like Movie")
    messagebox.showinfo("","Thanks!") #a message box to thank user for submitting the 'survey'

submit=Button(top,text="Submit",command=on_submit) #if the submit button is clicked, the on_submit function will execute
submit.pack(anchor=W,padx=5,pady=15)

top=mainloop()


