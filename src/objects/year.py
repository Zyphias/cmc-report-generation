from objects.student import Student
from .group import Class


class Year:
    """Object which holds all data for a given year and period, includes:
        - year: string
        - period: string
        - classes: list of Class
            - tutor: string
            - students: list of Students
            - topics: list of strings
    """

    def __init__(self, year: str, period: str):
        self.year = year
        self.period = period
        self.classes = []

    def add_class(self, tutor, students, topics, level):
        self.classes.append(Class(tutor, students, topics, level))

    def get_classes(self) -> list[Class]:
        return self.classes

    def get_year(self) -> str:
        return self.year

    def get_period(self) -> str:
        return self.period

    def get_student(self, student_name: str) -> Student | None:
        for class_ in self.classes:
            student = class_.get_student(student_name)
            if student is not None:
                return student
        return None

    def get_students(self) -> list[Student]:
        students = []
        for class_ in self.classes:
            students.extend(class_.get_students())
        return students


"""
    Year (csv):
    - year: string
    - period: string
    - classes:
        - tutor: string
        - students: Students
        - topics: list of strings
"""
