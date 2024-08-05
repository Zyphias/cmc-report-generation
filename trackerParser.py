import random
import pandas as pd
from tabulate import tabulate
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from PIL import Image

from reportlab.lib import colors
import sys
from reportlab.pdfgen import canvas


def chunk_list(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def generate_random_words(word_list, num_words):
    return ' '.join(random.choices(word_list, k=num_words))


def create_text_box(c, x, y, width, initial_height, word_list, num_words=100, line_width=1):
    # Generate random words
    random_words = generate_random_words(word_list, num_words)

    # Set up styles
    styles = getSampleStyleSheet()

    # Title style - smaller font size
    title_style = ParagraphStyle(
        name='TitleStyle', fontName='Helvetica-Bold', fontSize=14, spaceAfter=5, alignment=0)  # Left align

    # Body text style
    body_style = ParagraphStyle(
        name='BodyStyle', fontName='Helvetica', fontSize=12, leading=12, alignment=0)  # Left align

    # Create title paragraph
    title_paragraph = Paragraph("Tutor Comments", title_style)

    # Create body paragraph
    body_paragraph = Paragraph(random_words, body_style)

    # Measure text sizes
    title_width, title_height = title_paragraph.wrap(
        width - 10, initial_height)
    body_width, body_height = body_paragraph.wrap(
        width - 10, initial_height - title_height - 15)

    # Adjust the height of the box if necessary
    adjusted_height = title_height + body_height + 30  # Adding some padding

    # Clear previous drawings if necessary (e.g., by drawing a white rectangle over the old box)
    c.setFillColor(colors.white)
    c.rect(x, y - initial_height, width, initial_height, fill=1, stroke=0)

    # Set line width
    c.setLineWidth(line_width)

    # Draw the updated box with the adjusted height
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    c.setFillColor(colors.white)
    c.rect(x, y - adjusted_height, width, adjusted_height, fill=1, stroke=1)

    # Reposition and draw the title - Aligned to the top-left corner
    title_x = x + 5  # Padding from the left
    title_y = y - 10  # Padding from the top
    title_paragraph.wrapOn(c, width - 10, adjusted_height)
    title_paragraph.drawOn(c, title_x, title_y - title_paragraph.height)

    # Reposition and draw the body text
    body_x = x + 5
    body_y = title_y - title_paragraph.height - 10  # Position below the title
    body_paragraph.wrapOn(c, width - 10, adjusted_height -
                          title_paragraph.height - 20)
    body_paragraph.drawOn(c, body_x, body_y - body_paragraph.height)


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


def generate_pdf(file_name, data):
    # Create a canvas object
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Draw the logo at the top left corner
    with Image.open('LetterHead.png') as img:
        original_width, original_height = img.size

    # Desired width for the logo
    desired_width = 8 * inch
    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Calculate the height to maintain the aspect ratio
    desired_height = desired_width / aspect_ratio

    x = (width - desired_width) / 2
    y = (height - desired_height) / 2

# Draw the logo at the top left corner
    c.drawImage('LetterHead.png', x=x, y=y, width=desired_width,
                height=desired_height, mask='auto')

    # Define margins
    left_margin = inch
    right_margin = inch
    top_margin = inch
    bottom_margin = inch

    # Adjust column widths
    column_widths = [1.2 * inch] * len(data[0])

    # Calculate table position
    table_width = sum(column_widths)
    table_height = len(data) * 0.5 * inch  # Estimate row height
    table_x = (width - table_width) / 2  # Center horizontally
    table_y = top_margin + table_height - 1.5 * inch  # Adjust for margin and space

    # Create a Table with adjusted column widths
    table = Table(data, colWidths=column_widths)

    # Define table styles
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d3f7c6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ])

    # Apply styles to the Table
    table.setStyle(style)

    # Build the table into the canvas
    table.wrapOn(c, width - left_margin - right_margin, table_height)
    table.drawOn(c, table_x, table_y)  # Position the table on the canvas

    # Define the position and size of the text box
    box_width = 400
    box_height = 200
    box_x = (width - box_width) / 2  # Center horizontally
    box_y = height - top_margin - box_height - \
        1.5 * inch - 1.5 * inch  # Adjust for margin and space

    # Generate a list of words (can be customized)
    word_list = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
                 "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo", "consequat", "duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate", "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur"]

    # Call the function to create the text box
    create_text_box(c, box_x, box_y, box_width, box_height, word_list)

    # Save the PDF
    c.save()


if __name__ == '__main__':
    init_program()
