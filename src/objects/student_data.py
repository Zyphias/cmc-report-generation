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

    def get_no_hw_feedback(self) -> list[str]:
        # Remove every 4th element
        return [self.feedback[i] for i in range(len(self.feedback)) if i % 4 != 3]

    def get_comments(self) -> list[str]:
        return self.comments

    def get_days_away(self) -> list[int]:
        # Return the index of the weeks where comments say 'away'. Integers
        return [i + 1 for i, comment in enumerate(self.comments) if isinstance(comment, str) and "away" in comment.lower()]

    def get_averages(self) -> list[str]:
        def extract_and_convert(feedback, start, step):
            # Extract elements and convert to numerical values
            return [5 - ord(feedback[i]) + ord('A') for i in range(start, len(feedback), step) if isinstance(feedback[i], str)]

        def average_to_grade(scores):
            # If no scores, return 'N/A'
            if not scores:
                return 'N/A'

            # Calculate average and convert back to letter grade
            return chr(5 - round(sum(scores) / len(scores)) + ord('A'))

        # Extract and convert feedback
        understanding = extract_and_convert(self.feedback, 0, 4)
        fluency = extract_and_convert(self.feedback, 1, 4)
        problem_solving = extract_and_convert(self.feedback, 2, 4)
        homework = extract_and_convert(self.feedback, 3, 4)

        # Calculate averages and convert to letter grades
        return [
            average_to_grade(understanding),
            average_to_grade(fluency),
            average_to_grade(problem_solving),
            average_to_grade(homework)
        ]

    def pretty_print(self):
        print("Averages: \n <U, F, PS, HW>")
        print(self.get_averages())
        print()

        # Print weekly feedback
        print("Weekly Feedback:")
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
