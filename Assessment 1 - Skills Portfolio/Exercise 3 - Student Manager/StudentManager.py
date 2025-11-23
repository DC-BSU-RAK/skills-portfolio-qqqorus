from tkinter import *
from tkinter import ttk, messagebox, font as tkfont
from dataclasses import dataclass
from pathlib import Path
from PIL import ImageTk, Image

# ---------------------- Data Model ---------------------- #

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

        self.root.configure(bg=self.BG_MAIN)
    
        self.base_font = self.choose_font_family()

        self.students = []
        self.highest_student = None
        self.lowest_student = None

        self.center_frame = None
        self.center_title_var = None
        self.students_btn = None
        self.individual_btn = None
        self.totalscores_btn = None

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
        self.totalscores_btn = Button(sidebar, text="Min-Max Scores     ",
            font=(self.base_font, 10, "bold"), anchor='e',
            fg="#d1d5db", bg=self.BG_SIDEBAR_BTN_INACTIVE,
            bd=0, width=btn_width, height=btn_height,
            command=lambda: [self.set_active_sidebar("totalscores"), self.totalscores_page()])
        self.totalscores_btn.place(x=15, y=200)

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

if __name__ == "__main__":
    root = Tk()
    app = StudentManagerApp(root)
    root.mainloop()