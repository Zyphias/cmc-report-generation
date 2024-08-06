from src.objects.student_data import StudentData


class Student:
    """
    Contains a student's name and Student Data
    """

    def __init__(self, name: str, data: StudentData):
        self.name = name
        self.data = data

    def get_student_data(self) -> StudentData:
        return self.data

    def get_student_name(self) -> str:
        return self.name
