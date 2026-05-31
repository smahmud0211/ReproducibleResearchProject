"""
Clean and preprocess the OWID CO2 dataset.

The script filters observations, creates GDP per capita,
selects the variables used in the analysis, and saves a
processed dataset for visualization and regression modeling.
"""

from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/owid-co2-data.csv")

PROCESSED_DIR = Path("data/processed")
CLEAN_FILE = PROCESSED_DIR / "co2_clean.csv"


def main():
    """
    Load the raw CO2 dataset, clean the data, and save a
    processed version for downstream analysis.

    The cleaning process:
    - Keeps observations from 1960 onward.
    - Removes rows with missing CO2 per capita or GDP values.
    - Calculates GDP per capita.
    - Selects and renames analysis variables.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_FILE)

    # Keep observations from 1960 onward with required values.
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

    clean.to_csv(CLEAN_FILE, index=False)

    print(f"Cleaned data saved to {CLEAN_FILE}")
    print(f"Rows: {clean.shape[0]}, Columns: {clean.shape[1]}")


if __name__ == "__main__":
    main()