import pandas as pd


class DataProcessor:
    """
    Processes and cleans CO2 emissions data.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def remove_missing_values(self) -> pd.DataFrame:
        """
        Remove rows with missing values.
        """
        return self.dataframe.dropna()


if __name__ == "__main__":
    from data_loader import DataLoader

    loader = DataLoader("data/raw/owid-co2-data.csv")
    data = loader.load_data()

    processor = DataProcessor(data)

    print(processor.remove_missing_values().head())