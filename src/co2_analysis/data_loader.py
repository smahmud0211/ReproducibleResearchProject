import pandas as pd


class DataLoader:
    """
    Loads CO2 emissions data from a CSV file.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV.
        """
        return pd.read_csv(self.filepath)


if __name__ == "__main__":
    loader = DataLoader("data/raw/owid-co2-data.csv")
    data = loader.load_data()

    print(data.head())