import random
import string
from turtle import color
from PIL import Image
from comments_generator import generate_comment
from objects.student import Student
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph


LETTER_HEAD_PATH = 'src/images/LetterHead.png'
MAX_WIDTH = 450
TEXT_SIZE = 11
FONT = "Helvetica"
TITLE_FONT = "Helvetica-Bold"
TITLE_FONT_SIZE = 13


def generate_random_words(num_words: int) -> str:
    words = []
    for _ in range(num_words):
        # Random word length between 3 and 10
        word_length = random.randint(3, 10)
        word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
        words.append(word)
    return ' '.join(words)


def draw_letterhead(c: canvas.Canvas, page_width: float, page_height: float):
    # Draw the logo at the top left corner
    with Image.open(LETTER_HEAD_PATH) as img:
        original_width, original_height = img.size

    # Desired width for the logo
    desired_width = 8 * inch
    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Calculate the height to maintain the aspect ratio
    desired_height = desired_width / aspect_ratio

    x = (page_width - desired_width) / 2
    y = (page_height - desired_height) / 2

    # Draw the logo at the top left corner
    c.drawImage(LETTER_HEAD_PATH, x=x, y=y, width=desired_width,
                height=desired_height, mask='auto')

    # Return the new 'page height' after the logo has been drawn
    return desired_height - 160


def draw_text_box(c, x, y, width, height, text):
    # Draw the box
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.rect(x, y, width, height, stroke=1, fill=1)

    # Draw the text inside the box
    c.setFillColor(black)
    c.setFont(FONT, TEXT_SIZE)

    # Measure the width and height of the text
    text_width = c.stringWidth(text, FONT, TEXT_SIZE)
    text_height = TEXT_SIZE  # Approximate text height

    # Center text horizontally and vertically in the box
    text_x = x + (width - text_width) / 2
    text_y = y + TEXT_SIZE

    c.drawString(text_x, text_y, text)


def draw_summary_line(c, page_width, page_height, pairs, max_width=MAX_WIDTH):
    # Define the size of the text boxes
    box_height = 30
    box_margin = 10  # Margin around text inside the box

    # Calculate the width of the text boxes based on the content
    c_widths = [c.stringWidth(pair[0], FONT, TEXT_SIZE) for pair in pairs]
    v_widths = [c.stringWidth(pair[1], FONT, TEXT_SIZE) for pair in pairs]

    # Find the maximum width of the text boxes to use consistent width
    max_c_width = max(c_widths)
    max_v_width = max(v_widths)

    # Define box width with margin
    box_width_c = max_c_width + 2 * box_margin
    box_width_v = max_v_width + 2 * box_margin

    # Calculate total width needed for all boxes (no spacing between them)
    total_width = len(pairs) * (box_width_c + box_width_v)

    # Calculate scaling factor to fit exactly within max_width
    scaling_factor = max_width / total_width

    # Adjust box sizes based on scaling factor
    scaled_box_width_c = box_width_c * scaling_factor
    scaled_box_width_v = box_width_v * scaling_factor

    # Calculate the starting x position to center the group of boxes
    start_x = (page_width - max_width) / 2

    # Draw the text boxes and text, ensuring no gap between boxes
    current_x = start_x
    for c_text, v_text in pairs:
        draw_text_box(c, current_x, page_height,
                      scaled_box_width_c, box_height, c_text)
        current_x += scaled_box_width_c
        draw_text_box(c, current_x, page_height,
                      scaled_box_width_v, box_height, v_text)
        current_x += scaled_box_width_v

    # Return the height of the text boxes
    return page_height - box_height


def draw_summary(c: canvas.Canvas, page_width: float, page_height: float, stu_name: str, stu_avg: list[str], stu_level: str) -> float:
    c.setFont(TITLE_FONT, TITLE_FONT_SIZE)
    c.drawString(100, page_height, "Summary of Results")
    c.setFont(FONT, TEXT_SIZE)

    # Define the information to display
    name_info = [['Name', stu_name], ['Level', stu_level], ['Mark', '86']]
    summary = [['Understanding', stu_avg[0]], ['Fluency',
               stu_avg[1]], ['Problem Solving', stu_avg[2]]]

    # Draw the text boxes for the information
    page_height = draw_summary_line(
        c, page_width, page_height - 50, name_info)
    page_height = draw_summary_line(c, page_width, page_height, summary)
    return page_height


def draw_comments(c, page_width, y, text, font_size=12, padding=10, width=MAX_WIDTH):
    # Set up the style for the paragraph
    text_style = ParagraphStyle(
        'Normal',
        fontName=FONT,
        fontSize=TEXT_SIZE,
        leading=TITLE_FONT_SIZE,
        spaceBefore=padding,
        spaceAfter=padding
    )

    # Create a Paragraph object for the text
    paragraph = Paragraph(text, text_style)

    # Calculate the height needed for the paragraph
    _, text_height = paragraph.wrap(width - 2 * padding, 0)

    # Set up the style for the title
    title_style = ParagraphStyle(
        'Title',
        fontName=TITLE_FONT,
        fontSize=TITLE_FONT_SIZE,
        leading=font_size + 4,
        spaceAfter=padding
    )
    title = Paragraph("Tutor Comments", title_style)
    _, title_height = title.wrap(width - 2 * padding, 0)

    # Calculate the total height including padding and title
    total_height = text_height + title_height + 3 * padding

    # Calculate the x-coordinate to center the box
    x = (page_width - width) / 2

    # Draw the box
    c.rect(x, y - total_height, width, total_height)

    # Draw the title inside the box
    title.drawOn(c, x + padding, y - padding - title_height)

    # Draw the text inside the box
    paragraph.drawOn(c, x + padding, y - 2 * padding -
                     title_height - text_height)


def generate_pdf(tutor: str, level: str, topics: list[str], student: Student):
    c = canvas.Canvas("test.pdf")

    # Acquire dimensions of the page
    width, height = A4

    # set font size
    c.setFont(FONT, TEXT_SIZE)

    # Insert letterhead, keep aspect ratio
    height = draw_letterhead(c, width, height)
    height = draw_summary(c, width, height, student.name,
                          student.averages, level)
    draw_comments(c, width, height,
                  generate_comment(student.name, student.averages, student.get_data().feedback))

    c.showPage()
    c.save()
    pass
