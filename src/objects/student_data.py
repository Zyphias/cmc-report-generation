class StudentData:
    """Holds all data for a student, including:
        - Weekly Feedback: list of strings
        - Comments: list of string
    """

    def __init__(self, feedback: list[str], comments: list[str]):
        self.feedback = feedback
        self.comments = comments

    def get_feedback(self) -> list[str]:
        return self.feedback

    def get_comments(self) -> list[str]:
        return self.comments

    def pretty_print(self):
        # Print four feedbacks per line
        for i in range(0, len(self.feedback), 4):
            print(self.feedback[i:i + 4])

        # print one comment per line
        print()
        print("Weekly Comments:")
        week = 0
        for comment in self.comments:
            week += 1
            print(f"{week}: {comment}")
        print()
