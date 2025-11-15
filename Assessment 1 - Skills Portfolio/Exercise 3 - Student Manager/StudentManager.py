"""
# Exercise 3 - Student Manager

A list of student marks are held in the studentMarks.txt file available in the resources folder. These need to be loaded into a program to analyse the data. The first line is a single integer that gives the number of students in the class. Each subsequent line of the file comprises a student code (between 1000 and 9999), three course marks (each out of 20) and an examination mark (out of 100).

There is one line of data for each student in the class, with each piece of data separated by a comma (see example below).

8439,Jake Hobbs,10,11,10,43

Your task is to create a Tkinter GUI App that enables the user to manage this data. As a minimum expectation your app should include the following menu and use appropriate programming techniques to handle the functionality required by each menu item.


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
- Overall percentage (coursework and examination marks contributing in direct proportion to the marks available i.e. the percentage is based on the potential total of 160 marks).
- Student grade ( ‘A’ for 70%+, ‘B’ for 60%-69%, ‘C’ for 50%-59%, ‘D’ for 40%-49%, ‘F’ for under 40% )

&nbsp;Once all students have been output you should also output a summary stating the number of students in the class and the average percentage mark obtained.


### 2. View individual student record
Allow the user to select a student then output their results as per menu item 1.
How you enable the user to select the individual student is up to you, this could be done via a menu code, or by allowing the user to enter a students name and/or student number.
### 3. Show student with highest overall mark
Identify the student with the highest mark and output their results in same format as menu item 1.
### 4. Show student with lowest overall mark
Identify the student with the lowest mark and output their results in same format as menu item 1.
"""