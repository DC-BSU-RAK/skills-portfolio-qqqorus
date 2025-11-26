from tkinter import *
from tkinter import ttk, messagebox, font as tkfont
from dataclasses import dataclass
from pathlib import Path
from PIL import ImageTk, Image

# data model 
@dataclass
class Student:
    code: int # int for id number
    name: str # string for name
    cw1: int # int for classwork marks
    cw2: int
    cw3: int
    exam: int # int for exam marks

    @property
    def coursework_total(self): # calculate the total marks for courseworks
        return self.cw1 + self.cw2 + self.cw3

    @property
    def overall_total(self): # total marks for everything
        return self.coursework_total + self.exam

    @property
    def percentage(self): # calculate the percentage
        return (self.overall_total / 160) * 100

    @property
    def grade(self): # assigns grades based on marks
        p = self.percentage
        if p >= 70:
            return "A"
        elif p >= 60:
            return "B"
        elif p >= 50:
            return "C"
        elif p >= 40:
            return "D"
        else:
            return "F"


class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("950x650")
        self.root.resizable(0, 0)
        self.root.iconbitmap(r'.\img\logo.ico')

        self.BG_MAIN = "#ffffff" # color of the main bg
        self.BG_SIDEBAR = "#252525" # bg color of the sidebar
        self.BG_SIDEBAR_BTN_ACTIVE = "#2a4a3d" # bg color of the active button
        self.BG_SIDEBAR_BTN_INACTIVE = "#252525" # bg color of the inactive button
        self.BG_CARD = "#f3f4f6" # bg color of the cards
        self.CARD_BORDER = "#e8e8e8" # color of the borders
        self.TEXT_PRIMARY = "#252525" # primary text color
        self.TEXT_MUTED = "#6b7280" # text color if it's muted
        self.ACCENT_GREEN = "#b6c58c"  # existing accent color
        self.ACCENT_GREEN_LIGHT = "#d4e0b1"
        self.ACCENT_GREEN_DARK = "#8a9c5f"
        self.HIGHLIGHT_COLOR = "#e8f4f1"
        self.SUCCESS_COLOR = "#10b981"
        self.WARNING_COLOR = "#f59e0b"
        self.ERROR_COLOR = "#ef4444"

        self.root.configure(bg=self.BG_MAIN)
    
        self.base_font = self.choose_font_family()

        self.students = []
        self.highest_student = None
        self.lowest_student = None

        self.center_frame = None
        self.center_title_var = None
        self.students_btn = None
        self.individual_btn = None
        self.minmax_btn = None

        self.load_data()
        self.build_layout()
        self.set_active_sidebar("students")
        self.students_page()
    
    # uses century gothic as the font family for all
    def choose_font_family(self):
        families = tkfont.families()
        if "Century Gothic" in families:
            return "Century Gothic"
        return tkfont.nametofont("TkDefaultFont").cget("family")

    # function to load data from studentMarks.txt
    def load_data(self):
        path = Path("studentMarks.txt")
        students = [] # stores the student's info in this list
        with path.open("r", encoding="utf-8") as f:
            first = f.readline().strip() # read line by line
            _ = int(first)

            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")] # splits the words separated by a comma
                if len(parts) != 6:
                    continue
                code = int(parts[0])
                name = parts[1]
                cw1, cw2, cw3, exam = map(int, parts[2:])
                students.append(Student(code, name, cw1, cw2, cw3, exam))

        self.students = students

    # function to build the main layout which will be applied to all frames
    def build_layout(self):
        # sidebar
        sidebar = Frame(self.root, bg=self.BG_SIDEBAR, width=500, height=650)
        sidebar.place(x=0, y=0)

        # load and resize logo
        logo = Image.open(r'.\img\logo.png')
        logoresize = logo.resize((30, 30))
        avianlogo = ImageTk.PhotoImage(logoresize)
        
        # store the image reference to prevent garbage collection
        self.title_logo_image = avianlogo
        
        # logo on the left of the title
        title_logo = Label(sidebar, image=avianlogo, bg=self.BG_SIDEBAR)
        title_logo.place(x=20, y=35)

        # title text beside the logo
        title_label1 = Label(sidebar, text="Avian",
            font=(self.base_font, 16, "bold"),
            bg=self.BG_SIDEBAR, fg="#b6c58c", justify=LEFT)
        title_label1.place(x=60, y=27)  # x position adjusted to be right of logo
        
        title_label2 = Label(sidebar, text="UNIVERSITY",
            font=(self.base_font, 12, "bold"),
            bg=self.BG_SIDEBAR, fg="#ffffff", justify=LEFT)
        title_label2.place(x=60, y=50)  # same x position, different y

        # predeclared values for the button width and height
        btn_width = 20
        btn_height = 2

        # navigation buttons
        # student records button is active
        self.students_btn = Button(sidebar, text="Student Records     ",
            font=(self.base_font, 10, "bold"),
            fg="#ffffff", bg=self.BG_SIDEBAR_BTN_ACTIVE,
            bd=0, width=btn_width, height=btn_height, anchor='e',
            command=lambda: [self.set_active_sidebar("students"), self.students_page()])
        self.students_btn.place(x=15, y=100)

        # individual records button is inactive
        self.individual_btn = Button(sidebar, text="Individual Records     ",
            font=(self.base_font, 10, "bold"),
            fg="#d1d5db", bg=self.BG_SIDEBAR_BTN_INACTIVE,
            bd=0, width=btn_width, height=btn_height, anchor='e',
            command=lambda: [self.set_active_sidebar("individual"), self.individual_page()])
        self.individual_btn.place(x=15, y=150)

        # minimum and maximum scores button (frame for the highest and lowest score) is inactive
        self.minmax_btn = Button(sidebar, text="Min-Max Scores     ",
            font=(self.base_font, 10, "bold"), anchor='e',
            fg="#d1d5db", bg=self.BG_SIDEBAR_BTN_INACTIVE,
            bd=0, width=btn_width, height=btn_height,
            command=lambda: [self.set_active_sidebar("minmax"), self.minmax_page()])
        self.minmax_btn.place(x=15, y=200)

        # center area displaying the main content
        center_outer = Frame(self.root, bg=self.BG_MAIN, width=900, height=650)
        center_outer.place(x=180, y=0)

        self.center_title_var = StringVar()
        self.center_title_var.set("Student Records")

        title_lbl = Label(center_outer, textvariable=self.center_title_var,
            font=(self.base_font, 16, "bold"),
            bg=self.BG_MAIN, fg=self.TEXT_PRIMARY)
        title_lbl.place(x=20, y=15)

        # frame containing the students records
        self.center_frame = Frame(center_outer, bg=self.BG_CARD,
            highlightbackground=self.CARD_BORDER, highlightthickness=1,
            width=730, height=570)
        self.center_frame.place(x=20, y=60)
    
    # clear center for every new frame
    def clear_center(self):
        for widget in self.center_frame.winfo_children():
            widget.destroy()


    def format_student_card(self, student, parent_frame=None):
        # format student info as a compact card with individual marks
        if parent_frame is None:
            parent_frame = self.center_frame
        
        grade_color = {
            "A": "green",
            "B": "blue",
            "C": "#fce80a",  # yellow
            "D": "orange",
            "F": "red" 
        }
        
        card_frame = Frame(parent_frame, bg="#f8fafc",
            relief=RAISED, bd=1, width=300, height=120)
        
        # name and ID
        name_label = Label(card_frame, text=f"{student.name}",
            font=(self.base_font, 9, "bold"),
            bg="#f8fafc", fg=self.TEXT_PRIMARY, anchor="w")
        name_label.place(x=10, y=8)
        
        id_label = Label(card_frame, text=f"ID: {student.code}",
            font=(self.base_font, 8),
            bg="#f8fafc", fg=self.TEXT_MUTED, anchor="w")
        id_label.place(x=10, y=25)
        
        # individual coursework marks
        marks_label = Label(card_frame, text=f"Marks: {student.cw1}, {student.cw2}, {student.cw3}",
            font=(self.base_font, 8),
            bg="#f8fafc", fg=self.TEXT_MUTED, anchor="w")
        marks_label.place(x=10, y=42)
        
        # coursework total and exam
        coursework_label = Label(card_frame, text=f"CW Total: {student.coursework_total}/60",
            font=(self.base_font, 8),
            bg="#f8fafc", fg=self.TEXT_PRIMARY, anchor="w")
        coursework_label.place(x=10, y=59)
        
        exam_label = Label(card_frame, text=f"Exam: {student.exam}/100",
            font=(self.base_font, 8),
            bg="#f8fafc", fg=self.TEXT_PRIMARY, anchor="w")
        exam_label.place(x=10, y=76)
        
        # overall total and percentage
        total_label = Label(card_frame, text=f"Total: {student.overall_total}/160",
            font=(self.base_font, 9, "bold"),
            bg="#f8fafc", fg=self.TEXT_PRIMARY, anchor="w")
        total_label.place(x=120, y=42)
        
        percent_label = Label(card_frame, text=f"{student.percentage:.1f}%",
            font=(self.base_font, 9, "bold"),
            bg="#f8fafc", fg=self.TEXT_PRIMARY, anchor="w")
        percent_label.place(x=120, y=59)
        
        # grade with color coding
        grade_label = Label(card_frame, text=student.grade,
            font=(self.base_font, 12, "bold"),
            bg=grade_color[student.grade], fg="white", width=3)
        grade_label.place(x=230, y=35)
        
        return card_frame

    # main container for the student cards
    def students_page(self):
        self.clear_center()
        self.center_title_var.set("Student Records")

        # title
        title = Label(self.center_frame, text="All Students - Detailed View",
            font=(self.base_font, 12, "bold"),
            bg=self.BG_CARD, fg=self.TEXT_PRIMARY)
        title.place(x=30, y=20)

        # create scrollable frame for cards
        canvas = Canvas(self.center_frame, bg=self.BG_CARD, highlightthickness=0, width=650, height=500)
        scrollbar = Scrollbar(self.center_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=self.BG_CARD)

        # make it scrollable 
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # pPsition canvas and scrollbar properly
        canvas.place(x=40, y=60, width=650, height=500)
        scrollbar.place(x=690, y=60, height=500)  # Adjusted x position

        # bind mouse wheel event for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        # add student cards in grid layout
        row, col = 0, 0
        for student in self.students:
            card = self.format_student_card(student, scrollable_frame)
            card.grid(row=row, column=col, padx=10, pady=10, in_=scrollable_frame)  # use grid instead of place
            
            col += 1
            if col >= 2:  # 2 columns
                col = 0
                row += 1

        # update scroll region after adding all cards
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # summary of the card info
        count = len(self.students)
        avg_percentage = sum(s.percentage for s in self.students) / count if count else 0
        
        summary = Label(self.center_frame, text=f"Total Students: {count} | Average: {avg_percentage:.1f}%",
            font=(self.base_font, 10),
            bg=self.BG_CARD, fg=self.TEXT_MUTED)
        summary.place(x=450, y=20)

    # individual record page to find a student
    def individual_page(self):
        self.clear_center()
        self.center_title_var.set("Individual Record")

        # title
        title = Label(self.center_frame, text="Find Student",
            font=(self.base_font, 12, "bold"),
            bg=self.BG_CARD, fg=self.TEXT_PRIMARY)
        title.place(x=20, y=15)

        # search label
        search_lbl = Label(self.center_frame, text="Student ID or Name:",
            font=(self.base_font, 10),
            bg=self.BG_CARD, fg=self.TEXT_MUTED)
        search_lbl.place(x=20, y=50)

        # search entry
        self.search_var = StringVar()
        search_entry = Entry(self.center_frame, textvariable=self.search_var,
            font=(self.base_font, 10), width=30)
        search_entry.place(x=180, y=50)
        search_entry.bind('<Return>', lambda e: self.do_search()) # may use return to search

        # search button
        search_btn = Button(self.center_frame, text="Search",
            font=(self.base_font, 9, "bold"),
            bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="#ecfdf5",
            bd=0, padx=12, pady=4, command=self.do_search)
        search_btn.place(x=420, y=48)

        # results frame
        self.result_frame = Frame(self.center_frame,
            bg="#f8fafc", relief=RAISED, bd=1)
        self.result_frame.place(x=20, y=90, width=680, height=450)

        # rnitial message beforre showing the result
        initial_msg = Label(self.result_frame, text="Enter student ID or name above to search",
            font=(self.base_font, 10),
            bg="#f8fafc", fg=self.TEXT_MUTED)
        initial_msg.place(relx=0.5, rely=0.5, anchor="center")

    # page to display the highest and lowest scores
    def minmax_page(self):
        self.clear_center()
        self.center_title_var.set("Minimum and Maximum Scores")
        
        self.compute_highest_lowest()

        # title
        title = Label(self.center_frame, text="Performance Overview",
            font=(self.base_font, 12, "bold"),
            bg=self.BG_CARD, fg=self.TEXT_PRIMARY)
        title.place(x=40, y=20)

        # highest score card
        high_frame = Frame(self.center_frame, bg="#e8f5e8",
            relief=RAISED, bd=1, width=650, height=150)
        high_frame.place(x=40, y=60)

        high_title = Label(high_frame, text="🏆 HIGHEST SCORE",
            font=(self.base_font, 12, "bold"),
            bg="#e8f5e8", fg="#065f46")
        high_title.place(x=20, y=15)

        if self.highest_student:
            high_name = Label(high_frame, text=f"Name: {self.highest_student.name}",
                font=(self.base_font, 10, "bold"),
                bg="#e8f5e8", fg=self.TEXT_PRIMARY)
            high_name.place(x=20, y=45)
            
            high_id = Label(high_frame, text=f"ID: {self.highest_student.code}",
                font=(self.base_font, 10),
                bg="#e8f5e8", fg=self.TEXT_MUTED)
            high_id.place(x=20, y=65)
            
            # individual marks
            high_marks = Label(high_frame, text=f"Coursework: {self.highest_student.cw1}, {self.highest_student.cw2}, {self.highest_student.cw3}",
                font=(self.base_font, 9),
                bg="#e8f5e8", fg=self.TEXT_MUTED)
            high_marks.place(x=20, y=85)
            
            high_cw_total = Label(high_frame, text=f"CW Total: {self.highest_student.coursework_total}/60",
                font=(self.base_font, 9),
                bg="#e8f5e8", fg=self.TEXT_PRIMARY)
            high_cw_total.place(x=20, y=105)
            
            high_exam = Label(high_frame, text=f"Exam: {self.highest_student.exam}/100",
                font=(self.base_font, 9),
                bg="#e8f5e8", fg=self.TEXT_PRIMARY)
            high_exam.place(x=150, y=105)
            
            high_score = Label(high_frame, text=f"Total Score: {self.highest_student.overall_total}/160",
                font=(self.base_font, 10, "bold"),
                bg="#e8f5e8", fg="#065f46")
            high_score.place(x=300, y=45)
            
            high_percent = Label(high_frame, text=f"Percentage: {self.highest_student.percentage:.1f}%",
                font=(self.base_font, 10),
                bg="#e8f5e8", fg=self.TEXT_PRIMARY)
            high_percent.place(x=300, y=65)
            
            high_grade = Label(high_frame, text=f"Grade: {self.highest_student.grade}",
                font=(self.base_font, 14, "bold"),
                bg="#10b981", fg="white", width=10)
            high_grade.place(x=500, y=60)

        # lowest Score Card
        low_frame = Frame(self.center_frame, bg="#f8e8e8",
            relief=RAISED, bd=1, width=650, height=150)
        low_frame.place(x=40, y=230)

        low_title = Label(low_frame, text="📉 LOWEST SCORE",
            font=(self.base_font, 12, "bold"),
            bg="#f8e8e8", fg="#7f1d1d")
        low_title.place(x=20, y=15)

        if self.lowest_student:
            low_name = Label(low_frame, text=f"Name: {self.lowest_student.name}",
                font=(self.base_font, 10, "bold"),
                bg="#f8e8e8", fg=self.TEXT_PRIMARY)
            low_name.place(x=20, y=45)
            
            low_id = Label(low_frame, text=f"ID: {self.lowest_student.code}",
                font=(self.base_font, 10),
                bg="#f8e8e8", fg=self.TEXT_MUTED)
            low_id.place(x=20, y=65)
            
            # individual marks
            low_marks = Label(low_frame, text=f"Coursework: {self.lowest_student.cw1}, {self.lowest_student.cw2}, {self.lowest_student.cw3}",
                font=(self.base_font, 9),
                bg="#f8e8e8", fg=self.TEXT_MUTED)
            low_marks.place(x=20, y=85)
            
            low_cw_total = Label(low_frame, text=f"CW Total: {self.lowest_student.coursework_total}/60",
                font=(self.base_font, 9),
                bg="#f8e8e8", fg=self.TEXT_PRIMARY)
            low_cw_total.place(x=20, y=105)
            
            low_exam = Label(low_frame, text=f"Exam: {self.lowest_student.exam}/100",
                font=(self.base_font, 9),
                bg="#f8e8e8", fg=self.TEXT_PRIMARY)
            low_exam.place(x=150, y=105)
            
            low_score = Label(low_frame, text=f"Total Score: {self.lowest_student.overall_total}/160",
                font=(self.base_font, 10, "bold"),
                bg="#f8e8e8", fg="#7f1d1d")
            low_score.place(x=300, y=45)
            
            low_percent = Label(low_frame, text=f"Percentage: {self.lowest_student.percentage:.1f}%",
                font=(self.base_font, 10),
                bg="#f8e8e8", fg=self.TEXT_PRIMARY)
            low_percent.place(x=300, y=65)
            
            low_grade = Label(low_frame, text=f"Grade: {self.lowest_student.grade}",
                font=(self.base_font, 14, "bold"),
                bg="#ef4444", fg="white", width=10)
            low_grade.place(x=500, y=60)

        # statistics
        stats_frame = Frame(self.center_frame, bg="#f0f9ff",
            relief=RAISED, bd=1, width=650, height=120)
        stats_frame.place(x=40, y=410)

        stats_title = Label(stats_frame, text="📊 CLASS STATISTICS",
            font=(self.base_font, 11, "bold"),
            bg="#f0f9ff", fg="#0369a1")
        stats_title.place(x=20, y=15)

        if self.students:
            count = len(self.students)
            avg_percent = sum(s.percentage for s in self.students) / count
            grade_counts = {}
            for s in self.students:
                grade_counts[s.grade] = grade_counts.get(s.grade, 0) + 1
            
            total_label = Label(stats_frame, text=f"Total Students: {count}",
                font=(self.base_font, 10),
                bg="#f0f9ff", fg=self.TEXT_PRIMARY)
            total_label.place(x=20, y=45)
            
            avg_label = Label(stats_frame, text=f"Class Average: {avg_percent:.1f}%",
                font=(self.base_font, 10),
                bg="#f0f9ff", fg=self.TEXT_PRIMARY)
            avg_label.place(x=200, y=45)
            
            grades_label = Label(stats_frame, text="Grade Distribution:",
                font=(self.base_font, 10, "bold"),
                bg="#f0f9ff", fg=self.TEXT_PRIMARY)
            grades_label.place(x=20, y=75)
            
            # grade counts in a row
            x_pos = 150
            for grade in "ABCDEF":
                if grade in grade_counts:
                    grade_label = Label(
                        stats_frame,
                        text=f"{grade}: {grade_counts[grade]}",
                        font=(self.base_font, 10),
                        bg="#f0f9ff",
                        fg=self.TEXT_PRIMARY
                    )
                    grade_label.place(x=x_pos, y=75)
                    x_pos += 60

    # function that activates the searching
    def do_search(self):
        query = self.search_var.get().strip().lower() # gets the keyword close to the names or ids
        if not query:
            messagebox.showinfo("Search", "Enter a student ID or name.")
            return

        found = None
        for s in self.students:
            if query == str(s.code).lower() or query in s.name.lower():
                found = s
                break

        # clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # text display if no student is found
        if found is None:
            not_found = Label(self.result_frame, text=f"No student found for: '{query}'",
                font=(self.base_font, 10),
                bg="#f8fafc", fg=self.TEXT_MUTED)
            not_found.place(relx=0.5, rely=0.5, anchor="center")
        else:
            # create a detailed student card for search results
            detailed_card = Frame(self.result_frame, bg="#ffffff",
                relief=RAISED, bd=1, width=450, height=180)
            detailed_card.place(relx=0.5, rely=0.5, anchor="center")
            
            # student name and ID
            name_label = Label(detailed_card, text=found.name,
                font=(self.base_font, 12, "bold"),
                bg="#ffffff", fg='#2a4a3d')
            name_label.place(x=20, y=20)
            
            id_label = Label(detailed_card, text=f"ID: {found.code}",
                font=(self.base_font, 10),
                bg="#ffffff", fg=self.TEXT_MUTED)
            id_label.place(x=20, y=45)
            
            # individual marks
            marks_label = Label(detailed_card, text=f"Coursework Marks: {found.cw1}, {found.cw2}, {found.cw3}",
                font=(self.base_font, 10),
                bg="#ffffff", fg=self.TEXT_PRIMARY)
            marks_label.place(x=20, y=70)
            
            cw_total_label = Label(detailed_card, text=f"Coursework Total: {found.coursework_total}/60",
                font=(self.base_font, 10),
                bg="#ffffff", fg=self.TEXT_PRIMARY)
            cw_total_label.place(x=20, y=95)
            
            exam_label = Label(detailed_card, text=f"Exam Mark: {found.exam}/100",
                font=(self.base_font, 10),
                bg="#ffffff", fg=self.TEXT_PRIMARY)
            exam_label.place(x=20, y=120)
            
            # overall performance
            total_label = Label(detailed_card, text=f"Overall Total: {found.overall_total}/160",
                font=(self.base_font, 10, "bold"),
                bg="#ffffff", fg=self.TEXT_PRIMARY)
            total_label.place(x=230, y=70)
            
            percent_label = Label(detailed_card, text=f"Percentage: {found.percentage:.1f}%",
                font=(self.base_font, 10, "bold"),
                bg="#ffffff", fg=self.TEXT_PRIMARY)
            percent_label.place(x=230, y=95)
            
            # grade with color
            grade_color = {
                "A": "green", "B": "blue", "C": "#fce80a", 
                "D": "orange", "F": "red"
            }
            grade_label = Label(detailed_card, text=f"Grade: {found.grade}",
                font=(self.base_font, 14, "bold"),
                bg=grade_color[found.grade], fg="white", width=10)
            grade_label.place(x=230, y=120)

    # computes the highest and lowest grades using min and max
    def compute_highest_lowest(self):
        if not self.students:
            self.highest_student = None
            self.lowest_student = None
            return
        self.highest_student = max(self.students, key=lambda s: s.overall_total)
        self.lowest_student = min(self.students, key=lambda s: s.overall_total)

    # links the sidebar buttons to tabs they belong to
    def set_active_sidebar(self, which):
        buttons = [self.students_btn, self.individual_btn, self.minmax_btn]
        for btn in buttons:
            btn.configure(bg=self.BG_SIDEBAR_BTN_INACTIVE, fg="#d1d5db")
        
        if which == "students":
            self.students_btn.configure(bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="#ecfdf5")
        elif which == "individual":
            self.individual_btn.configure(bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="#ecfdf5")
        elif which == "minmax":
            self.minmax_btn.configure(bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="#ecfdf5")

# root
if __name__ == "__main__":
    root = Tk()
    app = StudentManagerApp(root)
    root.mainloop()