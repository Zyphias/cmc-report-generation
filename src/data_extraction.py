import sys
import pandas as pd
from objects.student import Student
from objects.student_data import StudentData
from objects.year import Year


def parse_student_data(data: str) -> StudentData:
    """Parse the data from a student row in the CSV file and return a StudentData object."""
    feedback = []
    comments = []

    # Comments are every 5th element. Add to comments
    for i in range(4, len(data), 5):
        comments.append(data[i])

    # Remove comments from data, the rest is feedback
    data = [data[i] for i in range(len(data)) if i % 5 != 4]
    feedback = data

    return StudentData(feedback, comments)


def csv_to_object(csv_file: str = './csv_store/24t3y9.csv') -> Year:
    """Read a CSV file and generate a new Year object associated with it."""

    # Open the CSV file
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        sys.exit(
            f"Error: File <{csv_file}> not found. Please ensure the file exists and try again.")

    # Initialise a new Year object
    year = csv_file[-5:-4]
    period = csv_file[-10:-6]
    year = Year(year, period)
    print(f"New Year object {year.get_year()} - {year.get_period()} created.")

    # Find the number of classes in the CSV file
    total_classes = 0
    for i, row in df.iterrows():
        if row.iloc[1] == 'Topic':
            total_classes += 1

    print(f"Found {total_classes} classes.")
    print()

    # Break the CSV file into classes
    for i, row in df.iterrows():
        if row.iloc[1] == 'Topic':
            tutor = ''
            students = []
            topics = []
            level = ''

            # Find the students in the class
            j = i + 1
            while j < len(df) and df.iloc[j, 1] != 'Topic':
                student = df.iloc[j, 1]
                # If student is NaN or not <first name> <last name>, skip
                if pd.isna(student) or len(student.split()) != 2:
                    j += 1
                    continue

                # Set tutor and level if not already set
                if tutor == '':
                    tutor = df.iloc[j, 0]
                    level = df.iloc[j+1, 0]

                # Create and append student to the list
                student_name = student.strip().lower()
                print(f"Found student {student_name}.")

                # Grab all data from that row
                student_data = df.iloc[j, 2:].to_list()
                student = Student(
                    student_name, parse_student_data(student_data))

                students.append(student)
                j += 1

            # Find the topics in the class
            while j < len(df) and df.iloc[j, 1] == 'Topic':
                topic = df.iloc[j, 0]
                topics.append(topic)
                j += 1

            # Create a new Class object and add it to the Year object
            year.add_class(tutor, students, topics, '')
            print(
                f"Class {tutor} created with {len(students)} students and {len(topics)} topics. Level: {level}.")
            i = j
            print('\n')

    print(
        f"Found {total_classes} classes.")

    return year
