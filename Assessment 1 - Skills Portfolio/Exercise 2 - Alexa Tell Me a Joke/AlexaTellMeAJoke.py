import os
from tkinter import *
import random
from PIL import Image, ImageTk, ImageSequence

def center_window(window):
    window.update()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 3
    window.geometry(f"+{x}+{y}")

class GIFPlayer:
    def __init__(self, gif_path, label):
        self.gif_path = gif_path
        self.label = label
        self.frames = []
        self.load_gif()
        self.current_frame = 0
        self.playing = False
        
    def load_gif(self):
        # Get the absolute path to the GIF
        current_dir = os.path.dirname(os.path.abspath(__file__))
        gif_absolute_path = os.path.join(current_dir, 'gifs', 'title.gif')
        
        with Image.open(gif_absolute_path) as img:
            for frame in ImageSequence.Iterator(img):
                frame = frame.resize((750, 600), Image.LANCZOS)
                photo = ImageTk.PhotoImage(frame)
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
            self.label.after(20, self.animate)



# def switch_frame(frame):
#     frame.tkraise()

root = Tk()
root.title('AlexaAI')
root.geometry('750x600')
root['bg'] = '#000000'

center_window(root)

title = Frame(root, bg='#000000')
title.place(x=0, y=0, relwidth=1, relheight=1)

# create label for gif
gif_label = Label(title, bg='#000000')
gif_label.place(relx=0.5, rely=0.5, anchor=CENTER)  # Center the label

# create and play gif
gif_player = GIFPlayer('gifs/title.gif', gif_label, width=600, height=400)
gif_player.play()

def on_closing():
    gif_player.stop()
    root.destroy()
    
def open_file():
    with open('randomJokes.txt', 'r') as file_handler:
        lines = file_handler.readlines()
    joke = []
    punchline = []

    for l in lines:
        data = l.split('?')
        joke.append(data[0])
        punchline.append(data[1].replace('\n', ''))

    number = random.randint(1, len(joke))
    chosen_joke = joke[number]
    chosen_punchline = punchline[number]

def title_countdown():
    countdown_time = 3
    
    def update_countdown():
        if countdown_time > 0:
            countdown_time -= 1
            root.after(1000, update_countdown)
        else:
            mainframe_transition()
    
    update_countdown()
    
def mainframe_transition():
    gif_player.stop()
    title.destroy()
    

interface = Frame(root, )


Button(root, text='Tell me a joke',
       command=open_file).place(x=20, y=155, width=100, height=20)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()