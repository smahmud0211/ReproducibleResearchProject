"""
Clean and preprocess the OWID CO2 dataset.

This module uses a DataCleaner class to filter the raw dataset,
create GDP per capita, and save a processed dataset for analysis.
"""

from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/owid-co2-data.csv")
PROCESSED_DIR = Path("data/processed")
CLEAN_FILE = PROCESSED_DIR / "co2_clean.csv"


class DataCleaner:
    """
    Clean the OWID CO2 dataset and save the processed output.
    """

    def __init__(self, raw_file: Path = RAW_FILE, output_file: Path = CLEAN_FILE):
        """
        Initialize input and output paths.
        """
        self.raw_file = raw_file
        self.output_file = output_file

    def run(self) -> None:
        """
        Execute the complete data cleaning workflow.
        """
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

        df = pd.read_csv(self.raw_file)

        df = df[
            (df["year"] >= 1960)
            & df["co2_per_capita"].notna()
            & df["gdp"].notna()
            & (df["population"] > 0)
        ].copy()

        df["gdp_per_capita"] = df["gdp"] / df["population"]

        clean = df[
            [
                "country",
                "iso_code",
                "year",
                "population",
                "gdp",
                "gdp_per_capita",
                "co2_per_capita",
                "co2",
                "cumulative_co2",
                "share_global_co2",
            ]
        ].rename(
            columns={
                "co2_per_capita": "co2_pc",
                "co2": "total_co2",
            }
        )

        clean.to_csv(self.output_file, index=False)

        print(f"Cleaned data saved to {self.output_file}")
        print(f"Rows: {clean.shape[0]}, Columns: {clean.shape[1]}")


def main() -> None:
    """
    Run the data cleaner.
    """
    cleaner = DataCleaner()
    cleaner.run()


if __name__ == "__main__":
    main()