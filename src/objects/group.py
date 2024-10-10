from pdf_generation import generate_pdf
from .student import Student


class Class:
    """Object which holds all data for a given class, includes:
        - tutor: string
        - students: list of Students
        - topics: list of strings
        - level: string
    """

    def __init__(self, tutor: str, students: list[Student], topics: list[str], level: str | None):
        self.tutor = tutor
        self.students = students
        self.topics = topics
        self.level = level

    def get_tutor(self) -> str:
        return self.tutor

    def get_students(self) -> list[Student]:
        return self.students

    def get_topics(self) -> list[str]:
        return self.topics

    def get_level(self) -> str:
        return self.level

    def get_student(self, student_name: str) -> Student:
        for student in self.students:
            if student.get_name() == student_name:
                return student
        return None

    def generate_pdfs(self):
        for student in self.students:
            generate_pdf(self.tutor, self.level, self.topics, student)

    def pretty_print(self):
        print(f"Tutor: {self.tutor}")
        print(f"Level: {self.level}")
        print("Students: ")
        for student in self.students:
            print(f"- {student.get_name()}")
