import sys
import pandas as pd
from objects.year import Year


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
            print(f"Found class in row {i}.")
            total_classes += 1

    # Break the CSV file into classes
    print(f"Found {total_classes} classes.")
    print('\n')

    for i, row in df.iterrows():
        if row.iloc[1] == 'Topic':

            # Tutor is found to the left of the first student.

            tutor = ''
            students = []
            topics = []
            level = ''

            # Find the students in the class
            # If student is NaN or not two words, skip
            j = i + 1
            while j < len(df) and df.iloc[j, 1] != 'Topic':
                student = df.iloc[j, 1]
                if pd.isna(student) or len(student.split()) != 2:
                    j += 1
                    continue

                if tutor == '':
                    tutor = df.iloc[j, 0]

                print(f"Found student {student}.")
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
                f"Class {tutor} created with {len(students)} students and {len(topics)} topics.")
            i = j
            print('\n')

    print(
        f"Found {total_classes} classes.")

    return year
