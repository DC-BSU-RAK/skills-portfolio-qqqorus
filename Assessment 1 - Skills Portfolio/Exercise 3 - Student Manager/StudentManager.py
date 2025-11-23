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

if __name__ == "__main__":
    root = Tk()
    app = StudentManagerApp(root)
    root.mainloop()