from .student_data import StudentData


class Student:
    """
    Contains a student's name and Student Data
    """

    def __init__(self, name: str, mark: str, data: StudentData):
        self.name = name
        self.data = data
        self.mark = mark
        self.averages = data.get_averages()

    def get_data(self) -> StudentData:
        return self.data

    def get_name(self) -> str:
        return self.name

    def pretty_print(self):
        print(f"Name: {self.name}")
        print(f"Mark: {self.mark}")
        print(self.data.pretty_print())
