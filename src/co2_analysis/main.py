from data_loader import DataLoader
from processor import DataProcessor
from analyzer import CO2Analyzer
from visualizer import CO2Visualizer


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
    #visualizer.plot_global_emissions(global_data)
    #visualizer.plot_top_emitters(top_emitters)
    #visualizer.plot_gdp_vs_co2(clean_data)
    #visualizer.plot_top_5_time_series(clean_data)

    print("Pipeline completed.")
    print(global_data.head())
    print(top_emitters.head())


if __name__ == "__main__":
    main()