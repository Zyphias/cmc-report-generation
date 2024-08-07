import sys
import pandas as pd
from objects.year import Year


def csv_to_object(csv_file: str = './csv_store/24t3y9.csv') -> Year:
    """Read a CSV file and generate a new Year object associated with it."""

    # Open the CSV file
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        sys.exit(
            f"Error: File {csv_file} not found. Please ensure the file exists and try again.")

    return Year('10', '24t3')
