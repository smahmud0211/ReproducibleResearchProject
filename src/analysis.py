"""
Run regression analysis for the CO2 emissions project.

This module estimates the relationship between GDP per capita and
CO2 emissions per capita using the cleaned OWID CO2 dataset.
The results are saved as text and CSV files for the final report.
"""

from pathlib import Path

import pandas as pd
import statsmodels.api as sm

CLEAN_FILE = Path("data/processed/co2_clean.csv")
TABLES_DIR = Path("outputs/tables")


def latest_country_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return the latest available observation for each country.

    Args:
        df: Cleaned CO2 dataset.

    Returns:
        A DataFrame containing the most recent country-level observations.
    """
    countries = df[df["iso_code"].notna()].copy()
    return (
        countries.sort_values("year")
        .groupby(["iso_code", "country"], as_index=False)
        .tail(1)
    )


def main() -> None:
    """
    Estimate a linear regression model and save the results.

    The model follows the original R project idea:

        CO2 per capita ~ GDP per capita

    Outputs:
        - outputs/tables/regression_summary.txt
        - outputs/tables/regression_coefficients.csv
    """
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(CLEAN_FILE)
    latest = latest_country_data(df)
    model_data = latest[["country", "gdp_per_capita", "co2_pc"]].dropna()

    x = sm.add_constant(model_data["gdp_per_capita"])
    y = model_data["co2_pc"]

    model = sm.OLS(y, x).fit()

    summary_path = TABLES_DIR / "regression_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as file:
        file.write(model.summary().as_text())

    coefficients = pd.DataFrame(
        {
            "term": model.params.index,
            "estimate": model.params.values,
            "p_value": model.pvalues.values,
        }
    )
    coefficients.to_csv(TABLES_DIR / "regression_coefficients.csv", index=False)

    print("Regression completed: CO2 per capita ~ GDP per capita")
    print(f"R-squared: {model.rsquared:.3f}")
    print(f"Saved summary to {summary_path}")


if __name__ == "__main__":
    main()