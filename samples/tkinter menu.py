from tkinter import *

top=Tk()
menu_bar=Menu(top)

#file
file_menu=Menu(menu_bar,tearoff=0) #choices start at position 0

file_menu.add_command(label='New',command=lambda:print('New')) #add a menu item, when clicked, it prints 'New'
  #a lambda function is small anonymous function, which can take any number of arguments, but can only have one expression
file_menu.add_command(label='OPen',command=lambda:print('Open'))
file_menu.add_command(label='Save',command=lambda:print('Save'))
file_menu.add_command(label='Save as...',command=lambda:print('Save as...'))
file_menu.add_command(label='Close',command=lambda:print('Close'))
file_menu.add_separator() #add a horizontal line
file_menu.add_command(label='Exit',command=top.quit) #when clicked, it stops program execution

menu_bar.add_cascade(label='File',menu=file_menu) #associate file_menu (child) with menu_bar (parent)

#edit
edit_menu=Menu(menu_bar,tearoff=0)

edit_menu.add_command(label='Undo',command=lambda:print('Undo'))
edit_menu.add_separator()
edit_menu.add_command(label='Cut',command=lambda:print('Cut'))
edit_menu.add_command(label='Copy',command=lambda:print('Copy'))
edit_menu.add_command(label='Paste',command=lambda:print('Paste'))
edit_menu.add_command(label='Select All',command=lambda:print('Select All'))

menu_bar.add_cascade(label='Edit',menu=edit_menu)

#help
help_menu=Menu(menu_bar,tearoff=0)

help_menu.add_command(label='Help Index',command=lambda:print('Help Index'))
help_menu.add_command(label='About...',command=lambda:print('About...'))

menu_bar.add_cascade(label='Help',menu=help_menu)

#top
top.config(menu=menu_bar)
top.mainloop()
