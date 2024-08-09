from data_extraction import csv_to_object
from pdf_generation import generate_pdf


def main():
    csv_file = 'src/csv_store/24t3y8.csv'

    # Read a CSV file and generate a new Year object
    year = csv_to_object(csv_file)

    # Main loop - get student info
    try:
        while True:
            student_name = input("Enter a student name: ").strip().title()
            if student_name == "":
                break
            student = year.get_student(student_name)
            if student is None:
                print("Student not found.")
            else:
                student.pretty_print()
                generate_pdf("Steve", "Path To Advanced", [
                    "Topic 1", "Topic 2"], student)
    except KeyboardInterrupt:
        print()
        print("Keyboard interrupt received, shutting down...")
    finally:
        print("Goodbye!")


if __name__ == '__main__':
    main()
