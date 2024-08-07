from data_extraction import csv_to_object


def main():
    csv_file = 'src/csv_store/24t3y9.csv'

    # Read a CSV file and generate a new Year object
    year = csv_to_object(csv_file)

    students = year.get_students()
    for student in students:
        print(student.get_name())

    student = year.get_student("grace mcmartin")
    if student is None:
        print("Student not found.")
    else:
        print(student.get_data().get_feedback())
        print(student.get_data().get_comments())

    print("Program finished. Success!")


if __name__ == '__main__':
    main()
