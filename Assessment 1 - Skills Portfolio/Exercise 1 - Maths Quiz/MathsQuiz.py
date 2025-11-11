import os
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from tkinter import ttk, messagebox
import random
import time
import pygame 

class MathQuiz:
    def __init__(self, root):
        # create main window
        self.root = root
        self.root.title('Maths Quiz')
        self.root.geometry('750x600')
        self.root.iconbitmap(r'.\img\logo.ico') # icon for the app
        self.root.resizable(0,0)
        self.root['bg'] = '#000000'
        # self.root.wm_attributes('-transparentcolor', 'black')
        
        # pygame audio
        pygame.mixer.init()
        
        # load audio files
        self.load_audio()
        
        # center the window
        self.center_window()
        
        # game variables
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
        self.container.place(x=0, y=0, relwidth=1, relheight=1)
        
        # call the function to load images
        self.load_images()
        
        # add bg music
        self.play_bg_music('main_menu')
        
        # function to load the main menu
        self.main_menu_loader()
        
    # load al audio files
    def load_audio(self):
        # background music for different screens
        self.bg_music = {
            'main_menu': './audio/mainmenu.mp3',
            'easy_quiz': './audio/easy.mp3',
            'moderate_quiz': './audio/moderate.mp3',
            'hard_quiz': './audio/hard.mp3'
        }
        
        # sound effects
        self.btn_sound = './audio/btnclick.mp3'
        self.correct_sound = './audio/correct.mp3'
        self.incorrect_sound = './audio/incorrect.mp3'
        self.complete_sound = './audio/ending.mp3'
    
        # story sound effects
        self.footsteps1 = './audio/footsteps1.mp3'
        self.footsteps2 = './audio/footsteps2.mp3'
        self.thud_sound = './audio/thud.mp3'
    
    # play bg music for specific frames
    def play_bg_music(self, type):
        pygame.mixer.music.stop() # stop any currently playnig audio
        if type in self.bg_music:
            pygame.mixer.music.load(self.bg_music[type])
            pygame.mixer.music.play(-1) # loop indefinitely
        elif type == 'silence':
            pygame.mixer.music.stop() # stop music for story panels
    
    # play sound effect
    def play_sound(self, type):
        if type == 'button':
            pygame.mixer.Sound(self.btn_sound).play()
        elif type == 'correct':
            pygame.mixer.Sound(self.correct_sound).play()
        elif type == 'incorrect':
            pygame.mixer.Sound(self.incorrect_sound).play()
        elif type == 'complete':
            pygame.mixer.Sound(self.complete_sound).play()
        elif type == 'footsteps1':
            pygame.mixer.Sound(self.footsteps1).play()
        elif type == 'footsteps2':
            pygame.mixer.Sound(self.footsteps2).play()
        elif type == 'thud':
            pygame.mixer.Sound(self.thud_sound).play()
    
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
            img_path = f"./img/easy/easy{i}.png" # imports the image files
            img = ImageTk.PhotoImage(Image.open(img_path)) # opens each image
            self.easy_bg.append(img) # appends the images in the list

        # this is for the quiz background (easy mode)
        easy_quiz_path = "./img/easy/easyquizbg.png"
        self.easy_quiz_bg = ImageTk.PhotoImage(Image.open(easy_quiz_path))

        # backgrounds for moderate mode (17 story images and 1 quiz background)
        self.moderate_bg = []
        for i in range(1, 18): # mod1.png to mod17.png
            img_path = f"./img/moderate/mod{i}.png"
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

        # play music for main menu
        self.play_bg_music('main_menu')

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
                 command=lambda: [self.play_sound('button'), # play button click sound 
                                  self.start_story('easy')]) # start easy story
        easy_btn.place(x=125, y=384)

        # moderate button
        med_btn = Button(self.main_menu, text='Moderate',
                        bg='#c0c0c0',
                        font=('Lucida Console', 15),
                        padx=21, pady=3,
                        command=lambda: [self.play_sound('button'), # play button click sound 
                                  self.start_story('moderate')]) # play moderate story
        med_btn.place(x=298, y=384)

        # hard button
        hard_btn = Button(self.main_menu, text='Hard',
                        bg='#c0c0c0',
                        font=('Lucida Console', 15),
                        padx=46, pady=3,
                        command=lambda: [self.play_sound('button'), # play button click sound 
                                  self.start_story('hard')]) # play hard story
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
        
        # stop all running timers
        self.stop_all_timers()
        
        self.current_mode = mode
        self.score = 0
        self.hearts = 3.0 # reset to 3 full hearts
        self.ques_num = 0
        self.story_progress = 0
        self.quiz_completed = False
        self.mod_time_remaining = self.mod_time_limit
        self.hardmode_time_remaining = self.hardmode_total_time
        self.mod_quiz_part = 1 # reset moderate mode quiz part
        
        if mode == 'easy':
            self.show_easy_story() # proceed to easy mode story
        elif mode == 'moderate':
            self.show_moderate_story() # proceed to moderate mode story
        else:
            self.show_hard_story() # proceed to hard mode story
    
    # stops all timers that are running
    def stop_all_timers(self):
        self.timer_running = False 
        self.mod_timer_running = False # stops timer for moderate mode
        self.hardmode_timer_running = False # stops timer for hard mode
        
    # goes to the easy mode path
    def show_easy_story(self):
        self.story_progress += 1
        
        if self.story_progress == 1:
            self.show_story_frame(self.start_easy_quiz, 0) # show story frame, start with easy quiz
        elif self.story_progress == 2:
            if self.quiz_completed:
                self.show_easy_ending() # show ending screen
            else:
                self.start_easy_quiz() # start with easy quiz
    
    def show_moderate_story(self):
        self.story_progress += 1
        
        bg_index = min(self.story_progress - 1, 16) # mod1.png to mod17.png
        
        """
        EDIT THE BG IMGS LATER
        """
        story_actions = {
            1: lambda: self.show_story_frame(self.show_moderate_story, 0), # show moderate story and the background,
            2: lambda: self.show_story_frame(self.show_moderate_story, 1),
            3: lambda: self.show_story_frame(self.show_moderate_story, 2),
            4: lambda: self.show_story_frame(self.show_moderate_story, 3),
            5: lambda: self.show_story_frame(self.show_moderate_story, 4),
            6: lambda: self.show_story_frame(self.show_moderate_story, 5),
            7: lambda: self.show_story_frame(self.show_moderate_story, 6),
            8: lambda: self.show_story_frame(self.show_moderate_story, 7),
            9: self.start_moderate_quiz_part1, # start mod quiz part 1
            10: lambda: self.show_story_frame(self.show_moderate_story, 8),
            11: lambda: self.show_story_frame(self.show_moderate_story, 9),
            12: self.start_moderate_quiz_part2, # start mod quiz part 2
            13: lambda: self.show_story_frame(self.show_moderate_story, 10),
            14: lambda: self.show_story_frame(self.show_moderate_story, 11),
            15: lambda: self.show_story_frame(self.show_moderate_story, 12),
            16: lambda: self.show_story_frame(self.show_moderate_story, 13),
            17: self.start_moderate_quiz_part3, # start mod quiz part 3,
            18: lambda: self.show_story_frame(self.show_moderate_story, 14), # go back to main menu
            19: lambda: self.show_story_frame(self.show_moderate_story, 15),
            20: lambda: self.show_story_frame(self.show_mod_ending, 16),
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
                self.show_hard_ending() # go to ending screen
            else:
                self.start_hard_quiz() # start hard quiz
    
    # show ending screen for easy mode
    def show_easy_ending(self):
        self.play_sound('complete') # audio 
        self.show_ending_screen('easy', 'easyend.png')
    
    # show ending screen for moderate mode
    def show_mod_ending(self):
        self.play_sound('complete') # audio 
        self.show_ending_screen('moderate', 'modend.png')
    
    # show ending screen for hard mode 
    def show_hard_ending(self):
        self.play_sound('complete') # audio 
        self.show_ending_screen('hard', 'hardend.png')
    
    # ending screen which shows the summary of the game mode and the score
    def show_ending_screen(self, mode, bg_img_name):
        # stop quiz music and play ending sound
        self.play_bg_music('silence')
        self.play_sound('complete')
        
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # create ending frame
        ending_frame = Frame(self.container, bg='#000000')
        ending_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # load and set bg images
        bg_path = f'./img/{mode}/{bg_img_name}'
        bg_img = ImageTk.PhotoImage(Image.open(bg_path))
        bg_label = Label(ending_frame, image=bg_img, bg='#000000')
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_img
        
        # score display
        score_label = Label(ending_frame, text=f'Final Score: {self.score}/100',
                            font=('Lucida Console', 20, 'bold'),
                            fg='white', bg='black')
        score_label.place(x=375, y=300, anchor='center')
        
        # grade calculation based on the score
        percentage = self.score
        if percentage >= 90:
            grade = 'A+'
            grade_color = '#f1c40f'
        elif percentage >= 80:
            grade = "A"
            grade_color = "#2ecc71"
        elif percentage >= 70:
            grade = "B"
            grade_color = "#3498db"
        elif percentage >= 60:
            grade = "C"
            grade_color = "#e67e22"
        else:
            grade = "D"
            grade_color = "#e74c3c"
    
        grade_label = Label(ending_frame, text=f'Grade: {grade}',
                            font=('Lucida Console', 24, 'bold'),
                            fg=grade_color, bg='black')
        grade_label.place(x=375, y=350, anchor='center')
        
        # continue button to proceed to the main menu
        continue_btn = Button(ending_frame, text='Back to Main Menu',
                              font=('Lucida Console', 14), 
                              bg='#c0c0c0',
                              command=lambda: [self.play_sound('button'), # play button sound click
                                               self.main_menu_loader()]) # go back to main menu
        continue_btn.place(x=375, y=450, anchor='center')
        
        # bind key press to continue
        self.root.bind('<KeyPress>', lambda e: [self.play_sound('button'), # play sound
                                                self.main_menu_loader()]) # go back to main menu
    
    # this shows the story frame with its bg image and continue buttons
    def show_story_frame(self, next_action, bg_index=0):
        self.stop_all_timers() # stops all timers first

        # stops any music for story panels
        self.play_bg_music('silence')
        
        # play story sound effects based on bg index
        if self.current_mode == 'moderate':
            if bg_index == 5: # mod6.png
                self.root.after(500, lambda: self.play_sound('footsteps1'))
            elif bg_index == 11: # mod12.png
                self.root.after(500, lambda: self.play_sound('footsteps2'))
            elif bg_index == 15: # mod16.png
                self.root.after(500, lambda: self.play_sound('thud'))

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
            self.set_background_img(story_frame, bg_image)
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
        instruction_label.place(x=240, y=550)
        
    # handle any key press to continue the story 
    def handle_key_press(self, event):
        self.root.unbind('<KeyPress>') # unbind the keys to prevent multiple triggers

        if self.next_action:
            self.next_action()
    
    def start_easy_quiz(self):
        self.total_ques = 10
        self.ques_num = 0
        self.quiz_completed = False
        self.play_bg_music('easy_quiz') # play easy quiz music
        self.create_quiz_screen() # create quiz screen
        self.generate_question() # generate question function
    
    def start_moderate_quiz_part1(self): # janitor's closet bg
        self.total_ques = 3
        self.ques_num = 0
        self.quiz_completed = False
        self.play_bg_music('moderate_quiz') # play moderate quiz music
        self.create_quiz_screen() # create quiz screen
        self.generate_question() # generate question function

    def start_moderate_quiz_part2(self): # principal's office bg
        self.total_ques = 3
        self.ques_num = 0
        self.quiz_completed = False
        self.play_bg_music('moderate_quiz') # play moderate quiz music
        self.create_quiz_screen() # create quiz screen
        self.generate_question() # generate question function
    
    def start_moderate_quiz_part3(self): # security room bg
        self.total_ques = 4 # 10 questions in total for moderate mode
        self.ques_num = 0
        self.quiz_completed = False
        self.play_bg_music('moderate_quiz') # play moderate quiz music
        self.create_quiz_screen() # create quiz screen
        self.generate_question() # generate question function

    def start_hard_quiz(self):
        self.total_ques = 10
        self.ques_num = 0
        self.quiz_completed = False
        self.play_bg_music('hard_quiz') # play hard quiz music
        self.create_quiz_screen() # create quiz screen
        self.generate_question() # generate question function

    def create_quiz_screen(self):
        for widget in self.container.winfo_children(): # clear container
            widget.destroy()
        
        # unbind any previous key bindings
        self.root.unbind('<KeyPress>')
        
        # quiz frame
        self.quiz_frame = Frame(self.container, bg='#000000')
        self.quiz_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # set quiz bgs based on the mode chosen
        if self.current_mode == "easy" and hasattr(self, 'easy_quiz_bg'):
            self.bg_label = self.set_background_img(self.quiz_frame, self.easy_quiz_bg)
        elif self.current_mode == "moderate" and hasattr(self, 'mod_quiz_bgs'):
            # Use different background for each moderate quiz part
            bg_index = self.mod_quiz_part - 1  # Convert to 0-based index
            if bg_index < len(self.mod_quiz_bgs) and self.mod_quiz_bgs[bg_index] is not None:
                self.bg_label = self.set_background_img(self.quiz_frame, self.mod_quiz_bgs[bg_index])
                print(f"Using moderate quiz background {self.mod_quiz_part}")
            else:
                # Fallback if specific background not found
                self.bg_label = self.set_background_img(self.quiz_frame, self.mod_quiz_bgs[0])
        elif self.current_mode == "hard" and hasattr(self, 'hard_quiz_bg'):
            self.bg_label = self.set_background_img(self.quiz_frame, self.hard_quiz_bg)
        
        # character feedback img that is placed on the bg
        self.feedback_img_label = Label(self.quiz_frame, bg='black')
        self.feedback_img_label.place(x=80, y=180)
        self.show_feedback_img('nospeech') # show the default feedback img
        
        # score display
        self.score_label = Label(self.quiz_frame, text=f'Score: {self.score}',
                                 font=('Lucida Console', 14),
                                 fg='white', bg='black')
        self.score_label.place(x=50, y=50)

        # counts the questions
        counter_text = f'Question: {self.ques_num}/{self.total_ques}'
        self.counter_label = Label(self.quiz_frame, text=counter_text,
                                   font=('Lucida Console', 14),
                                   fg='white', bg='black')
        self.counter_label.place(x=50, y=80)
        
        # display the hearts
        self.hearts_frame = Frame(self.quiz_frame, bg='#000000')
        self.hearts_frame.place(x=580, y=50)
        self.update_hearts_display()
        
        # timer for moderate and hard mode
        if self.current_mode == 'moderate':
            timer_text = f'Time Left: {self.mod_time_remaining}s'
            self.mod_timer_label = Label(self.quiz_frame, text=timer_text,
                                         font=('Lucida Console', 16), 
                                         fg='#f39c12', bg='black')
            self.mod_timer_label.place(x=300, y=100)
            
        if self.current_mode == 'hard':
            timer_text = f'Time Left: {self.hardmode_time_remaining}s'
            self.hard_timer_label = Label(self.quiz_frame, text=timer_text,
                                          font=('Lucida Console', 16),
                                          fg='#e74c3c', bg='black')
            self.hard_timer_label.place(x=300, y=100)
        
        self.ques_label = Label(self.quiz_frame, text='', 
                                font=('Lucida Console', 24, 'bold'), 
                                fg='black', bg='white',
                                padx=23, pady=18)
        self.ques_label.place(x=510, y=260, anchor='center')
        
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
        button_positions = [
            (358, 356), (510, 356), 
            (358, 415), (510, 415)
        ] # list storing the buttons coordinates
        
        for i, (x, y) in enumerate(button_positions):
            choice_btn = Button(self.quiz_frame, text='',
                                font=('Lucida Console', 15),
                                command=lambda idx=i: [self.play_sound('button'), # play button click sound
                                                       self.check_choice(idx)],
                                width=10, bg='#c0c0c0', fg='black',
                                padx=7, pady=5)
            choice_btn.place(x=x, y=y)
            self.choice_buttons.append(choice_btn) # appends the choices inside the list
    
    # create an entry form for moderate and hard mode
    def create_entry_interface(self):
        # answer entry area
        self.answer_entry = Entry(self.quiz_frame, textvariable='Answer',
                                  font=('Lucida Console', 20),
                                  width=10, justify='center')
        self.answer_entry.place(x=420, y=365)
        self.answer_entry.bind('<Return>', lambda e: [self.play_sound('button'), # play button sound
                                                      self.check_ans_entry()]) # uses the return key in the keyboard to submit the answer
        self.answer_entry.focus()
        
        # submit button
        submit_btn = Button(self.quiz_frame, text='Submit',
                            font=('Lucida Console', 15, 'bold'),
                            command=lambda: [self.play_sound('button'),
                                             self.check_ans_entry()],
                            bg='#c0c0c0', fg='black',
                            padx=30, pady=3)
        submit_btn.place(x=425, y=443)
        
    # update hearts using imags
    def update_hearts_display(self):
        for widget in self.hearts_frame.winfo_children():
            widget.destroy()
        
        # create heart labels
        self.heart_labels = []
        for i in range(3):
            heart_label = Label(self.hearts_frame, bg='black')
            heart_label.pack(side='left', padx=2)
            self.heart_labels.append(heart_label)
    
        self.update_heart_img()
    
    # update the heart images based on current heart count
    def update_heart_img(self):
        if not hasattr(self, 'heart_labels') or not self.heart_labels:
            return
        
        for i in range(3):
            heart_value = self.hearts - i
            
            # full heart
            if heart_value >= 1:
                if self.heart_images.get('full'):
                    self.heart_labels[i].config(image=self.heart_images['full'])
                    self.heart_labels[i].image = self.heart_images['full']
            # half heart
            elif heart_value >= 0.5:
                if self.heart_images.get('half'):
                    self.heart_labels[i].config(image=self.heart_images['half'])
                    self.heart_labels[i].image = self.heart_images['half']
            # empty heart
            else:
                if self.heart_images.get('empty'):
                    self.heart_labels[i].config(image=self.heart_images['empty'])
                    self.heart_labels[i].image = self.heart_images['empty']
    
    def generate_question(self):
        self.ques_num += 1
        
        self.show_feedback_img('nospeech') # reset to no speech character
        
        # update counter label
        counter_text = f'Question: {self.ques_num}/{self.total_ques}'
        self.counter_label.config(text=counter_text)
        
        self.attempts = 0
        
        # reset timers based on mode
        if self.current_mode == "moderate":
            self.mod_time_remaining = self.mod_time_limit
            if hasattr(self, 'mod_timer_label'):
                self.mod_timer_label.config(text=f"Time Left: {self.mod_time_remaining}s", fg='#e74c3c')
        elif self.current_mode == "hard":
            self.hardmode_time_remaining = self.hardmode_total_time
        
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
        
        self.ques_label.config(text=self.current_ques)
    
        if self.current_mode == "easy":
            self.generate_choices()
        else:
            if hasattr(self, 'answer_entry'):
                self.answer_entry.delete(0, END)
                self.answer_entry.focus()
        
        # start the appropriate timer for each mode
        if self.current_mode == "moderate":
            self.start_mod_timer() # start moderate timer
        elif self.current_mode == "hard" and self.ques_num == 1:
            self.start_hard_timer() # start hard timer
    
    def generate_choices(self):
        self.choices = [self.correct_ans]
        # function to make the wrong choices
        while len(self.choices) < 4:
            wrong_ans = self.correct_ans + random.randint(-5, 5)
            if wrong_ans != self.correct_ans and wrong_ans > 0 and wrong_ans not in self.choices:
                self.choices.append(wrong_ans)
        
        # randomizes the buttons
        random.shuffle(self.choices) # shuffle is from random lib
        for i, button in enumerate(self.choice_buttons):
            button.config(text=str(self.choices[i]), state='normal', bg='#c0c0c0')
            
    def start_mod_timer(self):
        self.mod_timer_running = True
        self.update_mod_timer()
    
    def update_mod_timer(self):
        # checks if timer should still run and if quiz frame still exists
        if (self.mod_timer_running and self.mod_time_remaining > 0
            and hasattr(self, 'quiz_frame') and self.quiz_frame.winfo_exists()
            and hasattr(self, 'mod_timer_label') and self.mod_timer_label.winfo_exists()):
            
            self.mod_time_remaining -= 1
            timer_text = f'Time left: {self.mod_time_remaining}s'
            self.mod_timer_label.config(text=timer_text, fg='white')
            
            if self.mod_time_remaining <= 3:
                self.mod_timer_label.config(fg='red')

            self.root.after(1000, self.update_mod_timer)
        
        elif self.mod_timer_running and self.mod_time_remaining <= 0:
            self.mod_timer_running = False
            self.mod_time_out()
        
        else:
            # timer was stopped or screen was closed
            self.mod_timer_running = False
            
    # timer has run out
    def mod_time_out(self):
        if hasattr(self, 'quiz_frame') and self.quiz_frame.winfo_exists():
            # time's up and lose half a heart and move to next question
            self.hearts -= 0.5
            self.show_feedback(False)
            self.update_heart_img()  # update heart images
            if self.hearts <= 0:
                self.root.after(1000, self.game_over)
            else:
                self.root.after(1000, self.next_ques)
        
    def start_hard_timer(self):
        self.hardmode_timer_running = True
        self.update_hard_timer()
    
    def update_hard_timer(self):
        if (self.hardmode_timer_running and self.hardmode_time_remaining > 0
        and hasattr(self, 'quiz_frame') and self.quiz_frame.winfo_exists()
        and hasattr(self, 'hard_timer_label') and self.hard_timer_label.winfo_exists()):
            
            self.hardmode_time_remaining -= 1
            timer_text = f'Time left: {self.hardmode_time_remaining}s'
            self.hard_timer_label.config(text=timer_text, fg='white')
            
            if self.hardmode_time_remaining <= 10:
                self.hard_timer_label.config(fg='red')
            
            self.root.after(1000, self.update_hard_timer)
        
        elif self.hardmode_timer_running and self.hardmode_time_remaining <= 0:
            self.hardmode_timer_running = False
            self.hard_time_out()
        
        else:
            # timer was stopped ot quiz screen was closed
            self.hardmode_timer_running = False
    
    def hard_time_out(self):
        if hasattr(self, 'quiz_frame') and self.quiz_frame.winfo_exists():
            self.root.after(1000, self.continue_story)
            
    def check_choice(self, choice_index):
        selected = self.choices[choice_index]
        self.attempts += 1
        
        # reset all buttons to default color
        for button in self.choice_buttons:
            button.config(bg='#c0c0c0')
        
        # highlight the selected button
        self.choice_buttons[choice_index].config(bg='#a0a0a0')  # slightly darker when selected
        
        # stop moderate timer if answe ris submitted
        if self.current_mode == 'moderate':
            self.mod_timer_running = False
        
        if selected == self.correct_ans:
            self.play_sound('correct') # play sound if user gets the correct ans
            if self.attempts == 1:
                self.score += 10 # gives 10 points if user get the correct answer on first try
            else:
                self.score += 5 # gives 5 points on the second try
            self.show_feedback(True) # boolean to show the feedback
            self.score_label.config(text=f'Score: {self.score}')
            self.root.after(1000, self.next_ques)
        
        else:
            self.play_sound('incorrect') # sound if incorrect
            if self.attempts == 1:
                # first wrong attempt loses half a heart
                self.hearts -= 0.5
                self.show_feedback(False)
                self.update_heart_img() # update heart images
                # dont move to the next ques yet to allow a 2nd attempt
            else:
                # second wrong attmept loses the remaining half of the heart
                self.hearts -= 0.5
                self.show_feedback(False)
                self.update_heart_img() # update heart images
                if self.hearts <= 0:
                    self.root.after(1500, self.game_over)
                else:
                    self.root.after(1500, self.next_ques)
                    
    def check_ans_entry(self):
        # if the user gives a data type that is not an integer
        try:
            user_ans = int(self.answer_entry.get())
        except ValueError:
            return
        
        self.attempts += 1
        
        # stop mod timer if ans is submitted
        if self.current_mode == 'moderate':
            self.mod_timer_running = False
        
        if user_ans == self.correct_ans:
            self.play_sound('correct') # play sound if user gets the correct ans
            if self.attempts == 1:
                self.score += 10 # +10 for correct ans on first try
            else:
                self.score += 5 # +5 for correct ans on second try
            self.show_feedback(True)
            self.score_label.config(text=f'Score: {self.score}')
            self.root.after(1000, self.next_ques)
        
        else:
            self.play_sound('incorrect') # incorrect sfx
            if self.attempts == 1:
                # first wrong attempt -0.5 heart
                self.hearts -= 0.5
                self.show_feedback(False)
                self.update_heart_img()
                if self.hearts <= 0:
                    self.root.after(1500, self.game_over)
                else:
                    # allow second attempt
                    self.answer_entry.delete(0, END) # clears the entry area
                    self.answer_entry.focus()
            
            else:
                # second wrong attempt -0.5 heart
                self.hearts -= 0.5
                self.show_feedback(False)
                self.update_heart_img()
                if self.hearts <= 0:
                    self.root.after(1000, self.game_over)
                else:
                    self.root.after(1000, self.next_ques)
    
    def next_ques(self):
        if self.ques_num >= self.total_ques:
            self.quiz_completed = True
            if self.current_mode == 'moderate':
                self.mod_timer_running = False
            elif self.current_mode == 'hard':
                self.hardmode_timer_running = False
            self.continue_story() # continue story after the quiz is completed
        else:
            self.generate_question()
    
    def continue_story(self):
        # stop all timers before continuing
        self.stop_all_timers()
        
        if self.current_mode == 'easy':
            self.show_easy_story()
        elif self.current_mode == 'moderate':
            self.show_moderate_story()
        else:
            self.show_hard_story()
        
    def game_over(self):
        self.stop_all_timers()
        self.main_menu_loader()
        
if __name__ == "__main__":
    root = Tk()
    app = MathQuiz(root)
    root.mainloop()