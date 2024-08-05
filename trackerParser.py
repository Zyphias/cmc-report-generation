import pandas as pd
import sys
from generatePdf import generate_pdf


def chunk_list(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def get_student_data(csv_file='24t3y9.csv', student_name: str = 'jessica powell') -> list:
    # Read the CSV file into a DataFrame
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("Error: File not found. Please ensure provided information is correct!")
        exit()

    # Convert all student names to lowercase
    first_column_name = df.columns[1]
    df[first_column_name] = df[first_column_name].str.lower()

    # Filter the DataFrame to get the row where 'Name' matches the user input
    student_row = df[df['Week'] == student_name]

    # Print the resulting row(s)
    if student_row.empty:
        sys.exit(f"No student found with the name: {student_name}")
    else:
        row_list = student_row.iloc[0].tolist()
        del row_list[:2]

        # move every 5th value to a new list
        comments = [row_list[i] for i in range(4, len(row_list), 5)]
        row_list = [row_list[i]
                    for i in range(len(row_list)) if (i + 1) % 5 != 0]

        # Keep only first letter of each value, skip over nan
        row_list = [x[0] if isinstance(x, str) else None for x in row_list]

        grouped_list = chunk_list(row_list, 4)

        # add increase numbers to each chunk
        for i in range(len(grouped_list)):
            grouped_list[i].insert(0, i+1)

        print("Row as a list:", grouped_list)
        print("Comments:", comments)
        # Append column titles
        grouped_list.insert(
            0, ['Week', 'Understanding', 'Procedures', 'Problem Solving', 'Homework'])
        return grouped_list


def init_program():
    # print("Welcome to the Student Database!")
    # student_name = input("Enter the student's name: ").lower()
    # year = input("Enter the students year (e.g. 9): ")
    # period = input("Enter the period (YYTT e.g. 24t3): ").lower()
    # data = get_student_data(period + 'y' + year + ".csv", student_name)
    data = get_student_data()

    generate_pdf('test.pdf', data)


if __name__ == '__main__':
    init_program()
