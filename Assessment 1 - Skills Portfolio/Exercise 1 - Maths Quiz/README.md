# Exercise 1 - Maths Quiz

**📝 DESCRIPTION:**

An interactive game that combines math challenges with a storyline across three difficulty levels. This Math Quiz contains subtle horror elements to it. It is set in a school setting, with one nameless character the player will portray to navigate the story with.

**🚀 FEATURES:**

    > GAME MODES / DIFFICULTY LEVEL <
        <Easy Mode>: Contains basic subtraction and addition of single-digit numbers with  multiple-choice answers.
        <Moderate Mode>: Involves intermediate subtraction and addition of two-digit numbers with text entry, and a 15 second timer per question.
        <Hard Mode>: Has advanced subtraction and addition of four-digit numbers with text entry, and a 2 minute timer for the overall quiz.

    > CORE MECHANICS <
        # Hearts System: 3 hearts in total, player loses 0.5 hearts every time they get an answer incorrectly.
        # Scoring System: 
            - 10 points for answering correctly on the first attempt
            - 5 points for answering correctly on the second attempt
        # Timed Quizzes:
            - Moderate: 15 seconds per question
            - Hard: 2 minutes / 120 seconds for the entire quiz

    > IMMERSIVE ELEMENTS <
        ~ Narrative panels between quiz sections.
        ~ Contains background music for each mode, sound effects, and character feedback sounds.
        ~ Has visual feedback of the character responding to correct / incorrect answers.

**🎮 HOW TO PLAY:**
1. Select difficulty. Choose from Easy, Moderate, or Hard.
2. Advance through narrative panels to proceed to the quiz.
3. Solve math problems to continue with the story.
4. Manage your hearts and time so that you don't run out.
5. Finish all questions to see your final score.

**⚙️ TECHNICAL IMPLEMENTATION:**

    > RANDOMIZATION <
        # Used Python's `random` module to generate random numbers for the quiz, randomize operators, shuffle the multiple-choice answers in Easy mode, and ensure that the number ranges appropriate for each difficulty level.

    > GUI FRAMEWORK AND WIDGETS <
        * Used [Frames] to contain different screens, especially in quizzes and story panels.
        * Used [Labels] to display text, scores, timers, and background images.
        * Used [Buttons] to submit answers, select difficulty, and replaying.
        * Used [Entry] to submit answers in moderate and hard mode.

    > FILE STRUCTURE <
        MathsQuiz/
        |--- MathsQuiz.py       # main game file
        |--- img/               
        |   |--- easy/          # easy mode backgrounds
        |   |--- moderate/      # moderate mod backgrounds
        |   |--- hard/          # hard mode backgrounds
        |   |--- feedback/      # character feedback images
        |   |--- hearts/        # heart display images
        |--- audio/             # music and sound effects
        |--- gif/               # main menu background

    > CONTROLS <
        * Mouse: Click buttons and navigate menus
        * Keyboard:
            - Press any key to advance story panels
            - Enter key to submit answers in moderate / hard mode

    > FUNCTIONS <*   
        `Class Structure`
            <MathQuiz> : main game class
        `Audio Functions`
            <load_audio()> : loads all the audio
            <play_bg_music()> : plays background music for different screens
            <play_sound()> : plays sound effects like buttons, correct answer, incorrect answer, etc.
        `Graphics and UI Functions`
            <load_images()> : loads all bg, feedback, and heart images
            <set_background_img()> : sets background images on frames
            <load_and_play_gif()> : loads and prepares GIF animation
            <animate_gif()> : handles GIF frame animation
            <stop_gif()> : stops GIF animations
            <show_feedback_img()> : displays character feedback images
            <show_feedback()> : shows feedback with auto reset
            <update_hearts_display()> : creates heart display frame
            <update_heart_img()> : updates heart images based on the lives left
        ``Game Flow Functions`
            <main_menu_loader()> : creates main menu with GIF bg
            <create_mode_buttons()> : creates difficulty selection buttons
            <start_story()> : initializes story mode
            <stop_all_timers()> : stops all running timers
        `Story Progression Functions`
            <show_easy_story()> : manages easy mode story flow
            <show_moderate_story()> : manages moderate mode story flow
            <show_hard_story()> : manages hard mode story flow
            <show_story_frame()> : displays story panels
            <handle_key_press()> : handles key presses to advance thru the narration
        `Quiz Functions`
            <start_easy_quiz()> : initializes easy quiz
            <start_moderate_quiz_part1/2/3()> : start moderate mode quiz parts
            <start_hard_quiz()> : starts hard quiz
            <create_quiz_screen()> : creates quiz interface
            <create_mcq_interface()> : creates multiple-choice buttons
            <create_entry_interface()> : creates text entry interface
            <generate_question()> : generates random math ques
            <generate_choices()> : generates multiple-choice options
        `Timer Functions`
            <start_mod_timer()> : starts moderate mode timer
            <update_mod_timer()> : updates moderate timer display
            <mod_time_out()> : handles moderate timer expiration
            <start_hard_timer()> : starts hard mode timer
            <update_hard_timer()> : updates the hard timer display
            <hard_time_out()> : handles hard timer expiration
        `Answer Checking Functions`
            <check_choice()> : checks multiple-choice answers
            <check_ans_entry()> : checks text entry answers
            <next_ques()> : advances to next question or ends quiz
        `End Game Functions`
            <show_easy_ending()> : easy mode ending screen
            <show_mod_ending()> : moderate mode ending screen
            <show_hard_ending()> : hard mode ending screen
            <show_ending_screen()> : generic ending screen which displays the final score and grade
            <game_over()> : handles game over state
            <continue_story()> : continues story after quiz completion
        `Utility Functions`
            <center_window()> : centers the application window
            <create_mode_buttons()> : creates main menu buttons
