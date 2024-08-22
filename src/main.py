from data_extraction import csv_to_object
from pdf_generation import generate_pdf


def main():
    csv_file = 'src/csv_store/24t3y9.csv'

    # Read a CSV file and generate a new Year object
    year = csv_to_object(csv_file)

    period = year.get_period()
    grade = f"Y{year.get_year()}"
    for class_ in year.get_classes():
        level = f"{grade} {class_.get_level()}"
        for student in class_.get_students():
            generate_pdf("Steve", level,
                         class_.get_topics(), student, period)

    # # Main loop - get student info
    # try:
    #     while True:
    #         student_name = input("Enter a student name: ").strip().title()
    #         if student_name == "":
    #             break
    #         student = year.get_student(student_name)
    #         if student is None:
    #             print("Student not found.")
    #         else:
    #             student.pretty_print()
    #             period = year.get_period()
    #             generate_pdf("Steve", "Y9 Advanced", [
    #                 "Midpoint, Gradient, Distance", "Pythagoras' Theorem", "Calculus", "Binomial Distribution",
    #                 "Yearly Study", "Midpoint, Gradient, Distance", "Pythagoras' Theorem", "Calculus",
    #                 "Binomial Distribution", "Yearly Study"], student, period)
    # except KeyboardInterrupt:
    #     print()
    #     print("Keyboard interrupt received, shutting down...")
    # finally:
    #     print("Goodbye!")


if __name__ == '__main__':
    main()
