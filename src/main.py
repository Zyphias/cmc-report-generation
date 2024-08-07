from data_extraction import csv_to_object


def main():
    csv_file = 'src/csv_store/24t3y9.csv'

    # Read a CSV file and generate a new Year object
    year = csv_to_object(csv_file)

    # Test student methods

    try:
        while True:
            student_name = input("Enter a student name: ").strip()
            if student_name == "":
                break
            student = year.get_student(student_name)
            if student is None:
                print("Student not found.")
            else:
                student.pretty_print()
    except KeyboardInterrupt:
        print()
        print("Keyboard interrupt received, shutting down...")
    finally:
        print("Goodbye!")


if __name__ == '__main__':
    main()
