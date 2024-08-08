from objects.student import Student
from reportlab.pdfgen import canvas


def generate_pdf(tutor: str, level: str, topics: list[str], student: Student):
    c = canvas.Canvas("hello.pdf")

    c.drawString(100, 300, f"Tutor: {tutor}")
    c.drawString(100, 250, f"Level: {level}")
    c.drawString(100, 200, f"Student: {student.name}")
    c.drawString(100, 150, f"Topics: {', '.join(topics)}")
    c.drawString(100, 100, f"Average: {student.averages}")
    c.drawString(100, 50, f"Total: {student.get_data().feedback}")

    c.showPage()
    c.save()
    pass
