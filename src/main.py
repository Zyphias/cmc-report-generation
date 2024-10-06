from data_extraction import csv_to_object
from get_email import get_contact_email
from objects.year import Year
from pdf_generation import generate_pdf
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def generate_year_reports(year: Year):
    period = year.get_period()

    if year.get_year() == '1' or year.get_year() == '2' or year.get_year() == '3':
        grade = f"Stage {year.get_year()}"
    else:
        grade = f"Y{year.get_year()}"

    for class_ in year.get_classes():
        tutor = class_.get_tutor()
        level = f"{grade} {class_.get_level()}"
        topics = class_.get_topics()
        for student in class_.get_students():
            generate_pdf(year.get_year(), tutor, level, topics,
                         student, period, student.get_days_away())
            print(
                f"Student: {student.get_name()}, Parent Email: {get_contact_email(student.get_name())}")


def generate_student_report(student_name, student_year, csv_files):
    csv_file = csv_files.get(student_year)
    if not csv_file:
        print(f"No CSV file found for year {student_year}.")
        return

    year = csv_to_object(csv_file)
    for class_ in year.get_classes():
        for student in class_.get_students():
            if student.get_name() == student_name:
                level = f"{year.get_year()} {class_.get_level()}"
                generate_pdf(year.get_year(), class_.get_tutor(), level, class_.get_topics(),
                             student, year.get_period(), student.get_days_away())
                return

    print(f"Student {student_name} not found in year {student_year}.")


def generate_single_year_report(student_year, csv_files):
    csv_file = csv_files.get(student_year)
    if not csv_file:
        print(f"No CSV file found for year {student_year}.")
        return

    year = csv_to_object(csv_file)
    generate_year_reports(year)


def main():
    csv_files = {
        '1': 'src/csv_store/24t3s1.csv',
        '2': 'src/csv_store/24t3s2.csv',
        '3': 'src/csv_store/24t3s3.csv',
        '7': 'src/csv_store/24t3y7.csv',
        '8': 'src/csv_store/24t3y8.csv',
        '9': 'src/csv_store/24t3y9.csv',
        '10': 'src/csv_store/24t3y10.csv',
        '11': 'src/csv_store/24t3y11.csv'
    }

    response = input(
        "Do you want to generate a single student report, a single year report, or all reports? (student/year/all): ").strip().lower()

    if response == 'student':
        student_name = input("Enter the student's name: ").strip()
        student_year = input(
            "Enter the student's year: 1/2/3/7/8/9/10/11 ").strip()
        generate_student_report(student_name, student_year, csv_files)

    elif response == 'year':
        student_year = input(
            "Enter the year you want to generate reports for: 1/2/3/7/8/9/10/11 ").strip()
        generate_single_year_report(student_year, csv_files)

    elif response == 'all':
        for csv_file in csv_files.values():
            year = csv_to_object(csv_file)
            generate_year_reports(year)


def send_email(receiver_email="steveyeung4@gmail.com", file_path="reports/24t3/Y9/kaylie_wong_24t3.pdf", student_name="Kaylie Wong"):
    # Email details
    sender_email = "steveyeung4@gmail.com"
    sender_password = "nxqg rklq eoho pmku"
    filename = file_path.split("/")[-1]

    # Create the email with 'mixed' subtype to allow attachments
    message = MIMEMultipart("mixed")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Term Report"

    # Add the body of the email
    body = f"Please find attached the term report for {student_name}."
    body_part = MIMEText(body, "plain")
    message.attach(body_part)

    # Attach the file
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={filename}",
    )

    message.attach(part)

    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

    print("Email sent successfully")
    exit()


if __name__ == '__main__':
    main()
    # send_email()
