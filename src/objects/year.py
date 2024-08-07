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

    def add_class(self, tutor, students, topics):
        self.classes.append(Class(tutor, students, topics))

    def get_classes(self) -> list[Class]:
        return self.classes

    def get_year(self) -> str:
        return self.year

    def get_period(self) -> str:
        return self.period


"""
    Year (csv):
    - year: string
    - period: string
    - classes:
        - tutor: string
        - students: Students
        - topics: list of strings
"""
