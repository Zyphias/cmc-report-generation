from src.data_extraction import csv_to_object
from legacy_code.generatePdf import generate_pdf
from legacy_code.trackerParser import get_student_data


def init_program():
    # print("Welcome to the Student Database!")
    # student_name = input("Enter the student's name: ").lower()
    # year = input("Enter the students year (e.g. 9): ")
    # period = input("Enter the period (YYTT e.g. 24t3): ").lower()
    # data = get_student_data(period + 'y' + year + ".csv", student_name)
    data = get_student_data()

    generate_pdf('test.pdf', data)


def main():
    csv_file = './csv_store/24t3y9.csv'

    # Read a CSV file and generate a new Year object
    year = csv_to_object(csv_file)
    print("Program finished. Success!")
    pass


if __name__ == '__main__':
    main()
