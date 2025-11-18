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

class AlexaAI:
    def __init__(self, root):
        self.root = root
        self.root.title('AlexaAI')
        self.root.geometry('750x600')
        self.root['bg'] = '#000000'

        # load jokes
        self.jokes = [] # list to store the jokes
        self.punchlines = [] # list to store the punchlines
        self.load_jokes() # lad the jokes from randomJokes .txt
        
        # create frames
        
        # start with title frame
        
        # center window using the function
        center_window(root)

    # loads the jokes from the randomJokes.txt file
    def load_jokes(self):
        with open('randomJokes.txt', 'r', encoding='utf-8') as file_handler:
           lines = file_handler.readlines()
    
        for l in lines:
            if '?' in l:
                data = l.split('?', 1) # split only on the first question mark
                if len(data) == 2:
                    self.jokes.append(data[0].strip())
                    self.punchlines.append(data[1].strip().replace('\n', ''))
    
    def create_frames(self):
        # create the title frame with gif
        self.title_frame = Frame(self.root, bg='#000000')
        
        # main frames with different backgrounds
        self.frames = {} # dictionary to store the frames and bg
        bg_names = ['bg1', 'bg2', 'bg3', 'bg4', 'bg5']
        for name in bg_names:
            frame = Frame(self.root)
            self.frames[name] = frame # matches the bg to their own frames
            
            bg_path = os.path.join('bgs', f'{name}.png')
            bg_photo = ImageTk.PhotoImage(Image.open(bg_path))
            bg_label = Label(frame, image=bg_photo)
            bg_label.image = bg_photo # to keep as reference
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
    

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


def main():
    root= Tk()
    app = AlexaAI(root)
    root.mainloop()