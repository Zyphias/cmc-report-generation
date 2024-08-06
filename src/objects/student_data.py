class StudentData:
    """Holds all data for a student, including:
        - Weekly Feedback: list of ??
        - Comments: list of string
    """

    def __init__(self, feedback: list[str], comments: list[str]):
        self.feedback = feedback
        self.comments = comments

    def get_feedback(self) -> list[str]:
        return self.feedback

    def get_comments(self) -> list[str]:
        return self.comments
