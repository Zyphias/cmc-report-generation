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
    csv_file = 'src/csv_store/24t3y8.csv'

    # Read a CSV file and generate a new Year object
    year = csv_to_object(csv_file)

    # Generate PDFs for each student in the year
    generate_year_reports(year)


if __name__ == '__main__':
    main()
