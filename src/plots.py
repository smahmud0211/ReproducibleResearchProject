"""
Generate visualizations for the CO2 emissions analysis project.

This module defines a CO2Visualizer class that creates the figures
used in the final report and reproduces the main visualizations from
the original R-based CO2 analysis project.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CLEAN_FILE = Path("data/processed/co2_clean.csv")
FIGURES_DIR = Path("outputs/figures")


class CO2Visualizer:
    """
    Generate and save CO2 emissions visualizations.
    """

    def __init__(self, clean_file: Path = CLEAN_FILE, figures_dir: Path = FIGURES_DIR):
        """
        Initialize input and output paths.
        """
        self.clean_file = clean_file
        self.figures_dir = figures_dir
        self.df = pd.read_csv(self.clean_file)
        self.latest = self.latest_country_data()
        self.latest_q = self.add_gdp_quartile()

    def save(self, name: str) -> None:
        """
        Save the current matplotlib figure to the figures directory.
        """
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(self.figures_dir / name, dpi=150)
        plt.close()
        print(f"Saved {self.figures_dir / name}")

    def latest_country_data(self) -> pd.DataFrame:
        """
        Return the latest available observation for each country.
        """
        countries = self.df[self.df["iso_code"].notna()].copy()
        return (
            countries.sort_values("year")
            .groupby(["iso_code", "country"], as_index=False)
            .tail(1)
        )

    def add_gdp_quartile(self) -> pd.DataFrame:
        """
        Assign countries to GDP-per-capita quartiles.
        """
        out = self.latest.copy()
        out["gdp_quartile"] = pd.qcut(
            out["gdp_per_capita"],
            4,
            labels=["Q1", "Q2", "Q3", "Q4"],
        )
        return out

    def plot_01_global_avg_co2_pc(self) -> None:
        """
        Plot global average CO2 emissions per capita over time.
        """
        data = self.df.groupby("year", as_index=False)["co2_pc"].mean()

        plt.figure(figsize=(10, 6))
        plt.plot(data["year"], data["co2_pc"])
        plt.title("Global Average CO2 per Capita Over Time")
        plt.xlabel("Year")
        plt.ylabel("t CO2 per Capita")
        plt.grid(True)

        self.save("01_global_average_co2_per_capita.png")

    def plot_02_gdp_vs_co2_pc(self) -> None:
        """
        Plot GDP per capita against CO2 emissions per capita.
        """
        plt.figure(figsize=(10, 6))
        sns.regplot(
            data=self.latest,
            x="gdp_per_capita",
            y="co2_pc",
            lowess=True,
            scatter_kws={"alpha": 0.5},
            line_kws={"color": "red"},
        )
        plt.title("GDP per Capita vs CO2 per Capita (Latest)")
        plt.xlabel("GDP per Capita")
        plt.ylabel("t CO2 per Capita")

        self.save("02_gdp_vs_co2_per_capita_latest.png")

    def plot_03_linear_regression(self) -> None:
        """
        Plot the linear relationship between GDP per capita and CO2 per capita.
        """
        plt.figure(figsize=(10, 6))
        sns.regplot(
            data=self.latest,
            x="gdp_per_capita",
            y="co2_pc",
            scatter_kws={"alpha": 0.35},
            line_kws={"color": "blue"},
        )
        plt.title("Linear Regression: CO2 per Capita ~ GDP per Capita")
        plt.xlabel("GDP per Capita")
        plt.ylabel("t CO2 per Capita")

        self.save("03_linear_regression_co2_pc_gdp_pc.png")

    def plot_04_top10_co2_pc(self) -> None:
        """
        Plot the top 10 countries by CO2 emissions per capita.
        """
        top10 = self.latest.sort_values("co2_pc", ascending=False).head(10)

        plt.figure(figsize=(10, 6))
        sns.barplot(data=top10, x="co2_pc", y="country")
        plt.title("Top 10 Countries by CO2 per Capita (Latest)")
        plt.xlabel("t CO2 per Capita")
        plt.ylabel("")

        self.save("04_top10_co2_per_capita.png")

    def plot_05_top5_time_series(self) -> None:
        """
        Plot CO2 emissions per capita over time for the top 5 countries.
        """
        top5_codes = (
            self.latest.sort_values("co2_pc", ascending=False)
            .head(5)["iso_code"]
            .tolist()
        )
        data = self.df[self.df["iso_code"].isin(top5_codes)]

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=data, x="year", y="co2_pc", hue="country")
        plt.title("CO2 per Capita Over Time: Top 5 Countries")
        plt.xlabel("Year")
        plt.ylabel("t CO2 per Capita")

        self.save("05_top5_co2_per_capita_time_series.png")

    def plot_06_boxplot_gdp_quartile(self) -> None:
        """
        Plot CO2 per capita by GDP quartile using a boxplot.
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.latest_q, x="gdp_quartile", y="co2_pc")
        plt.title("CO2 per Capita by GDP per Capita Quartile")
        plt.xlabel("GDP Quartile")
        plt.ylabel("t CO2 per Capita")

        self.save("06_co2_per_capita_by_gdp_quartile_boxplot.png")

    def plot_07_violin_gdp_quartile(self) -> None:
        """
        Plot CO2 per capita by GDP quartile using a violin plot.
        """
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=self.latest_q, x="gdp_quartile", y="co2_pc")
        plt.title("Distribution of CO2 per Capita by GDP Quartile")
        plt.xlabel("GDP Quartile")
        plt.ylabel("t CO2 per Capita")

        self.save("07_co2_per_capita_by_gdp_quartile_violin.png")

    def plot_08_heatmap(self) -> None:
        """
        Plot a heatmap of average CO2 per capita by year and GDP quartile.
        """
        quartiles = self.latest_q[["iso_code", "gdp_quartile"]]
        data = self.df.merge(quartiles, on="iso_code", how="inner")

        pivot = (
            data.groupby(["gdp_quartile", "year"], observed=False)["co2_pc"]
            .mean()
            .reset_index()
        )
        pivot = pivot.pivot(index="gdp_quartile", columns="year", values="co2_pc")

        plt.figure(figsize=(12, 5))
        sns.heatmap(pivot, cmap="viridis")
        plt.title("Average CO2 per Capita by Year and GDP Quartile")
        plt.xlabel("Year")
        plt.ylabel("GDP Quartile")

        self.save("08_heatmap_avg_co2_per_capita_by_year_gdp_quartile.png")

    def plot_09_cumulative_sum_pc(self) -> None:
        """
        Plot the cumulative sum of average CO2 per capita over time.
        """
        data = self.df.groupby("year", as_index=False)["co2_pc"].sum().sort_values("year")
        data["cumulative_co2_pc"] = data["co2_pc"].cumsum()

        plt.figure(figsize=(10, 6))
        plt.plot(data["year"], data["cumulative_co2_pc"])
        plt.title("Cumulative Sum of CO2 per Capita Over Time")
        plt.xlabel("Year")
        plt.ylabel("Cumulative t CO2 per Capita")
        plt.grid(True)

        self.save("09_cumulative_sum_co2_per_capita.png")

    def plot_10_yearly_percent_change(self) -> None:
        """
        Plot year-over-year percentage change in average CO2 per capita.
        """
        data = self.df.groupby("year", as_index=False)["co2_pc"].mean().sort_values("year")
        data["percent_change"] = data["co2_pc"].pct_change() * 100

        plt.figure(figsize=(10, 6))
        plt.plot(data["year"], data["percent_change"])
        plt.title("Year-over-Year % Change in Global Avg CO2 per Capita")
        plt.xlabel("Year")
        plt.ylabel("% Change")
        plt.grid(True)

        self.save("10_year_over_year_change_global_avg_co2_pc.png")

    def plot_11_co2_pc_vs_total_co2(self) -> None:
        """
        Plot CO2 per capita against total CO2 emissions.
        """
        data = self.latest[
            (self.latest["total_co2"] > 0) & self.latest["co2_pc"].notna()
        ]

        plt.figure(figsize=(10, 6))
        sns.regplot(
            data=data,
            x="total_co2",
            y="co2_pc",
            scatter_kws={"alpha": 0.5},
            line_kws={"color": "green"},
        )
        plt.xscale("log")
        plt.title("CO2 per Capita vs Total CO2 Emissions (Latest)")
        plt.xlabel("Total CO2 Emissions, Mt (log scale)")
        plt.ylabel("t CO2 per Capita")

        self.save("11_co2_per_capita_vs_total_co2.png")

    def run(self) -> None:
        """
        Generate all project visualizations.
        """
        self.plot_01_global_avg_co2_pc()
        self.plot_02_gdp_vs_co2_pc()
        self.plot_03_linear_regression()
        self.plot_04_top10_co2_pc()
        self.plot_05_top5_time_series()
        self.plot_06_boxplot_gdp_quartile()
        self.plot_07_violin_gdp_quartile()
        self.plot_08_heatmap()
        self.plot_09_cumulative_sum_pc()
        self.plot_10_yearly_percent_change()
        self.plot_11_co2_pc_vs_total_co2()


def main() -> None:
    """
    Run the visualization pipeline.
    """
    visualizer = CO2Visualizer()
    visualizer.run()


if __name__ == "__main__":
    main()