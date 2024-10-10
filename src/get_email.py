import pandas as pd


def get_contact_email(student_name: str) -> str:
    # Split at the last space
    first_name, last_name = student_name.rsplit(' ', 1)

    # open csv file
    df = pd.read_csv("src/csv_store/contacts.csv")
    # search for student first and last name
    for _, row in df.iterrows():
        if row["First Name"] + " " + row["Last Name"] == student_name:
            return row["Parent Contact 1 Email"]

    # if no email found, warn user
    return "WARNING: NO PARENT EMAIL"
