import matplotlib.pyplot as plt


class CO2Visualizer:
    """
    Creates visualizations for CO2 emissions analysis.
    """

    def plot_global_emissions(self, dataframe):
        plt.figure(figsize=(10, 5))
        plt.plot(dataframe["year"], dataframe["total_co2"])
        plt.title("Global CO2 Emissions Over Time")
        plt.xlabel("Year")
        plt.ylabel("CO2 Emissions")
        plt.tight_layout()
        plt.show()