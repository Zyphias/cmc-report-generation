from PIL import Image
from objects.student import Student
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, white


LETTER_HEAD_PATH = 'src/images/LetterHead.png'
MAX_WIDTH = 408.072
TEXT_SIZE = 12
FONT = "Helvetica"
TITLE_FONT = "Helvetica-Bold"
TITLE_FONT_SIZE = 14


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
    # Measure the width of the text
    text_width = c.stringWidth(text, FONT, TEXT_SIZE)
    # Center text horizontally in the box
    text_x = x + (width - text_width) / 2
    # Center text vertically in the box (6 is half of font size for adjustment)
    text_y = y + height / 2 - 6
    c.drawString(text_x, text_y, text)


def draw_name_level(c, page_width, height, stu_name, stu_level, max_width=MAX_WIDTH):
    # Define the size of the text boxes
    box_height = 30
    box_margin = 10  # Margin around text inside the box

    # Define the text for the boxes
    name_text = "Name"
    name_value = stu_name
    level_text = "Level"
    level_value = stu_level

    # Calculate the width of the text boxes based on the content
    name_width = c.stringWidth(name_text, FONT, TEXT_SIZE)
    name_value_width = c.stringWidth(name_value, FONT, TEXT_SIZE)
    level_width = c.stringWidth(level_text, FONT, TEXT_SIZE)
    level_value_width = c.stringWidth(level_value, FONT, TEXT_SIZE)

    # Find the maximum width of the text boxes to use consistent width
    max_name_width = max(name_width, level_width)
    max_level_width = max(name_value_width, level_value_width)

    # Define box widths with margin
    box_width_name = max_name_width + 2 * box_margin
    box_width_level = max_level_width + 2 * box_margin

    # Total width of one pair of boxes (name + value) plus (level + value)
    pair_width = box_width_name + box_width_level

    # Calculate total width needed for all boxes (no spacing between them)
    total_width = 2 * pair_width

    # Calculate scaling factor to fit the boxes within the max_width
    scaling_factor = max_width / total_width

    # Adjust box sizes based on scaling factor
    scaled_box_width_name = box_width_name * scaling_factor
    scaled_box_width_level = box_width_level * scaling_factor

    # Calculate the starting x position to center the group of boxes
    start_x = (page_width - max_width) / 2

    # Draw the text boxes and text, ensuring no gap between boxes
    draw_text_box(c, start_x, height,
                  scaled_box_width_name, box_height, name_text)
    draw_text_box(c, start_x + scaled_box_width_name,
                  height, scaled_box_width_level, box_height, name_value)

    draw_text_box(c, start_x + scaled_box_width_name + scaled_box_width_level,
                  height, scaled_box_width_name, box_height, level_text)
    draw_text_box(c, start_x + 2 * scaled_box_width_name + scaled_box_width_level,
                  height, scaled_box_width_level, box_height, level_value)

    # Return the height of the text boxes
    return height - box_height


def draw_summary_level(c, page_width, page_height, pairs, max_width=MAX_WIDTH):
    # Define the size of the text boxes
    box_height = 30
    box_margin = 10  # Margin around text inside the box

    # Define the text for the boxes
    c1 = pairs[0][0]
    v1 = pairs[0][1]
    c2 = pairs[1][0]
    v2 = pairs[1][1]
    c3 = pairs[2][0]
    v3 = pairs[2][1]

    # Calculate the width of the text boxes based on the content
    c1_width = c.stringWidth(c1, FONT, TEXT_SIZE)
    v1_width = c.stringWidth(v1, FONT, TEXT_SIZE)
    c2_width = c.stringWidth(c2, FONT, TEXT_SIZE)
    v2_width = c.stringWidth(v2, FONT, TEXT_SIZE)
    c3_width = c.stringWidth(c3, FONT, TEXT_SIZE)
    v3_width = c.stringWidth(v3, FONT, TEXT_SIZE)

    # Find the maximum width of the text boxes to use consistent width
    max_c_width = max(c1_width, c2_width, c3_width)
    max_v_width = max(v1_width, v2_width, v3_width)

    # Define box width with margin
    box_width_c = max_c_width + 2 * box_margin
    box_width_v = max_v_width + 2 * box_margin

    # Calculate total width needed for all boxes (no spacing between them)
    total_width = 3 * (box_width_c + box_width_v)

    # Calculate scaling factor to fit within max_width
    scaling_factor = max_width / total_width

    # Adjust box sizes based on scaling factor
    scaled_box_width_c = box_width_c * scaling_factor
    scaled_box_width_v = box_width_v * scaling_factor

    # Calculate the starting x position to center the group of boxes
    scaled_total_width = 3 * (scaled_box_width_c + scaled_box_width_v)
    start_x = (page_width - scaled_total_width) / 2

    # Draw the text boxes and text, ensuring no gap between boxes
    draw_text_box(c, start_x, page_height,
                  scaled_box_width_c, box_height, c1)
    draw_text_box(c, start_x + scaled_box_width_c,
                  page_height, scaled_box_width_v, box_height, v1)

    draw_text_box(c, start_x + scaled_box_width_c + scaled_box_width_v,
                  page_height, scaled_box_width_c, box_height, c2)
    draw_text_box(c, start_x + 2 * (scaled_box_width_c) + scaled_box_width_v,
                  page_height, scaled_box_width_v, box_height, v2)

    draw_text_box(c, start_x + 2 * (scaled_box_width_c + scaled_box_width_v),
                  page_height, scaled_box_width_c, box_height, c3)
    draw_text_box(c, start_x + 3 * (scaled_box_width_c) + 2 * scaled_box_width_v,
                  page_height, scaled_box_width_v, box_height, v3)

    # Print width of the boxes for debugging
    print(f"Scaled total width: {scaled_total_width}")

    # Return the height of the text boxes
    return page_height - box_height


def draw_summary(c: canvas.Canvas, page_width: float, page_height: float, stu_name: str, stu_avg: list[str], stu_level: str) -> float:
    c.setFont(TITLE_FONT, TITLE_FONT_SIZE)
    c.drawString(100, page_height, "Summary of Results")
    c.setFont(FONT, TEXT_SIZE)

    summary = [['Understanding', stu_avg[0]], ['Fluency',
               stu_avg[1]], ['Problem Solving', stu_avg[2]]]
    page_height = draw_name_level(
        c, page_width, page_height - 50, stu_name, stu_level)
    page_height = draw_summary_level(c, page_width, page_height, summary)
    return page_height


def generate_pdf(tutor: str, level: str, topics: list[str], student: Student):
    c = canvas.Canvas("hello.pdf")

    # Acquire dimensions of the page
    width, height = A4

    # set font size
    c.setFont(FONT, TEXT_SIZE)

    # Insert letterhead, keep aspect ratio
    height = draw_letterhead(c, width, height)
    draw_summary(c, width, height, student.name,
                 student.averages, level)

    c.drawString(100, 300, f"Tutor: {tutor}")
    c.drawString(100, 250, f"Level: {level}")
    c.drawString(100, 200, f"Student: {student.name}")
    c.drawString(100, 150, f"Topics: {', '.join(topics)}")
    c.drawString(100, 100, f"Average: {student.averages}")
    c.drawString(100, 50, f"Total: {student.get_data().feedback}")

    c.showPage()
    c.save()
    pass
