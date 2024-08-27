import os
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
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfReader, PdfWriter


LETTER_HEAD_PATH = 'src/images/LetterHead.png'
MAX_WIDTH = 450
TEXT_SIZE = 11
FONT = "Helvetica"
TITLE_FONT = "Helvetica-Bold"
TITLE_FONT_SIZE = 13
UNDERSTANDING_COLOUR = '#69bf4b'
FLUENCY_COLOUR = '#003965'
PS_COLOUR = '#01665e'


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


def draw_summary(c: canvas.Canvas, page_width: float, page_height: float, stu_name: str, stu_avg: list[str], stu_mark: str, stu_level: str) -> float:
    c.setFont(TITLE_FONT, TITLE_FONT_SIZE)
    c.drawString(100, page_height, "Summary of Results")
    c.setFont(FONT, TEXT_SIZE)

    # Define the information to display
    name_info = [['Name', stu_name], ['Class', stu_level]]
    summary = [['Understanding', stu_avg[0]], ['Fluency',
               stu_avg[1]], ['Problem Solving', stu_avg[2]]]

    # Draw the text boxes for the information
    page_height = draw_summary_line(
        c, page_width, page_height - 50, name_info)
    page_height = draw_summary_line(c, page_width, page_height, summary)
    return page_height


def draw_comments(c, page_width, y, text, font_size=12, padding=10, width=MAX_WIDTH) -> float:
    text = text.replace("\n", "<br/>")

    # Set up the style for the paragraph
    text_style = ParagraphStyle(
        'Normal',
        fontName=FONT,
        fontSize=TEXT_SIZE - 2,
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
        fontSize=TITLE_FONT_SIZE - 2,
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

    return y - total_height - 20


def draw_key(c: canvas.Canvas, page_width, page_height, colors, width=MAX_WIDTH):
    # Define the key dimensions and spacing
    key_radius = 6  # Radius of the circle
    key_spacing = 50  # Space between keys, adjusted for text length

    # Strings corresponding to each key
    labels = ['Understanding', 'Fluency', 'Problem Solving']

    # Set font size to 10pt
    font_size = 10
    c.setFont("Helvetica", font_size)

    # Calculate the total width needed for keys and labels
    total_keys_width = 0
    key_label_pairs = []
    for i, label in enumerate(labels):
        # Calculate the width of the label at 10pt font size
        label_width = c.stringWidth(label, "Helvetica", font_size)
        # Calculate the total width of the key and label pair
        # 5 units of padding between key and label
        pair_width = 2 * key_radius + label_width + 5
        key_label_pairs.append(pair_width)
        total_keys_width += pair_width

    # Add the spacing between keys
    total_keys_width += (len(colors) - 1) * key_spacing

    # Calculate the starting x position to center the keys and labels
    key_x = (page_width - total_keys_width) / 2
    key_y = page_height

    # Draw the keys (as circles) and their labels
    for i, color in enumerate(colors):
        c.setFillColor(color)
        # Draw a circle with center at (key_x + key_radius, key_y)
        c.circle(key_x + key_radius, key_y, key_radius, fill=1)

        c.setFillColor(black)
        # Vertically center the text with the circle
        text_y = key_y - (font_size / 2)
        c.drawString(key_x + 2 * key_radius + 5, text_y, labels[i])

        # Move the x position to the next key position
        key_x += key_label_pairs[i] + key_spacing

    # Return the new y position after drawing the keys
    return key_y - 20  # Adjust to give space for the next element below


def draw_graph(c: canvas.Canvas, page_width, page_height, data, topics, days_away: list[int], display_weeks, width=MAX_WIDTH-100):

    # Limit the data and topics to the first n weeks
    # Assuming each week has 3 data points (Understanding, Fluency, PS)
    data = data[:display_weeks * 3]
    topics = topics[:display_weeks]

    # Include colour keys
    c.setFillColor(black)
    c.setFont(TITLE_FONT, TITLE_FONT_SIZE)
    c.drawString(100, page_height - 10, "Weekly Feedback")
    c.setFont(FONT, TEXT_SIZE)
    page_height -= 28

    # Define colors for the bars
    colors = [
        HexColor(UNDERSTANDING_COLOUR),
        HexColor(FLUENCY_COLOUR),
        HexColor(PS_COLOUR)
    ]

    page_height = draw_key(c, page_width, page_height, colors)

    # Constants
    GRAPH_HEIGHT = 130
    BOTTOM_OF_GRAPH = page_height - GRAPH_HEIGHT
    EMPTY_POINT_HEIGHT = 1
    BARS_PER_GROUP = 3
    GAP_WIDTH = 5  # Gap width between groups of bars
    TOPIC_LABEL_OFFSET = 10  # Offset from the bottom of the bars to the topic label
    INITIAL_GAP_WIDTH = 5  # Define the initial gap before the first group of bars
    FONT_SIZE = 8  # Font size of the topic labels
    RIGHT_OFFSET = 3  # Adjust this value to move the topic text further to the right

    # Draw the axes
    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.line((page_width - width) / 2, page_height - GRAPH_HEIGHT,
           (page_width + width) / 2, page_height - GRAPH_HEIGHT)
    c.line((page_width - width) / 2, page_height,
           (page_width - width) / 2, page_height - GRAPH_HEIGHT)

    # Draw notches and labels on the y-axis
    letters = ['', 'E', 'D', 'C', 'B', 'A']
    num_letters = len(letters)

    for i, letter in enumerate(letters):
        y = BOTTOM_OF_GRAPH + (GRAPH_HEIGHT * i / (num_letters - 1))
        c.line((page_width - width) / 2, y, (page_width - width) / 2 - 5, y)
        c.drawString((page_width - width) / 2 - 20, y - 5, letter)

    # Prepare data
    num_data_points = len(data)
    data = [str(item) if isinstance(item, str) else '' for item in data]

    # Calculate bar dimensions
    bar_width = (width - (GAP_WIDTH * (num_data_points //
                                       BARS_PER_GROUP))) / num_data_points

    # Draw bars
    for i, letter in enumerate(data):
        # Calculate the x position for each bar
        group_index = i // BARS_PER_GROUP
        bar_index_in_group = i % BARS_PER_GROUP
        # Include the initial gap before the first group of bars
        x = (page_width - width) / 2 + INITIAL_GAP_WIDTH + \
            (i * bar_width) + (group_index * GAP_WIDTH)

        # Set the color for the current bar
        c.setFillColor(colors[bar_index_in_group])
        c.setLineWidth(0.5)

        # Handle empty strings
        if letter == '':
            y = BOTTOM_OF_GRAPH + EMPTY_POINT_HEIGHT
            bar_height = EMPTY_POINT_HEIGHT
        else:
            y = BOTTOM_OF_GRAPH + \
                (GRAPH_HEIGHT * letters.index(letter) / (num_letters - 1))
            bar_height = BOTTOM_OF_GRAPH - y

        # Draw the bar
        c.rect(x, y, bar_width, bar_height, fill=1)

        c.setFillColor(black)

    for i, topic in enumerate(topics):
        # Calculate the x position for each group of three bars
        group_start_index = i * BARS_PER_GROUP
        # Include the initial gap before the first group of bars
        group_x_start = (page_width - width) / 2 + INITIAL_GAP_WIDTH + \
            (group_start_index * bar_width) + (i * GAP_WIDTH)
        group_x_center = group_x_start + (BARS_PER_GROUP * bar_width) / 2

        # Adjust the topic_x to move the text to the right
        topic_x = group_x_center + RIGHT_OFFSET

        # Set the font and size for the topic labels
        c.setFont(FONT, FONT_SIZE)
        topic_width = c.stringWidth(topic, FONT, FONT_SIZE)
        topic_height = FONT_SIZE  # Assuming height is approximately equal to font size

        # Calculate the position for the vertical text
        topic_y = BOTTOM_OF_GRAPH - TOPIC_LABEL_OFFSET - \
            topic_width  # Adjusted y position

        # Save the state of the canvas
        c.saveState()

        # Translate the canvas to the center of where the text will be drawn
        c.translate(topic_x, topic_y)

        # Rotate the canvas 90 degrees around the new origin
        c.rotate(90)

        # if i is in days_away, change the color of the text
        if i + 1 in days_away:
            c.setFillColor(HexColor('#ff0000'))
            # Draw the text
            c.drawString(0, 0, topic)
            c.setFillColor(black)
        else:
            # Draw the text
            c.drawString(0, 0, topic)

        # Restore the canvas state
        c.restoreState()
    return page_height - 200


def generate_pdf(year: str, tutor: str, level: str, topics: list[str], student: Student, period: str, days_away: list[int] = None):
    # Define the folder where you want to save the PDFs
    folder_path = f"reports/{period}/{year}"

    # Ensure the reports directory exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create the file name with the path
    print_name = student.name.lower().replace(" ", "_")
    file_name = f"{print_name}_{period}.pdf"
    file_path = os.path.join(folder_path, file_name)

    # Create the canvas with the specified path
    c = canvas.Canvas(file_path)

    # Acquire dimensions of the page
    width, height = A4

    # Set font size
    c.setFont(FONT, TEXT_SIZE)

    # Insert letterhead, keep aspect ratio
    height = draw_letterhead(c, width, height)
    height = draw_summary(c, width, height, student.name,
                          student.averages, student.mark, level)
    height = draw_comments(c, width, height,
                           generate_comment(student.name, student.averages, student.get_data().comments))
    height = draw_graph(
        c, width, height, student.get_data().get_no_hw_feedback(), topics, days_away, 6)

    # Draw centered footer
    c.setFont(FONT, 8)
    c.drawCentredString(
        width / 2, 20, f"© Cherrybrook Maths Coaching 2024")

    # Finalize the PDF
    c.showPage()
    c.save()

    with open(f"{file_path}", "rb") as existing_pdf:
        reader = PdfReader(existing_pdf)

        # Create a writer object for the final output PDF
        writer = PdfWriter()

        # Add all pages from the original PDF
        for page in reader.pages:
            writer.add_page(page)

        # Read the additional PDF
        with open("src/metric.pdf", "rb") as additional_pdf:
            additional_reader = PdfReader(additional_pdf)

            # Add all pages from the additional PDF
            for page in additional_reader.pages:
                writer.add_page(page)

        # Save the final PDF
        with open(f"{file_path}", "wb") as final_pdf:
            writer.write(final_pdf)

    print(f"PDF saved at: {file_path}")
