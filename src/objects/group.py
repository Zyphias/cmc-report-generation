from .student import Student


class Class:
    """Object which holds all data for a given class, includes:
        - tutor: string
        - students: list of Students
        - topics: list of strings
    """

    def __init__(self, tutor: str, students: list[Student], topics: list[str], level: str):
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
