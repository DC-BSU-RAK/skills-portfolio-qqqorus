import os
from tkinter import *
from tkinter import ttk, messagebox, font as tkfont
from dataclasses import dataclass
from pathlib import Path

# data modeling
@dataclass
class Student:
    code: int # int for id number
    name: str # string for name
    cw1: int # int for classwork marks
    cw2: int
    cw3: int
    exam: int # int for exam marks

    @property
    def coursework_total(self) -> int:
        return self.cw1 + self.cw2 + self.cw3

    @property
    def overall_total(self) -> int:
        return self.coursework_total + self.exam

    @property
    def percentage(self) -> float:
        return (self.overall_total / 160) * 100

    @property
    def grade(self) -> str:
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

# create class for the app
class StudentManagerApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title('Student Manager')
        self.root.geometry('1200x700')
        self.root.resizable(0, 0)
        self.root.iconbitmap(r'.\img\logo.ico')

        # App colours
        self.BG_MAIN = '#f3f4f6'
        self.BG_SIDEBAR = '#111827'
        self.BG_SIDEBAR_BTN_ACTIVE = '#10b981'
        self.BG_SIDEBAR_BTN_INACTIVE = '#1f2933'
        self.BG_CARD = '#ffffff'
        self.CARD_BORDER = '#e5e7eb'
        self.TEXT_PRIMARY = '#111827'
        self.TEXT_MUTED = '#6b7280'

        self.root.configure(bg=self.BG_MAIN)

        # global font setup
        self.base_font_family = self._choose_font_family()
        self._configure_default_fonts()

        # data
        self.students: list[Student] = []
        self.highest_student: Student | None = None
        self.lowest_student: Student | None = None

        # placeholders for widgets that need cross-method access
        self.center_frame = None
        self.center_title_var = None
        self.highest_txt = None
        self.lowest_txt = None
        self.students_btn = None
        self.individual_btn = None

        # layout
        self._load_data()
        self._build_layout()
        self.set_active_sidebar("students")
        self.students_page()
        # highest/lowest start blank on purpose

    # functions for fonts
    def _choose_font_family(self) -> str:
        """
        Try Quicksand, then Century Gothic, else fall back to TkDefaultFont's family.
        """
        families = set(tkfont.families())
        if "Quicksand" in families:
            return "Quicksand"
        if "Century Gothic" in families:
            return "Century Gothic"
        # fallback
        default = tkfont.nametofont("TkDefaultFont")
        return default.cget("family")

    # default fonts configuration
    def _configure_default_fonts(self):
        """
        Override Tk default fonts so everything uses the chosen family
        unless explicitly changed.
        """
        for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont",
                     "TkHeadingFont", "TkFixedFont", "TkIconFont",
                     "TkTooltipFont"):
            f = tkfont.nametofont(name)
            size = f.cget("size")
            weight = f.cget("weight")
            slant = f.cget("slant")
            underline = f.cget("underline")
            overstrike = f.cget("overstrike")
            f.configure(family=self.base_font_family, size=size,
                        weight=weight, slant=slant,
                        underline=underline, overstrike=overstrike)

    # load data from studentMarks.txt
    def _load_data(self):
        """
        Load students from studentMarks.txt into self.students.
        """
        self.students = self.load_students("studentMarks.txt")
    
    @staticmethod
    def load_students(filename: str) -> list[Student]:
        """
        Read studentMarks.txt and return a list of Student objects.
        File format:
            first line: number of students (can be ignored safely)
            remaining lines: code,name,cw1,cw2,cw3,exam
        """
        path = Path(filename)
        if not path.exists():
            raise FileNotFoundError(f"{filename} not found")

        students: list[Student] = []
        with path.open("r", encoding="utf-8") as f:
            first = f.readline().strip()
            # If the first line isn't a count, treat it as data
            _ = int(first)

            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 6:
                    continue

                code = int(parts[0])
                name = parts[1]
                cw1, cw2, cw3, exam = map(int, parts[2:])
                students.append(Student(code, name, cw1, cw2, cw3, exam))

        return students

    def _build_layout(self):
        """
        Build all the fixed layout frames:
          - sidebar
          - center column and title
          - center card
          - right column with highest/lowest cards
        """
        # left sidebar frame
        options_frame = Frame(self.root, bg=self.BG_SIDEBAR)
        options_frame.pack(side=LEFT, fill=Y)
        options_frame.pack_propagate(False)
        options_frame.configure(width=180, height=700)

        # center "card" frame
        center_outer = Frame(self.root, bg=self.BG_MAIN)
        center_outer.pack(side=LEFT, fill=BOTH, expand=True)
        center_outer.pack_propagate(False)
        center_outer.configure(width=640, height=700)


# execution in main page
if __name__ == "__main__":
    app = StudentManagerApp()
    app.run()