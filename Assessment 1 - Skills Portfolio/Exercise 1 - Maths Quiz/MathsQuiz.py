import os
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from tkinter import ttk, messagebox
import random
import time

class MathQuiz:
    def __init__(self, root):
        # create main window
        self.root = root
        self.root.title('Maths Quiz')
        self.root.geometry('750x600')
        self.root.iconbitmap(r'.\img\logo.ico') # icon for the app
        self.root.resizable(0,0)
        self.root['bg'] = '#000000'
        
        self.center_window()
        
        # game variables
            # score, hearts, mode, current question, correct answer, choices, 
            # attempts, question number, total questions, time limit, timer for moderate mode,
            # timer for hard mode, time remaining (for both mod and hard), is timer running, 
            # story progress, quiz finished, play gif
        self.score = 0 # set the score to 0
        self.hearts = 3 # set the number of hearts to 3 (full hearts)
        self.current_mode = None # set the current mode to none
        self.current_ques = None # question is none
        self.correct_ans = None # no correct answer set as default
        self.choices = [] # will store the choices here later on
        self.attempts = 0 # set to 0, will count when the quiz starts
        self.ques_num = 0 # set to 0, will increment when the quiz starts
        self.total_ques = 10 # all quiz modes have 10 questions max
        self.time_limit = 10 # 10 seconds for each question in moderate mode
        self.hardmode_total_time = 90 # 1min and 30secs timer for the whole hardmode quiz
        self.time_remaining = self.time_limit
        self.hardmode_time_remaining = self.hardmode_total_time
        self.timer_running = False 
        self.hardmode_timer_running = False
        self.story_progress = 0 # story progress will increase when the game starts based on frames
        self.quiz_completed = False
        self.gif_playing = False
        
        # container for all frames
        self.container = Frame(self.root, bg='#000000')
        self.container.place(x=0, y=0, relwidth=1, relhight=1)
        
        # will define a function to load the images (for frames)
        
        # will create a function to load the main menu
        
    # a function to center the tkinter window when it opens
    def center_window(self):
        self.root.update()  # Force window to update and calculate actual size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 3
        self.root.geometry(f"+{x}+{y}")

    # a function to load all background and feedback images to be used for each mode
    def load_images(self):
        # backgrounds for easy mode (2 story images and 1 quiz background)
        self.easy_bg = [] # a list to store all images for the story
        for i in range(1, 3):
            img_path = f".img/easy/easy{i}.png" # imports the image files
            img = ImageTk.PhotoImage(Image.open(img_path)) # opens each image
            self.easy_bg.append(img) # appends the images in the list

        # this is for the quiz background (easy mode)
        easy_quiz_path = "./img/easy/easyquizbg.png"
        self.easy_quiz_bg = ImageTk.PhotoImage(Image.open(easy_quiz_path))

        # backgrounds for moderate mode (17 story images and 1 quiz background)
        self.moderate_bg = []
        for i in range(1, 18): # mod1.png to mod17.png
            img_path = f".img/moderate/mod{i}.png"
            img = ImageTk.PhotoImage(Image.open(img_path))
            self.moderate_bg.append(img)

        # quiz background for moderate mode
        mod_quiz_path = './img/moderate/modquizbg.png'
        self.moderate_quiz_bg = ImageTk.PhotoImage(Image.open(mod_quiz_path))
        
        # hard mode bgs
        self.hard_bg = []
        for i in range(1, 4):
            img_path = f'./img/hard/hard{i}.png'
            img = ImageTk.PhotoImage(Image.open(img_path))
            self.hard_bg.append(img)
        
        # hard quiz bg
        hard_quiz_path = './img/hard/hardquizbg.png'
        self.hard_quiz_bg = ImageTk.PhotoImage(Image.open(hard_quiz_path))
        
        # feedback images (correct, incorrect, try, no speech)
        self.feedback_imgs = {} # dictionary to store the images
        feedback_types = ['correct', 'incorrect', 'nospeech', 'try']
        for type in feedback_types:
            img_path = f'./img/feedback/{type}.png' # uses 'type' instead of a random letter bc the file name is referred to based on the type
            self.feedback_imgs[type] = ImageTk.PhotoImage(Image.open(img_path)) # image appending with the type

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
        try:
            # Get the absolute path to the GIF
            current_dir = os.path.dirname(os.path.abspath(__file__))
            gif_absolute_path = os.path.join(current_dir, 'gifs', 'title.gif')
            
            with Image.open(gif_absolute_path) as img:
                for frame in ImageSequence.Iterator(img):
                    photo = ImageTk.PhotoImage(frame.copy())
                    self.frames.append(photo)
        except FileNotFoundError:
            print(f"Error: GIF file not found at {gif_absolute_path}")
            # Create a fallback image
            fallback_image = Image.new('RGB', (300, 200), color='lightblue')
            self.frames = [ImageTk.PhotoImage(fallback_image)]
        except Exception as e:
            print(f"Error loading GIF: {e}")
            # Create a fallback image
            fallback_image = Image.new('RGB', (300, 200), color='lightgray')
            self.frames = [ImageTk.PhotoImage(fallback_image)]
                
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


