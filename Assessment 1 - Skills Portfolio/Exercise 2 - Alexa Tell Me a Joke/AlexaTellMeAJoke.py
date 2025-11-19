import os
from tkinter import *
import random
from PIL import Image, ImageTk, ImageSequence
import pygame

# for audio
pygame.mixer.init()

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

class AudioPlayer:
    def __init__(self):
        self.load_audio_files()
        
    def load_audio_files(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # load button sound
        button_path = os.path.join(current_dir, 'audio', 'button.mp3')
        self.button_sound = pygame.mixer.Sound(button_path)
        
        # load popup sound for the joke and punchline
        popup_path = os.path.join(current_dir, 'audio', 'popup.mp3')
        self.popup_sound = pygame.mixer.Sound(popup_path)
    
    def play_button_sound(self):
        self.button_sound.play()
        
    def play_popup_sound(self):
        self.popup_sound.play()

class AlexaAI:
    def __init__(self, root):
        self.root = root
        self.root.title('AlexaAI')
        self.root.geometry('750x600')
        self.root['bg'] = '#000000'
        self.root.resizable(0,0)

        self.audio = AudioPlayer()

        # load jokes
        self.original_jokes = [] # store all jokes initially before getting used
        self.original_punchlines = [] # store all punchlines initially before getting used
        self.jokes = [] # list to store the available jokes
        self.punchlines = [] # list to store the available punchlines
        self.load_jokes() # load the jokes from randomJokes .txt
        
        # create frames
        self.current_joke_index = -1
        
        # setup fonts for labels
        self.setup_fonts()
        
        # create frames
        self.create_frames()
        
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
                    self.original_jokes.append(data[0].strip())
                    self.original_punchlines.append(data[1].strip().replace('\n', ''))
    
        # initialize available jokes with all jokes
        self.jokes = self.original_jokes.copy()
        self.punchlines = self.original_punchlines.copy()
    
    def setup_fonts(self):
        self.joke_font = ('Stack Sans Headline', 13)
        self.thinking_font = ('Stack Sans Headline', 20)
    
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
                               command=self.quit_app, bd=0, highlightthickness=0,
                               activebackground='#d9d9d9')
        self.quit_btn.place(x=351, y=361)
        
        # frame 3 (bg3)
        self.thinking_lbl = Label(self.frames['bg3'], text='',
                                  font=self.thinking_font,
                                  bg='#d9d9d9', fg='black')
        self.thinking_lbl.place(x=90, y=207)
        
        self.joke_lbl = Label(self.frames['bg3'], text='', wraplength=500,
                                 font=self.joke_font, justify='left',
                                 bg='#d9d9d9', fg='black')
        self.joke_lbl.place(x=80, y=212)
        
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
        
        self.quit_btn_bg3 = Button(self.frames['bg3'], image=self.quit_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=self.quit_app, bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.quit_btn_bg3.place(x=355, y=509)
        
        # frame 4 (bg4) - Loading before punchline (no UI elements)
        self.joke_lbl_bg4 = Label(self.frames['bg4'], font=self.joke_font, 
                              wraplength=500, justify='left', bg='#d9d9d9', fg='black')
        self.joke_lbl_bg4.place(x=80, y=212)
        
        # frame 5 (bg5)
        # copy the joke label to bg5 so it remains visible
        self.joke_lbl_bg5 = Label(self.frames['bg5'], font=self.joke_font, 
                              wraplength=500, justify='left', bg='#d9d9d9', fg='black')
        self.joke_lbl_bg5.place(x=80, y=212)
        
        self.punchline_lbl = Label(self.frames['bg5'], text='', font=self.joke_font, 
                                   wraplength=500, justify='left', bg='#d9d9d9', fg='black')
        self.punchline_lbl.place(x=80, y=362)
        
        # Control buttons for frame 5
        self.next_btn_bg5 = Button(self.frames['bg5'], image=self.next_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=self.next_joke, bd=0, highlightthickness=0,
                                    activebackground='#d9d9d9')
        self.next_btn_bg5.place(x=525, y=509)
        
        self.quit_btn_bg5 = Button(self.frames['bg5'], image=self.quit_img, 
                                    bg='#d9d9d9', fg='black', 
                                    command=self.quit_app, bd=0, highlightthickness=0,
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
        self.audio.play_button_sound() # play button sound
        
        # disable generate button for the rest of the app
        self.generate_btn.config(state=DISABLED)
        
        # go to bg2
        self.show_frame('bg2')
        
        # after 0.5 seconds it will go to bg3 after thinking animation
        self.root.after(500, self.show_thinking_animation)
    
    def show_thinking_animation(self):
        self.show_frame('bg3')
        
        # clear previous joke
        self.joke_lbl.config(text='')
        
        # start thinking animation
        self.thinking_dots = 0
        self.animate_thinking()
        
    def animate_thinking(self):
        dots = '.' * (self.thinking_dots % 4)
        self.thinking_lbl.config(text=f'{dots}')
        self.thinking_dots += 1

        # animate for 2 seconds, then show joke
        if self.thinking_dots <= 8: # 8 cycles = 2 seconds
            self.root.after(250, self.animate_thinking)
        else:
            self.show_joke_setup()
    
    def show_joke_setup(self):
        # select random joke from the list
        if not self.jokes:
            self.handle_no_more_jokes()
            return

        # select random joke from available jokes list
        self.current_joke_index = random.randint(0, len(self.jokes) - 1)
        joke_text = self.jokes[self.current_joke_index]
        
        # show joke setup in bg3
        self.thinking_lbl.forget() # remove the thinking text
        self.joke_lbl.config(text=joke_text + '?')
        
        # set the joke in bg4 and bg5 so they will remain shown
        self.joke_lbl_bg4.config(text=joke_text + '?')
        self.joke_lbl_bg5.config(text=joke_text + '?')
        
        self.audio.play_popup_sound() # play popup sound when joke appears
        
        # store the current punchline before removing the joke
        self.current_punchline = self.punchlines[self.current_joke_index]
        
        # remove the used joke immediately after selecting it
        self.remove_used_joke()
    
    def show_punchline(self):
        self.audio.play_button_sound() # play button sound
        
        # go to bg4 first
        self.show_frame('bg4')
        
        # after 1.3 seconds, go to bg5 and show punchline
        self.root.after(1300, self.reveal_punchline)
            
    def remove_used_joke(self):
        if self.current_joke_index >= 0:
            # remove used joke and punchline
            del self.jokes[self.current_joke_index]
            del self.punchlines[self.current_joke_index]
            self.current_joke_index = -1        
    
    def reveal_punchline(self):
        self.show_frame('bg5')
        # use the stored punchline instead of accessing by index
        if hasattr(self, 'current_punchline') and self.current_punchline:
            self.punchline_lbl.config(text=self.current_punchline)
            self.current_punchline = None # clear the stored punchline after use
    
            self.audio.play_popup_sound() # play popup sound when punchline appears
            
            self.current_punchline = None
    
    def handle_no_more_jokes(self):
        # show message when no more jokes are available
        self.thinking_lbl.forget()
        self.joke_lbl.config(text='No more jokes available! Restart the app for more jokes.')
        
        # disable button since there's no punchline to show
        self.punchline_btn.config(state=DISABLED)
        
        # disable next button
        self.next_btn.config(state=DISABLED)
    
    def next_joke(self):
        self.audio.play_button_sound() # play button sound
        
        # check if there's still jokes available
        if not self.jokes:
            self.handle_no_more_jokes()
            return
        
        # go back to bg 2 and restart the cycle
        self.show_frame('bg2')
        self.root.after(1000, self.show_thinking_animation)
        
    def quit_app(self):
        self.audio.play_button_sound() # play button sfx
        self.root.after(100, self.root.destroy) # add a small delay before quitting to let the sound play
            
def main():
    root= Tk()
    app = AlexaAI(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()