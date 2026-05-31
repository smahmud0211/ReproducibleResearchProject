"""
Download the OWID CO2 dataset and save it locally.

The script retrieves the latest CO2 dataset from Our World in Data
and stores it in the data/raw directory for further processing.
"""

from pathlib import Path

import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

RAW_DIR = Path("data/raw")
RAW_FILE = RAW_DIR / "owid-co2-data.csv"


def main():
    """
    Download the OWID CO2 dataset and save it as a CSV file.

    Creates the raw data directory if it does not exist and
    prints basic information about the downloaded dataset.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_URL)
    df.to_csv(RAW_FILE, index=False)

    print(f"Downloaded dataset to {RAW_FILE}")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")


if __name__ == "__main__":
    main()