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

import os
from tkinter import *
import random
from PIL import Image, ImageTk, ImageSequence

def center_window(window):
    window.update()  # Force window to update and calculate actual size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 3
    window.geometry(f"+{x}+{y}")

class GIFPlayer:
    def __init__(self, gif_path, label, width=None, height=None):
        self.gif_path = gif_path
        self.label = label
        self.frames = []
        self.width = width
        self.height = height
        self.load_gif()
        self.current_frame = 0
        self.playing = False
        
    def load_gif(self):
        # Get the absolute path to the GIF
        current_dir = os.path.dirname(os.path.abspath(__file__))
        gif_absolute_path = os.path.join(current_dir, 'gifs', 'title.gif')
        
        with Image.open(gif_absolute_path) as img:
            for frame in ImageSequence.Iterator(img):
                photo = ImageTk.PhotoImage(frame.copy())
                self.frames.append(photo)
                
    def play(self):
        self.playing = True
        self.animate()
        
    def stop(self):
        self.playing = False
        
    def animate(self):
        if self.playing and self.frames:
            self.label.config(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.label.after(100, self.animate)  # Adjust speed as needed

root = Tk()
root.title('AlexaAI')
root.geometry('750x600')
root['bg'] = '#000000'

center_window(root)

container = Frame(root, bg='#000000')
container.place(x=0, y=0, relwidth=1, relheight=1)

hero_page = Frame(container, bg='#000000')
hero_page.place(x=0, y=0, relwidth=1, relheight=1)

# Create label for GIF
gif_label = Label(hero_page, bg='#000000')
gif_label.place(relx=0.5, rely=0.5, anchor=CENTER)  # Center the label

# Create and play GIF
gif_player = GIFPlayer('gifs/hero.gif', gif_label, width=600, height=400)
gif_player.play()

def on_closing():
    gif_player.stop()
    root.destroy()
    
class AlexaAI():
    def __init__(self, root):
        self.root = root
    
# def open_file():
#     with open('randomJokes.txt', 'r') as file_handler:
#         lines = file_handler.readlines()
#     joke = []
#     punchline = []

#     for l in lines:
#         data = l.split('?')
#         joke.append(data[0])
#         punchline.append(data[1].replace('\n', ''))

#     number = random.randint(1, len(joke))
#     chosen_joke = joke[number]
#     chosen_punchline = punchline[number]
    
#     joketxt.insert(END, chosen_joke)
#     punchlinetxt.insert(END, chosen_punchline)

# joketxt = Text(root)
# joketxt.place(x=20, y=20, width=300, height=150)
# punchlinetxt = Text(root)
# punchlinetxt.place(x=320, y=20, width=300, height=150)

# Button(root, text='Tell me a joke',
#        command=open_file).place(x=20, y=155, width=100, height=20)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()