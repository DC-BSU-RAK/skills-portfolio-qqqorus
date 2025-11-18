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
        self.root.resizable(0,0)

        # load jokes
        self.jokes = [] # list to store the jokes
        self.punchlines = [] # list to store the punchlines
        self.load_jokes() # lad the jokes from randomJokes .txt
        
        # create frames
        
        # setup fonts for labels
        self.setup_fonts()
        
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
    
    def setup_fonts(self):
        self.joke_font = ('Stack Sans Headline', 13)
        self.thinking_font = ('Stack Sans Headline', 16)
    
    def create_frames(self):
        # create the title frame with gif
        self.title_frame = Frame(self.root, bg='#000000')
        
        # main frames with different backgrounds
        self.frames = {} # dictionary to store the frames and bg
        bg_names = ['bg1', 'bg2', 'bg3', 'bg4', 'bg5']
        for name in bg_names:
            frame = Frame(self.root)
            self.frames[name] = frame # matches the bg to their own frames
            
            bg_path = os.path.join('imgs', 'bgs', f'{name}.png')
            bg_photo = ImageTk.PhotoImage(Image.open(bg_path))
            bg_label = Label(frame, image=bg_photo)
            bg_label.image = bg_photo # to keep as reference
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        self.setup_ui()
        
    def setup_ui(self):
        # using images for the buttons since i want them to be rounded
        self.generate_img = PhotoImage(file='./imgs/buttons/generate.png')
        self.punchline_img = PhotoImage(file='./imgs/buttons/punchline.png')
        self.next_img = PhotoImage(file='./imgs/buttons/next.png')
        self.quit_img = PhotoImage(file='./imgs/buttons/quit.png')
        
        # frame 1 - generate joke button
        self.generate_btn = Button(self.frames['bg1'], bg='#d9d9d9', 
                                 image=self.generate_img, 
                                 command=[placeholder], bd=0, highlightthickness=0,
                                 activebackground='#d9d9d9')
        self.generate_btn.place(x=86, y=361)
        
        self.quit_btn = Button(self.frames['bg1'], bg='#d9d9d9', image=self.quit_img,
                               command=self.root.destroy, bd=0, highlightthickness=0,
                               activebackground='#d9d9d9')
        self.quit_btn.place(x=351, y=361)
        
        # frame 3
        self.thinking_lbl = Label(self.frames['bg3'], text='',
                                  font=self.thinking_font,
                                  bg='#d9d9d9', fg='black')
        self.thinking_lbl.place(x=90, y=190)
        
        
        self.joke_lbl = Label(self.frames['bg3'], text='', wraplength=600,
                                 font=self.joke_font,
                                 bg='#d9d9d9', fg='black')
        self.joke_lbl.place(x=80, y=197)
        
        # control buttons for frame 3
        self.punchline_btn = Button(self.frames['bg3'], image=self.punchline_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=[placeholder], bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.punchline_btn.place(x=150, y=600)
        
        self.next_btn = Button(self.frames['bg3'], image=self.next_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=[placeholder], bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.next_btn.place(x=450, y=600)
        
        self.quit_btn = Button(self.frames['bg3'], image=self.quit_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=self.root.destroy, bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.quit_btn.place(x=250)
        
        # Frame 4 (bg4) - Loading before punchline (no UI elements)
        self.joke_label_bg4 = Label(self.frames['bg4'], font=self.joke_font, 
                              wraplength=600, justify='center', bg='#d9d9d9', fg='black')
        self.joke_label_bg4.place(x=80, y=197)
        
        # Frame 5 (bg5) - Punchline reveal (with joke still visible)
        # Copy the joke label to bg5 so it remains visible
        self.joke_label_bg5 = Label(self.frames['bg5'], font=self.joke_font, 
                              wraplength=600, justify='center', bg='#d9d9d9', fg='black')
        self.joke_label_bg5.place(x=80, y=197)
        
        self.punchline_label = Label(self.frames['bg5'], text='', font=self.joke_font, 
                                   wraplength=600, justify='center', bg='#d9d9d9', fg='black')
        self.punchline_label.place(x=80, y=348)
        
        # Control buttons for frame 5
        self.next_btn_bg5 = Button(self.frames['bg5'], image=self.next_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=self.next_joke, bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.next_btn_bg5.place(relx=0.4, rely=0.85, anchor=CENTER, width=120, height=35)
        
        self.quit_btn_bg5 = Button(self.frames['bg5'], image=self.quit_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=self.root.destroy, bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.quit_btn_bg5.place(relx=0.6, rely=0.85, anchor=CENTER, width=120, height=35)

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

    

interface = Frame(root, )


Button(root, text='Tell me a joke',
       command=open_file).place(x=20, y=155, width=100, height=20)


def main():
    root= Tk()
    app = AlexaAI(root)
    root.mainloop()