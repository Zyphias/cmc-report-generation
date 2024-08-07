from data_extraction import csv_to_object


def main():
    csv_file = 'src/csv_store/24t3y9.csv'

    # Read a CSV file and generate a new Year object
    year = csv_to_object(csv_file)
    print("Program finished. Success!")
    pass


if __name__ == '__main__':
    main()
