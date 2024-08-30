from data_extraction import csv_to_object
from objects.year import Year
from pdf_generation import generate_pdf


def generate_year_reports(year: Year):
    period = year.get_period()
    grade = f"Y{year.get_year()}"
    for class_ in year.get_classes():
        tutor = class_.get_tutor()
        level = f"{grade} {class_.get_level()}"
        for student in class_.get_students():
            generate_pdf(year.get_year(), tutor, level,
                         class_.get_topics(), student, period, student.get_days_away())


def main():
    y10_csv_file = 'src/csv_store/24t3y10.csv'
    y9_csv_file = 'src/csv_store/24t3y9.csv'
    y8_csv_file = 'src/csv_store/24t3y8.csv'
    y7_csv_file = 'src/csv_store/24t3y7.csv'

    response = input("Do you want a single student report? y/n: ")
    if response == 'y':
        stu_name = input("Enter the student's name: ")
        stu_year = input("Enter the student's year: 7/8/9/10 ")
        if stu_year == '7':
            csv_file = y7_csv_file
        elif stu_year == '8':
            csv_file = y8_csv_file
        elif stu_year == '9':
            csv_file = y9_csv_file
        elif stu_year == '10':
            csv_file = y10_csv_file

        year = csv_to_object(csv_file)
        for class_ in year.get_classes():
            for s in class_.get_students():
                if s.get_name() == stu_name:
                    generate_pdf(year.get_year(), class_.get_tutor(), f"Y{year.get_year()} {class_.get_level()}",
                                 class_.get_topics(), s, year.get_period(), s.get_days_away())
                    return

    # Read a CSV file and generate a new Year object
    year = csv_to_object(csv_file)

    # Generate PDFs for each student in the year
    generate_year_reports(year)


if __name__ == '__main__':
    main()
