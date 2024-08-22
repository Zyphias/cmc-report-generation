from data_extraction import csv_to_object
from pdf_generation import generate_pdf


def generate_year_reports(year):
    period = year.get_period()
    grade = f"Y{year.get_year()}"
    for class_ in year.get_classes():
        level = f"{grade} {class_.get_level()}"
        for student in class_.get_students():
            generate_pdf("Steve", level,
                         class_.get_topics(), student, period)


def main():
    csv_file = 'src/csv_store/24t3y9.csv'

    # Read a CSV file and generate a new Year object
    year = csv_to_object(csv_file)

    # Generate PDFs for each student in the year
    generate_year_reports(year)


if __name__ == '__main__':
    main()
