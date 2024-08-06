class Year:
    """Object which holds all data for a given year and period, includes:
        - year: string
        - period: string
        - students: Students
    """

    def __init__(self, year, period):
        self.year = year
        self.period = period

    def is_leap(self):
        return self.year % 4 == 0 and (self.year % 100 != 0 or self.year % 400 == 0)
