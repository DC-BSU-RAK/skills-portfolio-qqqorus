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
        self.hearts = 3.0 # set the number of hearts to 3 (full hearts) and as a float
        self.current_mode = None # set the current mode to none
        self.current_ques = None # question is none
        self.correct_ans = None # no correct answer set as default
        self.choices = [] # will store the choices here later on
        self.attempts = 0 # set to 0, will count when the quiz starts
        self.ques_num = 0 # set to 0, will increment when the quiz starts
        self.total_ques = 10 # all quiz modes have 10 questions max
        self.time_limit = 15
        self.mod_time_limit = 15 # 15 seconds for each question in moderate mode
        self.hardmode_total_time = 90 # 1min and 30secs timer for the whole hardmode quiz
        self.time_remaining = self.time_limit
        self.mod_time_remaining = self.mod_time_limit
        self.hardmode_time_remaining = self.hardmode_total_time
        self.timer_running = False
        self.mod_timer_running = False
        self.hardmode_timer_running = False
        self.story_progress = 0 # story progress will increase when the game starts based on frames
        self.quiz_completed = False
        self.gif_playing = False
        self.mod_quiz_part = 1 # tracks which moderate quiz part the user is in
        self.next_action = None
        
        # container for all frames
        self.container = Frame(self.root, bg='#000000')
        self.container.place(x=0, y=0, relwidth=1, relhight=1)
        
        # call the function to load images
        self.load_images()
        
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
        self.mod_quiz_bgs = []
        for i in range(1, 4): # modquizbg1.png to modquizbg3.png
            img_path = f'./img/moderate/modquizbg{i}.png'
            img = ImageTk.PhotoImage(Image.open(img_path))
            self.mod_quiz_bgs.append(img)
            
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

        self.heart_images = {}
        heart_types = ['empty', 'full', 'half']
        for type in heart_types:
            img_path = f'./img/hearts/{type}.png'
            img = Image.open(img_path)
            img = img.resize((30,30)) # resize the hearts to 30x30 pixels
            self.heart_images[type] = ImageTk.PhotoImage(img)

    # creating the main_menu with gif background
    def main_menu_loader(self):
        for widget in self.container.winfo_children():
            widget.destroy() # this function creates a clear container

        # creating frame for main menu
        self.main_menu = Frame(self.container, bg='#000000')
        self.main_menu.place(x=0, y=0, relwidth=1, relheight=1)
        
        # creating the gif background label
        self.gif_label = Label(self.main_menu, bg='#000000')
        self.gif_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # load and play the gif bg
        self.gif_playing = True
        self.load_and_play_gif()
        
        # putting the buttons for mode selection
        self.create_mode_buttons()
        
    # function to load and play the main menu bg gif
    def load_and_play_gif(self):
        current_dir = os.path.dirname(os.path.abspath(__file__)) # gets the absolute path of this python file
        gif_path = os.path.join(current_dir, 'gifs', 'title.gif') # combines the current dir path with the 'gifs' folder and 'title.gif' filename
    
        self.gif_frames = [] # empty list to store all individual frames of the gif
        with Image.open(gif_path) as img: # opening the gif file and using with statement to ensure the file is closed after use
            for frame in ImageSequence.Iterator(img): # loop through each frame in the gif file
                photo = ImageTk.PhotoImage(frame.copy()) # creating a copy with 'frame.copy()' to avoid modifying the original frame
                self.gif_frames.append(photo) # adds current frame to the list
        
        self.current_gif_frame = 0 # counter to keep track of what frame is being currently displayed
        self.animate_gif()

    # animate the gif frames
    def animate_gif(self):
        if (hasattr(self, 'gif_frames') and self.gif_frames and # checks if the object has a 'gif_frames' attr (list) & if the list is not empty
            hasattr(self, 'gif_playing') and self.gif_playing and # checks if the object has a 'gif_playing' attr (animation control) and if it's set to 'True'
            hasattr(self, 'gif_label') and self.gif_label.winfo_exists()): # checks if the object has 'gif_label' attr (display widget) and if it still exists in the window
            
            self.gif_label.config(image=self.gif_frames[self.current_gif_frame]) # updates the gif_label widget to show the current frame
            self.current_gif_frame = (self.current_gif_frame + 1) % len(self.gif_frames) # calculates the next frame index using modulo
            self.root.after(100, self.animate_gif) # creates the loop so the gif will run repeatedly
        
    # stops the gif animation
    def stop_gif(self):
        self.gif_playing = False # break the loop bc it's set to 'False'

    # create mode selection buttons that will be placed on the GIF bg
    def create_mode_buttons(self):
        # easy button
        easy_btn = Button(self.main_menu, text='Easy',
                 bg='#c0c0c0',
                 font=('Lucida Console', 15),
                 padx=46, pady=3,
                 command=lambda: self.start_story('easy'))
        easy_btn.place(x=125, y=384)

        # moderate button
        med_btn = Button(self.main_menu, text='Moderate',
                        bg='#c0c0c0',
                        font=('Lucida Console', 15),
                        padx=21, pady=3,
                        command=lambda: self.start_story('moderate'))
        med_btn.place(x=298, y=384)

        # hard button
        hard_btn = Button(self.main_menu, text='Hard',
                        bg='#c0c0c0',
                        font=('Lucida Console', 15),
                        padx=46, pady=3,
                        command=lambda: self.start_story('hard'))
        hard_btn.place(x=468, y=384)

    # will set the bg image on a frame
    def set_background_img(self, frame, image):
        if image is not None:
            bg_label = Label(frame, image=image, bg='#000000')
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = image
            return bg_label

    def start_story(self, mode):
        # stop gif animation
        self.stop_gif()
        
        self.stop_all_timers()
        
        self.current_mode = mode
        self.score = 0
        self.hearts = 3
        self.ques_num = 0
        self.story_progress = 0
        self.quiz_completed = False
        self.hardmode_time_remaining = self.hardmode_total_time
        
        if mode == 'easy':
            self.show_easy_story() # proceed to easy mode story
        elif mode == 'moderate':
            self.show_moderate_story() # proceed to moderate mode story
        else:
            self.show_hard_story() # proceed to hard mode story
    
    # stops all timers that are running
    def stop_all_timers(self):
        self.timer_running = False # stops timer for moderate mode
        self.hardmode_timer_running = False # stops timer for hard mode
        
    # goes to the easy mode path
    def show_easy_story(self):
        self.story_progress += 1
        
        if self.story_progress == 1:
            self.show_story_frame(self.start_easy_quiz, 0) # show story frame, start with easy quiz
        elif self.story_progress == 2:
            if self.quiz_completed:
                self.show_story_frame(self.main_menu_loader, 1) # show story frame, go back to main menu
            else:
                self.start_easy_quiz # start with easy quiz
    
    def show_moderate_story(self):
        self.story_progress += 1
        
        bg_index = min(self.story_progress - 1, 16)
        
        """
        EDIT THE BG IMGS LATER
        """
        story_actions = {
            1: lambda: # show moderate story and the background,
            # will add more story actions once the show story frame functions is created
            9: # start mod quiz part 1,
            12: # start mod quiz part 2,
            17: # start mod quiz part 3,
            18: lambda: [placeholder] # go back to main menu
        }
       
        action = story_actions.get(self.story_progress)
        if action:
            action()
        
    def show_hard_story(self):
        self.story_progress += 1
        
        if self.story_progress == 1: 
            self.show_story_frame(self.start_hard_quiz, 0) # start hard quiz
        elif self.story_progress == 2:
            if self.quiz_completed:
                self.show_story_frame(self.main_menu_loader) # go back to main menu
            else:
                self.start_hard_quiz # start hard quiz
    
    # this shows the story frame with its bg image and continue buttons
    def show_story_frame(self, next_action, bg_index=0):
        self.stop_all_timers() # stops all timers first

        # for a clear container
        for widget in self.container.winfo_children():
            widget.destroy()
            
        # create a story frame
        story_frame = Frame(self.container, bg='#000000')
        story_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # set the appropriate bg
        if self.current_mode == 'easy' and hasattr(self, 'easy_bg'):
            bg_image = self.easy_bg[bg_index] if bg_index < len(self.easy_bg) else None
            self.set_background_img(story_frame, bg_image)
        elif self.current_mode == 'moderate' and hasattr(self, 'moderate_bg'):
            bg_image = self.moderate_bg[bg_index] if bg_index < len(self.moderate_bg) else None
        elif self.current_mode == 'hard' and hasattr(self, 'hard_bg'):
            bg_image = self.hard_bg[bg_index] if bg_index < len(self.hard_bg) else None
            self.set_background_img(story_frame, bg_image)
        
        # variable to store the next action
        self.next_action = next_action
        
        # binds any key press to navigate thru the narration
        self.root.bind('<KeyPress>', self.handle_key_press)
        self.root.focus_set() # ensure that the window has focus to receive key events
        
        # create the instruction label at the bottom
        instruction_label = Label(story_frame, text='Press any key to continue...',
                                  font=('Lucida Console', 12),
                                  fg='white', bg='#000000')
        instruction_label.place(x=250, y=550)
        
    # handle any key press to continue the story 
    def handle_key_press(self, event):
        self.root.unbind('<KeyPress>') # unbind the keys to prevent multiple triggers

        if self.next_action:
            self.next_action()
    
    def start_easy_quiz(self):
        self.total_ques = 10
        self.ques_num = 0
        self.quiz_completed = False
        self.create_quiz_screen() # create quiz screen
        [placeholder]
        # generate question function
    
    def start_moderate_quiz_part1(self): # janitor's closet bg
        self.total_ques = 3
        self.ques_num = 0
        self.quiz_completed = False
        self.create_quiz_screen() # create quiz screen
        [placeholder]
        # generate question function

    def start_moderate_quiz_part2(self): # principal's office bg
        self.total_ques = 3
        self.ques_num = 0
        self.quiz_completed = False
        self.create_quiz_screen() # create quiz screen
        [placeholder]
        # generate question function
    
    def start_moderate_quiz_part3(self): # security room bg
        self.total_ques = 4 # 10 questions in total for moderate mode
        self.ques_num = 0
        self.quiz_completed = False
        self.create_quiz_screen() # create quiz screen
        [placeholder]
        # generate question function

    def start_hard_quiz(self):
        self.total_ques = 10
        self.ques_num = 0
        self.quiz_completed = False
        self.create_quiz_screen() # create quiz screen
        [placeholder]
        # generate question function

    def create_quiz_screen(self):
        for widget in self.container.winfo_children(): # clear container
            widget.destroy()
            
        # quiz frame
        self.quiz_frame = Frame(self.container, bg='#000000')
        self.quiz_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # set quiz bgs based on the mode chosen
        if self.current_mode == 'easy' and hasattr(self, 'easy_quiz_bg'):
            self.bg_label = self.set_background_img(self.quiz_frame, self.easy_quiz_bg)
        elif self.current_mode == 'moderate' and hasattr(self, 'moderate_quiz_bg'):
            self.bg_label = self.set_background_img(self.quiz_frame, self.moderate_quiz_bg)
        elif self.current_mode == 'hard' and hasattr(self, 'hard_quiz_bg'):
            self.bg_label = self.set_background_img(self.quiz_frame, self.hard_quiz_bg)
        
        # character feedback img that is placed on the bg
        self.feedback_img_label = Label(self.quiz_frame, bg='#000000')
        self.feedback_img_label.place(x=50, y=200)
        # show the default feedback img
        
        # score display
        self.score_label = Label(self.quiz_frame, text=f'Score: {self.score}',
                                 font=('Lucida Console', 14),
                                 fg='white')
        self.score_label.place(x=300, y=50)

        # counts the questions
        counter_text = f'Question: {self.ques_num}/{self.total_ques}'
        self.counter_label = Label(self.quiz_frame, text=counter_text,
                                   font=('Lucida Console, 14'),
                                   fg='white')
        self.counter_label.place(x=300, y=80)
        
        # hearts display
        self.hearts_frame = Frame(self.quiz_frame)
        self.hearts_frame.place(x=500, y=50)
        self.update_hearts_display()
        
        # timer for moderate and hard mode
        if self.current_mode == 'moderate':
            timer_text = f'Time Left: {self.time_remaining}s'
            self.mod_timer_label = Label(self.quiz_frame, text=timer_text,
                                         font=('Lucida Console', 16), 
                                         fg='#f39c12')
            self.mod_timer_label.place(x=300, y=110)
        elif self.current_mode == 'hard':
            timer_text = f'Time Left: {self.hardmode_time_remaining}s'
            self.hard_timer_label = Label(self.quiz_frame, text=timer_text,
                                          font=('Lucida Console, 16'),
                                          fg='#e74c3c')
            self.hard_timer_label.place(x=300, y=110)
        
        self.ques_label = Label(self.quiz_frame, text='', 
                                font=('Lucida Console', 24, 'bold'), 
                                fg='#000000')
        self.ques_label.place(x=375, y=200, anchor='center')
        
        # input area for the user to answer
        if self.current_mode == 'easy':
            self.create_mcq_interface() # mcq interface
        else:
            self.create_entry_interface() # entry form interface for moderate and hard mode
        
    # show the appropriate character feedback img
    def show_feedback_img(self, type):
        if (hasattr(self, 'feedback_imgs') and type in self.feedback_imgs and
            self.feedback_imgs[type] is not None):
            self.feedback_img_label.config(image=self.feedback_imgs[type])
            self.feedback_img_label.image = self.feedback_imgs[type]
    
    # display feedback using the imgs
    def show_feedback(self, is_correct=True):
        if is_correct:
            self.show_feedback_img('correct')
        else:
            if self.attempts == 1:
                self.show_feedback_img('try')
            else:
                self.show_feedback_img('incorrect')
        
        # return to nospeech after 1 second
        self.root.after(1000, lambda: self.show_feedback_img('nospeech'))
    
    # create multiple choice buttons for easy mode
    def create_mcq_interface(self):
        self.choice_buttons = [] # empty list to store the choices
        button_positions = [(250, 300), (450, 300), (250, 400), (450, 400)] # list storing the buttons coordinates
        
        for i, (x, y) in enumerate(button_positions):
            choice_btn = Button(self.quiz_frame, text='',
                                font=('Lucida Console', 14),
                                command=[placeholder],
                                width=8, height=2, bg='#ffffff', fg='black')
        choice_btn.place(x=x, y=y)
        self.choice_buttons.append() # appends the choices inside the list
    
    # create an entry form for moderate and hard mode
    def create_entry_interface(self):
        answer_label = Label(self.quiz_frame, text='Answer:',
                             font=('Lucida Console', 14),
                             fg='#00000')
        answer_label.place(x=300, y=350)
        
        # answer entry area
        self.answer_entry = Entry(self.quiz_frame,
                                  font=('Lucida Console', 14),
                                  width=10, justify='center')
        self.answer_entry.place(x=400, y=350)
        self.answer_entry.bind('<Return>', lambda e: [placeholder]) # uses the return key in the keyboard to submit the answer
        self.answer_entry.focus()
        
        # submit button
        submit_btn = Button(self.quiz_frame, text='Submit',
                            font=('Lucida Console', 12),
                            command=[placeholder],
                            bg='#2ecc71', fg='white')
        submit_btn.place(x=500, y=350)
        
    def update_hearts_display(self):
        for widget in self.hearts_frame.winfo_children():
            widget.destroy()
            
        # [placeholder]
        for i in range(3):
            if i < self.hearts:
                hearts = '♥' if i < int(self.hearts) else '♡'
                color = 'red' if i < int(self.hearts) else 'pink'
            else:
                heart = '♡'
                color = 'gray'

            heart_label = Label(self.hearts_frame, text=heart,
                                font=('Lucida Console'),
                                fg=color)
            heart_label.pack(side='left', padx=2)
    
    def generate_question(self):
        self.ques_num += 1
        
        self.show_feedback_img('nospeech') # reset to no speech character
        
        counter_text = f'Question: {self.ques_num}/{self.total_ques}'
        self.counter_label.config(text=counter_text)
        
        self.attempts = 0
        
        # generate question based on difficulty
        if self.current_mode == 'easy':
            a, b = random.randint(-9, 10), random.randint(-9, 10)
            operator = random.choice(['+', '-'])
            if operator == '+':
                self.correct_ans = a + b
            else:
                a, b = max(a, b), min(a, b) # makes sure that the bigger number is always first
                self.correct_ans = a - b
            self.current_ques = f'{a} {operator} {b} ='
        elif self.current_mode == 'moderate':
            a, b = random.randint(10, 100), random.randint(10, 100)
            operator = random.choice(['+', '-'])
            if operator == '+':
                self.correct_ans = a + b
            else:
                a, b = max(a, b), min(a, b)
                self.correct_ans = a - b
            self.current_ques = f'{a} {operator} {b} = ?'
        else:
            a, b = random.randint(1000, 5001), random.randint(1000, 5001)
            operator = random.choice(['+', '-'])
            if operator == '+':
                self.correct_ans = a + b
            else:
                a, b = max(a, b), min(a, b)
                self.correct_ans = a - b
            self.current_ques = f'{a} {operator} {b} = ?'
        
        self.question_label.config(text=self.current_ques)
    
        if self.current_mode == "easy":
            self.generate_choices()
        else:
            if hasattr(self, 'answer_entry'):
                self.answer_entry.delete(0, END)
                self.answer_entry.focus()
        
        # start the appropriate timer for each mode
        if self.current_mode == "moderate" and self.question_number == 1:
            # start moderate timer
        elif self.current_mode == "hard" and self.question_number == 1:
            # start hard timer
    
    def generate_choices(self):
        self.choices = [self.correct_ans]
        while len(self.choices) < 4:
        
if __name__ == "__main__":
    root = Tk()
    root.mainloop()