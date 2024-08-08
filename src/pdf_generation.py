from PIL import Image
from objects.student import Student
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

LETTER_HEAD_PATH = 'src/images/LetterHead.png'


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


def generate_pdf(tutor: str, level: str, topics: list[str], student: Student):
    c = canvas.Canvas("hello.pdf")

    # Acquire dimensions of the page
    width, height = A4

    # Insert letterhead, keep aspect ratio
    draw_letterhead(c, width, height)

    c.drawString(100, 300, f"Tutor: {tutor}")
    c.drawString(100, 250, f"Level: {level}")
    c.drawString(100, 200, f"Student: {student.name}")
    c.drawString(100, 150, f"Topics: {', '.join(topics)}")
    c.drawString(100, 100, f"Average: {student.averages}")
    c.drawString(100, 50, f"Total: {student.get_data().feedback}")

    c.showPage()
    c.save()
    pass
