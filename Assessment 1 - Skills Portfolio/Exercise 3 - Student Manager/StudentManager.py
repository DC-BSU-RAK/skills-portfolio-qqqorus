import os
from tkinter import *
from tkinter import ttk, messagebox
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




# execution in main page
if __name__ == "__main__":
    app = StudentManager()
    app.run()