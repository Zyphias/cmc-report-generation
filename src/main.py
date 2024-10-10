import os
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

    if year.get_year() == 'S1' or year.get_year() == 'S2' or year.get_year() == 'S3':
        grade = f"Stage {year.get_year().strip('S')}"
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


def generate_student_report(student_name: str, student_year: str, csv_files: dict):
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


def generate_single_year_report(student_year: str, csv_files: dict):
    csv_file = csv_files.get(student_year)
    if not csv_file:
        print(f"No CSV file found for year {student_year}.")
        return

    year = csv_to_object(csv_file)
    generate_year_reports(year)


def generate_reports():
    period = input(
        "What period would you like to generate reports for? (24t3/24t4): ").strip().lower()

    # Check if the period is valid, by checking folder path
    if not os.path.isdir(f'src/csv_store/{period}'):
        print(f"{period} is not in the system.")
        return

    csv_files = {
        f"{year}": f"src/csv_store/{period}/24t3Y{year}.csv" if year > 3 else f"src/csv_store/{period}/24t3S{year}.csv" for year in range(1, 11)}

    type = input(
        "Do you want to generate a single student report, a single year report, or all reports? (student/year/all): ").strip().lower()

    res = input(
        f"Are you sure you want to generate {type} report(s) for {period}? (y/n): ").strip().lower()

    # If the user does not confirm the action, return
    if res != 'y':
        return

    if type == 'student':
        student_name = input("Enter the student's name: ").strip()
        student_year = input(
            "Enter the student's year: 1/2/3/7/8/9/10/11 ").strip()
        generate_student_report(student_name, student_year, csv_files)

    elif type == 'year':
        student_year = input(
            "Enter the year you want to generate reports for: 1/2/3/7/8/9/10/11 ").strip()
        generate_single_year_report(student_year, csv_files)

    elif type == 'all':
        for csv_file in csv_files.values():
            year = csv_to_object(csv_file)
            generate_year_reports(year)


def send_email(receiver_email: str = "steveyeung4@gmail.com", file_path: str = "reports/24t3/Y9/kaylie_wong_24t3.pdf", student_name: str = "Kaylie Wong"):
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


def main():
    while True:
        res = input(
            "Would you like to generate reports or send emails? (r/e): ").strip().lower()

        if res == 'r':
            generate_reports()
        elif res == 'e':
            print(NotImplementedError("Email functionality not implemented."))
            # send_email()
        else:
            print("Invalid response.")


if __name__ == '__main__':
    main()
