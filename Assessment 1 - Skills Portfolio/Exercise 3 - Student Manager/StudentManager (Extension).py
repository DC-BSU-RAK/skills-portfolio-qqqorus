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
        self.highest_btn = None
        self.lowest_btn = None
        self.sort_btn = None
        self.add_btn = None
        self.delete_btn = None
        self.update_btn = None

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

    # function to save data to studentMarks.txt
    def save_data(self):
        path = Path("studentMarks.txt")
        with path.open("w", encoding="utf-8") as f:
            f.write(f"{len(self.students)}\n")
            for student in self.students:
                f.write(f"{student.code},{student.name},{student.cw1},{student.cw2},{student.cw3},{student.exam}\n")
        return True

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

        # highest score button
        self.highest_btn = Button(sidebar, text="Highest Score     ",
            font=(self.base_font, 10, "bold"), anchor='e',
            fg="#d1d5db", bg=self.BG_SIDEBAR_BTN_INACTIVE,
            bd=0, width=btn_width, height=btn_height,
            command=self.show_highest_score)
        self.highest_btn.place(x=15, y=200)

        # lowest score button
        self.lowest_btn = Button(sidebar, text="Lowest Score     ",
            font=(self.base_font, 10, "bold"), anchor='e',
            fg="#d1d5db", bg=self.BG_SIDEBAR_BTN_INACTIVE,
            bd=0, width=btn_width, height=btn_height,
            command=self.show_lowest_score)
        self.lowest_btn.place(x=15, y=250)

        # sort button
        self.sort_btn = Button(sidebar, text="Sort Records     ",
            font=(self.base_font, 10, "bold"), anchor='e',
            fg="#d1d5db", bg=self.BG_SIDEBAR_BTN_INACTIVE,
            bd=0, width=btn_width, height=btn_height,
            command=self.sort_students_dialog)
        self.sort_btn.place(x=15, y=300)

        # add button
        self.add_btn = Button(sidebar, text="Add Student     ",
            font=(self.base_font, 10, "bold"), anchor='e',
            fg="#d1d5db", bg=self.BG_SIDEBAR_BTN_INACTIVE,
            bd=0, width=btn_width, height=btn_height,
            command=self.add_student_dialog)
        self.add_btn.place(x=15, y=350)

        # delete button
        self.delete_btn = Button(sidebar, text="Delete Student     ",
            font=(self.base_font, 10, "bold"), anchor='e',
            fg="#d1d5db", bg=self.BG_SIDEBAR_BTN_INACTIVE,
            bd=0, width=btn_width, height=btn_height,
            command=self.delete_student_dialog)
        self.delete_btn.place(x=15, y=400)

        # update button
        self.update_btn = Button(sidebar, text="Update Student     ",
            font=(self.base_font, 10, "bold"), anchor='e',
            fg="#d1d5db", bg=self.BG_SIDEBAR_BTN_INACTIVE,
            bd=0, width=btn_width, height=btn_height,
            command=self.update_student_dialog)
        self.update_btn.place(x=15, y=450)

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

        # position canvas and scrollbar properly
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

        # initial message beforre showing the result
        initial_msg = Label(self.result_frame, text="Enter student ID or name above to search",
            font=(self.base_font, 10),
            bg="#f8fafc", fg=self.TEXT_MUTED)
        initial_msg.place(relx=0.5, rely=0.5, anchor="center")

    # show highest score in custom dialog
    def show_highest_score(self):
        self.compute_highest_lowest()
        if not self.highest_student:
            messagebox.showinfo("Highest Score", "No student records found.")
            return
        
        student = self.highest_student
        self.show_student_dialog("HIGHEST SCORE", student)

    # show lowest score in custom dialog
    def show_lowest_score(self):
        self.compute_highest_lowest()
        if not self.lowest_student:
            messagebox.showinfo("Lowest Score", "No student records found.")
            return
        
        student = self.lowest_student
        self.show_student_dialog("LOWEST SCORE", student)

    # custom dialog to show student information with Century Gothic font
    def show_student_dialog(self, title, student):
        dialog = Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x350")  # slightly larger for better spacing
        dialog.resizable(0, 0)
        dialog.configure(bg=self.BG_MAIN)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.iconbitmap(r'.\img\logo.ico')

        # center the window
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # header with accent color
        header_frame = Frame(dialog, bg=self.ACCENT_GREEN_DARK, height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # title in header
        title_label = Label(header_frame, text=title,
            font=(self.base_font, 16, "bold"),
            bg=self.ACCENT_GREEN_DARK, fg="white")
        title_label.place(relx=0.5, rely=0.5, anchor="center")

        # content frame
        content_frame = Frame(dialog, bg=self.BG_MAIN)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # student info with better styling
        name_label = Label(content_frame, 
            text=f"{student.name}",
            font=(self.base_font, 14, "bold"),
            bg=self.BG_MAIN, fg=self.TEXT_PRIMARY)
        name_label.place(x=10, y=10)

        id_label = Label(content_frame,
            text=f"ID: {student.code}",
            font=(self.base_font, 11),
            bg=self.BG_MAIN, fg=self.TEXT_MUTED)
        id_label.place(x=10, y=35)

        # marks in a nicely formatted box
        marks_frame = Frame(content_frame, bg=self.HIGHLIGHT_COLOR, relief=SOLID, bd=1)
        marks_frame.place(x=10, y=70, width=340, height=100)

        marks_text = f"Coursework: {student.cw1}, {student.cw2}, {student.cw3}\n" \
                    f"Coursework Total: {student.coursework_total}/60\n" \
                    f"Exam: {student.exam}/100\n" \
                    f"Overall: {student.overall_total}/160 ({student.percentage:.1f}%)"

        marks_label = Label(marks_frame, text=marks_text,
            font=(self.base_font, 9),
            bg=self.HIGHLIGHT_COLOR, fg=self.TEXT_PRIMARY, justify=LEFT)
        marks_label.place(x=10, y=10)

        # grade with prominent display
        grade_color = {
            "A": self.SUCCESS_COLOR, "B": "#3b82f6", "C": self.WARNING_COLOR,
            "D": "#f97316", "F": self.ERROR_COLOR
        }
        
        grade_frame = Frame(content_frame, bg=grade_color[student.grade], relief=RAISED, bd=1)
        grade_frame.place(x=280, y=10, width=70, height=50)
        
        grade_label = Label(grade_frame, text=f"GRADE\n{student.grade}",
            font=(self.base_font, 11, "bold"),
            bg=grade_color[student.grade], fg="white", justify=CENTER)
        grade_label.place(relx=0.5, rely=0.5, anchor="center")

        # close button
        close_btn = Button(content_frame, text="Close",
            font=(self.base_font, 10, "bold"),
            bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="white",
            command=dialog.destroy, width=12, height=1)
        close_btn.place(x=130, y=190)

    # sort students dialog
    def sort_students_dialog(self):
        sort_window = Toplevel(self.root)
        sort_window.title("Sort Students")
        sort_window.geometry("300x250")
        sort_window.resizable(0, 0)
        sort_window.configure(bg=self.BG_MAIN)
        sort_window.transient(self.root)
        sort_window.grab_set()
        sort_window.iconbitmap(r'.\img\logo.ico')

        # center the window
        sort_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - sort_window.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - sort_window.winfo_height()) // 2
        sort_window.geometry(f"+{x}+{y}")

        Label(sort_window, text="Sort Students By:", 
              font=(self.base_font, 12, "bold"),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).pack(pady=20)

        # sort options
        sort_var = StringVar(value="name_asc")

        Radiobutton(sort_window, text="Name (A-Z)", variable=sort_var, value="name_asc",
                   font=(self.base_font, 10), bg=self.BG_MAIN).pack(anchor='w', padx=50)
        Radiobutton(sort_window, text="Name (Z-A)", variable=sort_var, value="name_desc",
                   font=(self.base_font, 10), bg=self.BG_MAIN).pack(anchor='w', padx=50)
        Radiobutton(sort_window, text="Total Score (High-Low)", variable=sort_var, value="score_desc",
                   font=(self.base_font, 10), bg=self.BG_MAIN).pack(anchor='w', padx=50)
        Radiobutton(sort_window, text="Total Score (Low-High)", variable=sort_var, value="score_asc",
                   font=(self.base_font, 10), bg=self.BG_MAIN).pack(anchor='w', padx=50)

        def apply_sort():
            self.sort_students(sort_var.get())
            sort_window.destroy()
            self.students_page()

        Button(sort_window, text="Apply Sort", 
               font=(self.base_font, 10, "bold"),
               bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="white",
               command=apply_sort).pack(pady=10)

    def sort_students(self, sort_type):
        if sort_type == "name_asc":
            self.students.sort(key=lambda s: s.name.lower())
        elif sort_type == "name_desc":
            self.students.sort(key=lambda s: s.name.lower(), reverse=True)
        elif sort_type == "score_desc":
            self.students.sort(key=lambda s: s.overall_total, reverse=True)
        elif sort_type == "score_asc":
            self.students.sort(key=lambda s: s.overall_total)
        
        if self.save_data():
            messagebox.showinfo("Success", "Students sorted and saved successfully!")

    # dialog to add students
    def add_student_dialog(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Student")
        add_window.geometry("400x400")
        add_window.resizable(0, 0)
        add_window.configure(bg=self.BG_MAIN)
        add_window.transient(self.root)
        add_window.grab_set()
        add_window.iconbitmap(r'.\img\logo.ico')

        # center the window
        add_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - add_window.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - add_window.winfo_height()) // 2
        add_window.geometry(f"+{x}+{y}")

        Label(add_window, text="Add New Student", 
              font=(self.base_font, 14, "bold"),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).pack(pady=10)

        # input fields
        input_frame = Frame(add_window, bg=self.BG_MAIN)
        input_frame.pack(pady=10)

        # student ID
        Label(input_frame, text="Student ID:", font=(self.base_font, 10),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        id_var = StringVar()
        id_entry = Entry(input_frame, textvariable=id_var, font=(self.base_font, 10))
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        # name
        Label(input_frame, text="Name:", font=(self.base_font, 10),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        name_var = StringVar()
        name_entry = Entry(input_frame, textvariable=name_var, font=(self.base_font, 10))
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        # coursework marks
        Label(input_frame, text="Coursework 1 (1-20):", font=(self.base_font, 10),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        cw1_var = StringVar()
        cw1_entry = Entry(input_frame, textvariable=cw1_var, font=(self.base_font, 10))
        cw1_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(input_frame, text="Coursework 2 (1-20):", font=(self.base_font, 10),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).grid(row=3, column=0, sticky='e', padx=5, pady=5)
        cw2_var = StringVar()
        cw2_entry = Entry(input_frame, textvariable=cw2_var, font=(self.base_font, 10))
        cw2_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(input_frame, text="Coursework 3 (1-20):", font=(self.base_font, 10),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).grid(row=4, column=0, sticky='e', padx=5, pady=5)
        cw3_var = StringVar()
        cw3_entry = Entry(input_frame, textvariable=cw3_var, font=(self.base_font, 10))
        cw3_entry.grid(row=4, column=1, padx=5, pady=5)

        # exam mark
        Label(input_frame, text="Exam Mark (1-100):", font=(self.base_font, 10),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).grid(row=5, column=0, sticky='e', padx=5, pady=5)
        exam_var = StringVar()
        exam_entry = Entry(input_frame, textvariable=exam_var, font=(self.base_font, 10))
        exam_entry.grid(row=5, column=1, padx=5, pady=5)

        def add_student():
            try:
                # validate inputs
                if not all([id_var.get(), name_var.get(), cw1_var.get(), cw2_var.get(), cw3_var.get(), exam_var.get()]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                code = int(id_var.get())
                name = name_var.get().strip()
                cw1 = int(cw1_var.get())
                cw2 = int(cw2_var.get())
                cw3 = int(cw3_var.get())
                exam = int(exam_var.get())

                # check if student ID already exists
                if any(s.code == code for s in self.students):
                    messagebox.showerror("Error", f"Student ID {code} already exists!")
                    return

                # validate mark ranges
                if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20 and 0 <= exam <= 100):
                    messagebox.showerror("Error", "Marks must be: CW1-3 (0-20), Exam (0-100)")
                    return

                # add student
                new_student = Student(code, name, cw1, cw2, cw3, exam)
                self.students.append(new_student)

                if self.save_data():
                    messagebox.showinfo("Success", f"Student {name} added successfully!")
                    add_window.destroy()
                    self.students_page()

            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for marks!")

        Button(add_window, text="Add Student", 
               font=(self.base_font, 10, "bold"),
               bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="white",
               command=add_student).pack(pady=10)

    # dialog for deleting student record
    def delete_student_dialog(self):
        delete_window = Toplevel(self.root)
        delete_window.title("Delete Student")
        delete_window.geometry("400x300")
        delete_window.resizable(0, 0)
        delete_window.configure(bg=self.BG_MAIN)
        delete_window.transient(self.root)
        delete_window.grab_set()
        delete_window.iconbitmap(r'.\img\logo.ico')

        # center the window
        delete_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - delete_window.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - delete_window.winfo_height()) // 2
        delete_window.geometry(f"+{x}+{y}")

        Label(delete_window, text="Delete Student", 
              font=(self.base_font, 14, "bold"),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).pack(pady=10)

        # search frame
        search_frame = Frame(delete_window, bg=self.BG_MAIN)
        search_frame.pack(pady=10)

        Label(search_frame, text="Student ID or Name:", font=(self.base_font, 10),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).grid(row=0, column=0, padx=5, pady=5)
        
        search_var = StringVar()
        search_entry = Entry(search_frame, textvariable=search_var, font=(self.base_font, 10), width=20)
        search_entry.grid(row=0, column=1, padx=5, pady=5)

        result_var = StringVar(value="Enter student ID or name to search")
        result_label = Label(delete_window, textvariable=result_var, font=(self.base_font, 9),
                           bg=self.BG_MAIN, fg=self.TEXT_MUTED, wraplength=350)
        result_label.pack(pady=10)

        found_student = None

        def search_student():
            nonlocal found_student
            query = search_var.get().strip().lower()
            if not query:
                result_var.set("Please enter a student ID or name")
                return

            found_student = None
            for s in self.students:
                if query == str(s.code).lower() or query in s.name.lower():
                    found_student = s
                    break

            if found_student:
                result_var.set(f"Found: {found_student.name} (ID: {found_student.code})\n"
                             f"Marks: {found_student.cw1}, {found_student.cw2}, {found_student.cw3} | "
                             f"Exam: {found_student.exam} | Total: {found_student.overall_total}/160")
            else:
                result_var.set(f"No student found for: '{query}'")

        def delete_student():
            nonlocal found_student
            if not found_student:
                messagebox.showerror("Error", "Please search and select a student first!")
                return

            if messagebox.askyesno("Confirm Delete", 
                                 f"Are you sure you want to delete {found_student.name} (ID: {found_student.code})?"):
                self.students.remove(found_student)
                if self.save_data():
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    delete_window.destroy()
                    self.students_page()

        Button(search_frame, text="Search", 
               font=(self.base_font, 9, "bold"),
               bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="white",
               command=search_student).grid(row=0, column=2, padx=5, pady=5)

        Button(delete_window, text="Delete Student", 
               font=(self.base_font, 10, "bold"),
               bg="#dc2626", fg="white",
               command=delete_student).pack(pady=10)

    # dialog to update student records
    def update_student_dialog(self):
        update_window = Toplevel(self.root)
        update_window.title("Update Student")
        update_window.geometry("500x500")
        update_window.resizable(0, 0)
        update_window.configure(bg=self.BG_MAIN)
        update_window.transient(self.root)
        update_window.grab_set()
        update_window.iconbitmap(r'.\img\logo.ico')

        # center the window
        update_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - update_window.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - update_window.winfo_height()) // 2
        update_window.geometry(f"+{x}+{y}")

        Label(update_window, text="Update Student Record", 
              font=(self.base_font, 14, "bold"),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).pack(pady=10)

        # search frame
        search_frame = Frame(update_window, bg=self.BG_MAIN)
        search_frame.pack(pady=10)

        Label(search_frame, text="Student ID or Name:", font=(self.base_font, 10),
              bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).grid(row=0, column=0, padx=5, pady=5)
        
        search_var = StringVar()
        search_entry = Entry(search_frame, textvariable=search_var, font=(self.base_font, 10), width=20)
        search_entry.grid(row=0, column=1, padx=5, pady=5)

        result_var = StringVar(value="Enter student ID or name to search")
        result_label = Label(update_window, textvariable=result_var, font=(self.base_font, 9),
                           bg=self.BG_MAIN, fg=self.TEXT_MUTED, wraplength=450)
        result_label.pack(pady=10)

        found_student = None
        input_frame = None

        def clear_input_frame():
            nonlocal input_frame
            if input_frame:
                input_frame.destroy()
                input_frame = None

        def search_student():
            nonlocal found_student, input_frame
            query = search_var.get().strip().lower()
            if not query:
                result_var.set("Please enter a student ID or name")
                clear_input_frame()
                return

            found_student = None
            for s in self.students:
                if query == str(s.code).lower() or query in s.name.lower():
                    found_student = s
                    break

            if found_student:
                result_var.set(f"Found: {found_student.name} (ID: {found_student.code})\n"
                             f"Current: CW1={found_student.cw1}, CW2={found_student.cw2}, "
                             f"CW3={found_student.cw3}, Exam={found_student.exam}")
                show_update_options()
            else:
                result_var.set(f"No student found for: '{query}'")
                clear_input_frame()

        def show_update_options():
            nonlocal input_frame
            clear_input_frame()
            
            input_frame = Frame(update_window, bg=self.BG_MAIN)
            input_frame.pack(pady=10)

            Label(input_frame, text="Select field to update:", font=(self.base_font, 11, "bold"),
                  bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).grid(row=0, column=0, columnspan=2, pady=10)

            # field selection
            field_var = StringVar(value="name")
            
            fields = [
                ("Name", "name"),
                ("Coursework 1", "cw1"),
                ("Coursework 2", "cw2"), 
                ("Coursework 3", "cw3"),
                ("Exam Mark", "exam")
            ]
            
            for i, (text, value) in enumerate(fields):
                Radiobutton(input_frame, text=text, variable=field_var, value=value,
                           font=(self.base_font, 10), bg=self.BG_MAIN).grid(row=i+1, column=0, sticky='w', padx=20)

            # new value input
            Label(input_frame, text="New Value:", font=(self.base_font, 10),
                  bg=self.BG_MAIN, fg=self.TEXT_PRIMARY).grid(row=1, column=1, padx=5, pady=5)
            
            value_var = StringVar()
            value_entry = Entry(input_frame, textvariable=value_var, font=(self.base_font, 10))
            value_entry.grid(row=1, column=2, padx=5, pady=5)

            def update_field():
                if not found_student:
                    return

                field = field_var.get()
                new_value = value_var.get().strip()

                if not new_value:
                    messagebox.showerror("Error", "Please enter a new value!")
                    return

                try:
                    if field == "name":
                        found_student.name = new_value
                    else:
                        new_value_int = int(new_value)
                        if field in ["cw1", "cw2", "cw3"] and not (0 <= new_value_int <= 20):
                            messagebox.showerror("Error", "Coursework marks must be between 0-20!")
                            return
                        if field == "exam" and not (0 <= new_value_int <= 100):
                            messagebox.showerror("Error", "Exam mark must be between 0-100!")
                            return
                        
                        if field == "cw1":
                            found_student.cw1 = new_value_int
                        elif field == "cw2":
                            found_student.cw2 = new_value_int
                        elif field == "cw3":
                            found_student.cw3 = new_value_int
                        elif field == "exam":
                            found_student.exam = new_value_int

                    if self.save_data():
                        messagebox.showinfo("Success", f"Student {field} updated successfully!")
                        update_window.destroy()
                        self.students_page()

                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number for marks!")

            Button(input_frame, text="Update Field", 
                   font=(self.base_font, 10, "bold"),
                   bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="white",
                   command=update_field).grid(row=6, column=1, columnspan=2, pady=10)

        Button(search_frame, text="Search", 
               font=(self.base_font, 9, "bold"),
               bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="white",
               command=search_student).grid(row=0, column=2, padx=5, pady=5)

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
                relief=RAISED, bd=1, width=450, height=190)
            detailed_card.place(relx=0.5, rely=0.5, anchor="center")
            
            # student name and ID
            name_label = Label(detailed_card, text=found.name,
                font=(self.base_font, 14, "bold"),
                bg=self.ACCENT_GREEN_DARK, fg='#ffffff')
            name_label.place(x=30, y=25)
            
            id_label = Label(detailed_card, text=f"ID: {found.code}",
                font=(self.base_font, 10),
                bg="#ffffff", fg=self.TEXT_MUTED)
            id_label.place(x=30, y=55)
            
            # individual marks
            marks_label = Label(detailed_card, text=f"Coursework Marks: {found.cw1}, {found.cw2}, {found.cw3}",
                font=(self.base_font, 10),
                bg="#ffffff", fg=self.TEXT_PRIMARY)
            marks_label.place(x=30, y=90)
            
            cw_total_label = Label(detailed_card, text=f"Coursework Total: {found.coursework_total}/60",
                font=(self.base_font, 10),
                bg="#ffffff", fg=self.TEXT_PRIMARY)
            cw_total_label.place(x=30, y=115)
            
            exam_label = Label(detailed_card, text=f"Exam Mark: {found.exam}/100",
                font=(self.base_font, 10),
                bg="#ffffff", fg=self.TEXT_PRIMARY)
            exam_label.place(x=30, y=140)
            
            # overall performance
            total_label = Label(detailed_card, text=f"Overall Total: {found.overall_total}/160",
                font=(self.base_font, 10, "bold"),
                bg="#ffffff", fg=self.TEXT_PRIMARY)
            total_label.place(x=250, y=90)
            
            percent_label = Label(detailed_card, text=f"Percentage: {found.percentage:.1f}%",
                font=(self.base_font, 10, "bold"),
                bg="#ffffff", fg=self.TEXT_PRIMARY)
            percent_label.place(x=250, y=115)
            
            # grade with color
            grade_color = {
                "A": "green", "B": "blue", "C": "#fce80a", 
                "D": "orange", "F": "red"
            }
            grade_label = Label(detailed_card, text=f"Grade: {found.grade}",
                font=(self.base_font, 14, "bold"),
                bg=grade_color[found.grade], fg="white", width=10)
            grade_label.place(x=250, y=140)

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
        buttons = [self.students_btn, self.individual_btn, self.highest_btn, self.lowest_btn,
                  self.sort_btn, self.add_btn, self.delete_btn, self.update_btn]
        for btn in buttons:
            btn.configure(bg=self.BG_SIDEBAR_BTN_INACTIVE, fg="#d1d5db")
        
        if which == "students":
            self.students_btn.configure(bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="#ecfdf5")
        elif which == "individual":
            self.individual_btn.configure(bg=self.BG_SIDEBAR_BTN_ACTIVE, fg="#ecfdf5")

# root
if __name__ == "__main__":
    root = Tk()
    app = StudentManagerApp(root)
    root.mainloop()