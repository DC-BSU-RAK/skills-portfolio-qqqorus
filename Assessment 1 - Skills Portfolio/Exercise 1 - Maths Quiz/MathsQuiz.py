'''
Develop a GUI using Tkinter that presents the user with quiz of arithmetic problems. Each "play" of the quiz should be 10 questions. The user should initially be presented with a short menu of options to select a difficulty level. It could look something like this:

    DIFFICULTY LEVEL
     1. Easy
     2. Moderate
     3. Advanced

The difficulty levels determine the number of digits in the numbers to be added or subtracted. Easy means only single digit numbers; moderate means double digit numbers; and advanced means 4-digit numbers. After the user picks the level they desire, your program presents problems that look like this:

    45 + 9 =
    34 - 88 =
    etc

For each problem presented, the user is given a chance to answer. If the answer is correct, another problem is presented. If the answer is wrong, the user is to be given one more chance at that problem. The program should keep a tally of the users score, awarding 10 points for a correct answer on first attempt and 5 points on the second attempt. You should implement a random number generator (see the resources folder) to determine:
- The values to be added or subtracted
- Whether the problem is addition or subtraction

&nbsp;
The program should include the functions listed below. These functions should make use of parameters and return values as appropriate. You may include others or extend the functionality of the program if you see fit.
- **displayMenu**: A function that displays the difficulty level menu at the beginning of the quiz.
- **randomInt**: A function that determines the values used in each question. The min and max values of the numbers should be based on the difficulty level chosen as described above.
- **decideOperation**: A function that randomly decides whether the problem is an addition or subtraction problem and returns a char.
- displayProblem: A function that displays the question to the user and accepts their answer.
-** isCorrect**: A function that checks whether the users answer was correct and outputs an appropriate message
- **displayResults**: function that outputs the users final score out of a possible 100 and ranks the user based on their score (e.g. A+ for a score over 90)

&nbsp;
Once the user has finished the quiz, prompt them to see if they'd like to play it again

&nbsp;
**HINT :**
- Use Labels to display questions and instructions.
- Use Entry widgets to accept answers.
- Use Buttons for submitting answers, selecting difficulty, and replaying.
- Use Label/messagebox to display results or feedback messages.
'''

import os
from tkinter import *
from PIL import Image, ImageTk, ImageSequence

# a function to center the tkinter window when it opens
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

# Create main window
root = Tk()
root.title('Maths Quiz')
root.geometry('750x600')
root.iconbitmap(r'.\img\logo.ico')
root.resizable(0,0)
root['bg'] = '#000000'

# Center the window
center_window(root)

# container for all frames
container = Frame(root, bg='#000000')
container.place(x=0, y=0, relwidth=1, relheight=1)

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
easybg = ImageTk.PhotoImage(Image.open(r'.\img\e1.png'))
easybglbl = Label(easymode, image=easybg)
easybglbl.pack()

# MODERATE MODE FRAME
modmode = Frame(container, bg='#000000')
modmode.place(x=0, y=0, relwidth=1, relheight=1)
modbg = ImageTk.PhotoImage(Image.open(r'.\img\e1.png'))
modbglbl = Label(modmode, image=easybg)
modbglbl.pack()

# HARD MODE FRAME
hardmode = Frame(container, bg='#000000')
hardmode.place(x=0, y=0, relwidth=1, relheight=1)
hardbg = ImageTk.PhotoImage(Image.open(r'.\img\e1.png'))
hardbglbl = Label(hardmode, image=easybg)
hardbglbl.pack()


# Make sure to stop animation when window closes
def on_closing():
    gif_player.stop()
    root.destroy()

switch_frame(main_menu)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()