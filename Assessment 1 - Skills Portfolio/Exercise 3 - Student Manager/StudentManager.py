"""
# Exercise 3 - Student Manager

A list of student marks are held in the studentMarks.txt file available in the resources 
folder. These need to be loaded into a program to analyse the data. The first line is 
a single integer that gives the number of students in the class. Each subsequent line 
of the file comprises a student code (between 1000 and 9999), three course marks (each 
out of 20) and an examination mark (out of 100).

There is one line of data for each student in the class, with each piece of data 
separated by a comma (see example below).

8439,Jake Hobbs,10,11,10,43

Your task is to create a Tkinter GUI App that enables the user to manage this data. 
As a minimum expectation your app should include the following menu and use appropriate 
programming techniques to handle the functionality required by each menu item.


    1. View all student records
    2. View individual student record
    3. Show student with highest total score
    4. Show student with lowest total score

Below are the expectations for each menu item:


                
### 1. View all student records:
The program should output the following information for each student:
- Students Name
- Students Number
- Total coursework mark
- Exam Mark
- Overall percentage (coursework and examination marks contributing in direct proportion 
to the marks available i.e. the percentage is based on the potential total of 160 marks).
- Student grade ( ‘A’ for 70%+, ‘B’ for 60%-69%, ‘C’ for 50%-59%, ‘D’ for 40%-49%, ‘F’ 
or under 40% )

&nbsp;Once all students have been output you should also output a summary stating the 
number of students in the class and the average percentage mark obtained.


### 2. View individual student record
Allow the user to select a student then output their results as per menu item 1.
How you enable the user to select the individual student is up to you, this could be 
done via a menu code, or by allowing the user to enter a students name and/or student 
number.
### 3. Show student with highest overall mark
Identify the student with the highest mark and output their results in same format as 
menu item 1.
### 4. Show student with lowest overall mark
Identify the student with the lowest mark and output their results in same format as 
menu item 1.
"""

import os
from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title('Student Manager')
root.geometry('1200x700')
root.iconbitmap(r'.\img\logo.ico')
root.resizable(0,0)

# maincontainer = Frame(root, bg='#000000')
# maincontainer.place(x=0, y=0, relwidth=1, relheight=1)

# frame1 = Frame(root, bg='#000000')
# frame1.place(x=0, y=0, relwidth=1, relheight=1)

# bgimg = ImageTk.PhotoImage(Image.open(r'.\img\bgs\studentrecordsbg.png'))
# bglbl = Label(frame1, image=bgimg)
# bglbl.place(x=0, y=0)

def home_page():
    delete_pages()
    home_frame = Frame(main_frame)

    lb = Label(home_frame,text='This is Home Page', font = ('Bold',30), bg='#234567',fg='#ffffff')
    lb.pack()
    home_frame.pack(pady=20)

#Function definitions for main page , When user clicks on main tab this function would be executed
def main_page():
    delete_pages()
    m_frame = Frame(main_frame)

    lb = Label(m_frame,text='This is Main Page', font = ('Bold',30), bg='#234567',fg='#ffffff')
    lb.pack()
    m_frame.pack(pady=20)

#Function definitions for info page , When user clicks on information tab this function would be executed
def info_page():
    delete_pages()
    info_frame = Frame(main_frame)

    lb = Label(info_frame,text='This is Info Page', font = ('Bold',30), bg='#234567',fg='#ffffff')
    lb.pack()
    info_frame.pack(pady=20)


#The following function is used to delete the contents of previous selected pages
def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()



#To create the frame on the left side of the window
options_frame = Frame(root, bg = '#22263d')

#Create home button
home_btn = Button(options_frame, text='Home', font=('Bold',12), fg='#ffffff',bg='#22263d',bd=0,
                     command=home_page)
home_btn.place(x=10, y=50)


#Create main button
main_btn = Button(options_frame, text='Main', font=('Bold',12), fg='#ffffff',bg='#22263d',bd=0,
                     command=main_page)
main_btn.place(x=10, y=100)

#Create info button
info_btn = Button(options_frame, text='Information', font=('Bold',12), fg='#ffffff',bg='#22263d',bd=0,
                     command=info_page)
info_btn.place(x=10, y=150)


options_frame.pack(side=LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=120, height=400) # Set the size of the left frame

#Create another frame to dispaly the contents when user clicks the buttons
main_frame = Frame(root,highlightbackground='black',highlightthickness=2,bg='#234567')

lb = Label(main_frame,text='Click on the buttons on left side', font = ('Bold',25),wraplength=250, bg='#234567',fg='#ffffff')
lb.pack()

main_frame.pack(side=LEFT)
main_frame.pack_propagate(False)
main_frame.configure(width=500, height=400) #Set the size of the frame on right side of window


root.mainloop()