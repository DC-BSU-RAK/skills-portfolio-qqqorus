"""
# Exercise 2 - Alexa tell me a Joke

The randomJokes.txt file in the resources folder contains a dataset of random jokes. 
Each joke is on a new line and consists of a setup and punchline separated by a question mark. 
For example:

    - Why did the chicken cross the road? To get to the other side.
    - What happens if you boil a clown? You get a laughing stock.
  
Develop a Tkinter GUI application that acts like a joke-telling assistant. 
The program should:

- Display a window with a button labeled "Alexa tell me a Joke".
- When the button is clicked, randomly select a joke from the randomJokes.txt file, 
    display the setup of the joke in a label.
- Provide another button labeled "Show Punchline"- When clicked, 
    display the punchline below the setup.
- Include a "Next Joke" button so the user can request another random joke.
- Additionally , provide a "Quit" button to close the application.
"""

from tkinter import *
import random

root = Tk()
root.title('AlexaAI')
root.geometry('500x500')
root['bg'] = '#234567'

jokes = {}

with open('randomJokes.txt', 'r') as file_handler:
    lines = file_handler.readlines()
joke = []
punchline = []

for l in lines:
    data = l.split('?')
    joke.append(data[0])
    punchline.append(data[1])
    
print(f'Joke list: {joke}')
print(f'Punchline list: {punchline}')


# def open_file():
#     with open('randomJokes.txt') as file_handler:
#         lines = file_handler.readline()
#         num_string = ''
#         for line in lines:
#             num_string += line.rstrip() + ''
    
#     txtarea.insert(END, num_string)

# txtarea = Text(root)
# txtarea.place(x=20, y=20, width=300, height=150)

# Button(root, text='read line',
#        command=open_file).place(x=20, y=155, width=100, height=20)

root.mainloop()