def switch_frame(frame):
    frame.tkraise()

# FRAME 1 (title frame)
main_menu = Frame(container, bg='#000000')
main_menu.place(x=0, y=0, relwidth=1, relheight=1)

# Create a label for the GIF background
gif_label = Label(main_menu, bg='#000000')
gif_label.pack()

# Create and start the GIF player
gif_player = GIFPlayer('./gifs/title.gif', gif_label, width=600, height=750)
gif_player.play()

# button display for all modes
easybtn = Button(main_menu, text='Easy',
                 bg='#c0c0c0',
                 font=('Lucida Console', 15),
                 padx=46, pady=3,
                 command=lambda: switch_frame(easymode))
easybtn.place(x=125, y=384)

medbtn = Button(main_menu, text='Moderate',
                 bg='#c0c0c0',
                font=('Lucida Console', 15),
                padx=21, pady=3,
                command=lambda: switch_frame(modmode))
medbtn.place(x=298, y=384)

hardbtn = Button(main_menu, text='Hard',
                 bg='#c0c0c0',
                font=('Lucida Console', 15),
                padx=46, pady=3,
                command=lambda: switch_frame(hardmode))
hardbtn.place(x=468, y=384)

# EASY MODE FRAME
easymode = Frame(container, bg='#000000')
easymode.place(x=0, y=0, relwidth=1, relheight=1)
easybg = ImageTk.PhotoImage(Image.open(r'.\img\easy1.png'))
easybglbl = Label(easymode, image=easybg)
easybglbl.pack()

game1 = Frame(container, bg='#000000')
game1.place(x=0, y=0, relwidth=1, relheight=1)
game1bg = ImageTk.PhotoImage(Image.open(r'.\img\easy2.png'))
game1bglbl = Label(game1, image=game1bg)
game1bglbl.pack()

nextbtn = Button(easymode, text='\u23f7',
                 bg='#c0c0c0',
                 font=('Lucida Console', 13),
                 command=lambda: switch_frame(game1))
nextbtn.place(x=610, y=448)

# MODERATE MODE FRAME
modmode = Frame(container, bg='#000000')
modmode.place(x=0, y=0, relwidth=1, relheight=1)
modbg = ImageTk.PhotoImage(Image.open(r'.\img\easy1.png'))
modbglbl = Label(modmode, image=easybg)
modbglbl.pack()

# HARD MODE FRAME
hardmode = Frame(container, bg='#000000')
hardmode.place(x=0, y=0, relwidth=1, relheight=1)
hardbg = ImageTk.PhotoImage(Image.open(r'.\img\easy1.png'))
hardbglbl = Label(hardmode, image=easybg)
hardbglbl.pack()


# Make sure to stop animation when window closes
def on_closing():
    gif_player.stop()
    root.destroy()

switch_frame(main_menu)


root.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == "__main__":
    root = Tk()
    root.mainloop()