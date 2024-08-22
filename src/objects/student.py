from .student_data import StudentData


class Student:
    """
    Contains a student's name and Student Data
    """

    def __init__(self, name: str, mark: str, data: StudentData):
        self.name = name
        self.data = data
        self.mark = mark
        self.days_away = data.get_days_away()
        self.averages = data.get_averages()

    def get_data(self) -> StudentData:
        return self.data

    def get_name(self) -> str:
        return self.name

    def get_mark(self) -> str:
        return self.mark

    def get_days_away(self) -> list[int]:
        return self.days_away

    def pretty_print(self):
        print(f"Name: {self.name}")
        print(f"Mark: {self.mark}")
        print(self.data.pretty_print())
