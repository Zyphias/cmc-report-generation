import sys
import pandas as pd
from src.classes.Year import Year


def csv_to_object(csv_file: str = './csv_store/24t3y9.csv') -> Year:
    """Read a CSV file and generate a new Year object associated with it."""

    # Open the CSV file
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        sys.exit(
            "Error: File not found. Please ensure provided information is correct!")

    return Year('10', '24t3')
