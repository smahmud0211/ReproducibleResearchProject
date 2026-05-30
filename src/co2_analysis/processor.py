import pandas as pd


class DataProcessor:
    """
    Processes and prepares CO2 emissions data similarly to the reference R script.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def remove_missing_values(self) -> pd.DataFrame:
        """
        Clean and prepare the OWID CO2 dataset.

        This follows the R reference logic:
        - keep rows from 1960 onwards
        - require CO2 per capita, GDP, and population
        - compute GDP per capita
        - keep total CO2 emissions
        """

        df = self.dataframe.copy()

        required_columns = [
            "country",
            "iso_code",
            "year",
            "co2_per_capita",
            "co2",
            "gdp",
            "population",
        ]

        df = df[required_columns]

        df = df[
            df["co2_per_capita"].notna()
            & df["gdp"].notna()
            & df["population"].notna()
            & (df["population"] > 0)
            & (df["year"] >= 1960)
        ]

        df = df.copy()

        df["co2_pc"] = df["co2_per_capita"]
        df["total_co2"] = df["co2"]
        df["gdp_pc"] = df["gdp"] / df["population"]

        return df


if __name__ == "__main__":
    from data_loader import DataLoader

    loader = DataLoader("data/raw/owid-co2-data.csv")
    data = loader.load_data()

    processor = DataProcessor(data)
    clean_data = processor.remove_missing_values()

    print(clean_data.head())
    print(clean_data.shape)