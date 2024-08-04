import pandas as pd
from tabulate import tabulate
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import sys


def chunk_list(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def get_student_data(csv_file, student_name: str) -> list:
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

        print("Row as a list:", grouped_list)
        print("Comments:", comments)
        # Append column titles
        grouped_list.insert(
            0, ['Week', 'Understanding', 'Procedures', 'Problem Solving', 'Homework'])
        return grouped_list


def init_program():
    print("Welcome to the Student Database!")
    student_name = input("Enter the student's name: ").lower()
    year = input("Enter the students year (e.g. 9): ")
    period = input("Enter the period (YYTT e.g. 24t3): ").lower()
    data = get_student_data(period + 'y' + year + ".csv", student_name)

    # data = [
    #     ['Week', 'Understanding', 'Procedures', 'Problem Solving', 'Homework'],
    #     ['Week 1', None, None, None],
    #     ['Week 2', 'B', 'A', 'B', 'B'],
    #     ['Week 3', None, None, None],
    #     [None, None, None, None],
    #     [None, None, None, None],
    #     [None, None, None, None],
    #     [None, None, None, None],
    #     [None, None, None, None],
    #     [None, None, None, None],
    #     [None, None, None, None]
    # ]
    generate_pdf('test.pdf', data)


def generate_pdf(file_name, data):
    pdf = SimpleDocTemplate(file_name, pagesize=letter, rightMargin=inch,
                            leftMargin=inch, topMargin=inch, bottomMargin=inch)

    # Adjust column widths
    column_widths = [1.2 * inch] * len(data[0])

    # Create a Table with adjusted column widths
    table = Table(data, colWidths=column_widths)

    # Define table styles
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ])

    # Apply styles to the Table
    table.setStyle(style)

    # Build the PDF
    pdf.build([table])


if __name__ == '__main__':
    init_program()
