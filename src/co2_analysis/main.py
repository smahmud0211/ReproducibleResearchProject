from co2_analysis.data_loader import DataLoader
from co2_analysis.processor import DataProcessor
from co2_analysis.analyzer import CO2Analyzer
from co2_analysis.visualizer import CO2Visualizer


def main():
    loader = DataLoader("data/raw/owid-co2-data.csv")
    raw_data = loader.load_data()

    processor = DataProcessor(raw_data)
    clean_data = processor.remove_missing_values()

    analyzer = CO2Analyzer(clean_data)
    global_data = analyzer.global_emissions_by_year()
    top_emitters = analyzer.top_emitters(year=2022)

    visualizer = CO2Visualizer()
    visualizer.plot_all(clean_data)

    print("Pipeline completed.")
    print(global_data.head())
    print(top_emitters.head())


if __name__ == "__main__":
    main()