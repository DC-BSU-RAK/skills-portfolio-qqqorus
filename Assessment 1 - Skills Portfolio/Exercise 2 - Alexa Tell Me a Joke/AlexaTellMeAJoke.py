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
        self.current_joke_index = -1
        
        # setup fonts for labels
        self.setup_fonts()
        
        # start with title frame
        self.show_title_frame()
        
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
                                 command=self.generate_joke, bd=0, highlightthickness=0,
                                 activebackground='#d9d9d9')
        self.generate_btn.place(x=86, y=361)
        
        self.quit_btn = Button(self.frames['bg1'], bg='#d9d9d9', image=self.quit_img,
                               command=self.root.destroy, bd=0, highlightthickness=0,
                               activebackground='#d9d9d9')
        self.quit_btn.place(x=351, y=361)
        
        # frame 3 (bg3)
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
                                    command=self.show_punchline, bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.punchline_btn.place(x=220, y=509)
        
        self.next_btn = Button(self.frames['bg3'], image=self.next_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=self.next_joke, bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.next_btn.place(x=525, y=509)
        
        self.quit_btn = Button(self.frames['bg3'], image=self.quit_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=self.root.destroy, bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.quit_btn.place(x=355, y=509)
        
        # frame 4 (bg4) - Loading before punchline (no UI elements)
        self.joke_lbl_bg4 = Label(self.frames['bg4'], font=self.joke_font, 
                              wraplength=600, justify='center', bg='#d9d9d9', fg='black')
        self.joke_lbl_bg4.place(x=80, y=197)
        
        # frame 5 (bg5)
        # copy the joke label to bg5 so it remains visible
        self.joke_lbl_bg5 = Label(self.frames['bg5'], font=self.joke_font, 
                              wraplength=600, bg='#d9d9d9', fg='black')
        self.joke_lbl_bg5.place(x=80, y=197)
        
        # thinking label for punchline animation in bg5
        self.thinking_lbl_bg5 = Label(self.frames['bg5'], text='',
                                      font=self.thinking_font,
                                      bg='#d9d9d9', fg='black')
        self.thinking_lbl_bg5.place(x=90, y=348)
        
        self.punchline_lbl = Label(self.frames['bg5'], text='', font=self.joke_font, 
                                   wraplength=600, bg='#d9d9d9', fg='black')
        self.punchline_lbl.place(x=80, y=348)
        
        # Control buttons for frame 5
        self.next_btn_bg5 = Button(self.frames['bg5'], image=self.next_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=self.next_joke, bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.next_btn_bg5.place(x=525, y=509)
        
        self.quit_btn_bg5 = Button(self.frames['bg5'], image=self.quit_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=self.root.destroy, bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.quit_btn_bg5.place(x=355, y=509)

    def show_title_frame(self):
        self.title_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        gif_lbl = Label(self.title_frame, bg='#000000')
        gif_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.gif_player = GIFPlayer('gifs/title.gif', gif_lbl)
        self.gif_player.play()
        
        # switch to main frame after 5 seconds
        self.root.after(5000, self.show_frame, 'bg1')

    def show_frame(self, name):
        # hide all frames first
        self.title_frame.place_forget()
        for frame in self.frames.values():
            frame.place_forget()
        
        # show the requested frame
        self.frames[name].place(x=0, y=0, relwidth=1, relheight=1)

    def generate_joke(self):
        # disable generate button for the rest of the app
        self.generate_btn.config(state=DISABLED)
        
        # go to bg2
        self.show_frame('bg2')
        
        # after 0.5 seconds it will go to bg3 after thinking animation
        self.root.after(500, self.show_thinking_animation_bg3)
    
    def show_thinking_animation_bg3(self):
        self.show_frame('bg3')
        
        # clear previous joke
        self.joke_lbl.config(text='')
        
        # start thinking animation
        self.thinking_dots = 0
        self.animate_thinking_bg3()
        
    def animate_thinking_bg3(self):
        dots = '.' * (self.thinking_dots % 4)
        self.thinking_lbl.config(text=f'{dots}')
        self.thinking_dots += 1

        # animate for 2 seconds, then show joke
        if self.thinking_dots <= 8: # 8 cycles = 2 seconds
            self.root.after(250, self.animate_thinking_bg3)
        else:
            self.show_joke_setup()
    
    def show_joke_setup(self):
        # select random joke from the list
        if self.jokes:
            self.current_joke_index = random.randint(0, len(self.jokes) - 1)
            joke_text = self.jokes[self.current_joke_index]
            
            # show joke setup in bg3
            self.thinking_lbl.forget() # remove the thinking text
            self.joke_lbl.config(text=joke_text + '?')
            
             # set the joke in bg4 and bg5 so they will remain shown
            self.joke_lbl_bg4.config(text=joke_text + '?')
            self.joke_lbl_bg5.config(text=joke_text + '?')
          
            # show buttons in bg3
            self.show_bg3_buttons()
            
    def hide_bg3_buttons(self):
        self.punchline_btn.place_forget()
        self.next_btn.place_forget()
        self.quit_btn.place_forget()
            
    def show_bg3_buttons(self):
        self.punchline_btn.place(x=220, y=509)
        self.next_btn.place(x=525, y=509)
        self.quit_btn.place(x=355, y=509)
    
    def show_punchline(self):
        # go to bg4 first
        self.show_frame('bg4')
        
        # after 2 seconds, go to bg5, thinking animation, and show punchline
        self.root.after(1000, self.show_thinking_animation_bg5)
            
    def show_thinking_animation_bg5(self):
        self.show_frame('bg5')
        
        # clear previous joke
        self.punchline_lbl.config(text='')
        self.thinking_lbl_bg5.config(text='')
        
        # start thinking animation
        self.thinking_dots = 0
        self.animate_thinking_bg5()
    
    def animate_thinking_bg5(self):
        dots = '.' * (self.thinking_dots % 4)
        self.thinking_lbl_bg5.config(text=f'{dots}')
        self.thinking_dots_bg5 += 1

        # animate for 2 seconds, then show joke
        if self.thinking_dots_bg5 <= 8: # 8 cycles = 2 seconds
            self.root.after(250, self.animate_thinking_bg5)
        else:
            self.show_joke_setup()
        
    def reveal_punchline(self):
        # hide thinking label before showing punchline
        self.thinking_lbl_bg5.config(text='')
        
        self.show_frame('bg5')
        if self.current_joke_index >= 0 and self.punchlines:
            punchline_text = self.punchlines[self.current_joke_index] # joke index will have the same index as punchline
            self.punchline_lbl.config(text=punchline_text)
    
    def next_joke(self):
        # go back to bg 2 and restart the cycle
        self.show_frame('bg2')
        self.root.after(1000, self.show_thinking_animation_bg3)
            
def main():
    root= Tk()
    app = AlexaAI(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()