"""
Generate visualizations for the CO2 emissions analysis project.

This module creates the figures used in the final report and reproduces
the main visualizations from the original R-based CO2 analysis project.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CLEAN_FILE = Path("data/processed/co2_clean.csv")
FIGURES_DIR = Path("outputs/figures")


def save(name: str) -> None:
    """
    Save the current matplotlib figure to the outputs/figures directory.

    Args:
        name: File name of the figure to be saved.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / name, dpi=150)
    plt.close()
    print(f"Saved {FIGURES_DIR / name}")


def latest_country_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return the latest available observation for each country.

    Only observations with an ISO code are kept, which helps remove
    regional aggregates and keeps the focus on country-level data.

    Args:
        df: Cleaned CO2 dataset.

    Returns:
        A DataFrame containing the most recent observation for each country.
    """
    countries = df[df["iso_code"].notna()].copy()
    return (
        countries.sort_values("year")
        .groupby(["iso_code", "country"], as_index=False)
        .tail(1)
    )


def plot_01_global_avg_co2_pc(df: pd.DataFrame) -> None:
    """
    Plot the global average CO2 emissions per capita over time.

    Args:
        df: Cleaned CO2 dataset.
    """
    data = df.groupby("year", as_index=False)["co2_pc"].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(data["year"], data["co2_pc"])
    plt.title("Global Average CO2 per Capita Over Time")
    plt.xlabel("Year")
    plt.ylabel("t CO2 per Capita")
    plt.grid(True)

    save("01_global_average_co2_per_capita.png")


def plot_02_gdp_vs_co2_pc(latest: pd.DataFrame) -> None:
    """
    Plot GDP per capita against CO2 emissions per capita.

    Args:
        latest: Latest available country-level observations.
    """
    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=latest,
        x="gdp_per_capita",
        y="co2_pc",
        lowess=True,
        scatter_kws={"alpha": 0.5},
        line_kws={"color": "red"},
    )
    plt.title("GDP per Capita vs CO2 per Capita (Latest)")
    plt.xlabel("GDP per Capita")
    plt.ylabel("t CO2 per Capita")

    save("02_gdp_vs_co2_per_capita_latest.png")


def plot_03_linear_regression(latest: pd.DataFrame) -> None:
    """
    Plot the linear relationship between GDP per capita and CO2 per capita.

    Args:
        latest: Latest available country-level observations.
    """
    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=latest,
        x="gdp_per_capita",
        y="co2_pc",
        scatter_kws={"alpha": 0.35},
        line_kws={"color": "blue"},
    )
    plt.title("Linear Regression: CO2 per Capita ~ GDP per Capita")
    plt.xlabel("GDP per Capita")
    plt.ylabel("t CO2 per Capita")

    save("03_linear_regression_co2_pc_gdp_pc.png")


def plot_04_top10_co2_pc(latest: pd.DataFrame) -> None:
    """
    Plot the top 10 countries by CO2 emissions per capita.

    Args:
        latest: Latest available country-level observations.
    """
    top10 = latest.sort_values("co2_pc", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top10, x="co2_pc", y="country")
    plt.title("Top 10 Countries by CO2 per Capita (Latest)")
    plt.xlabel("t CO2 per Capita")
    plt.ylabel("")

    save("04_top10_co2_per_capita.png")


def plot_05_top5_time_series(df: pd.DataFrame, latest: pd.DataFrame) -> None:
    """
    Plot CO2 emissions per capita over time for the top 5 countries.

    Args:
        df: Cleaned CO2 dataset.
        latest: Latest available country-level observations.
    """
    top5_codes = latest.sort_values("co2_pc", ascending=False).head(5)[
        "iso_code"
    ].tolist()
    data = df[df["iso_code"].isin(top5_codes)]

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data, x="year", y="co2_pc", hue="country")
    plt.title("CO2 per Capita Over Time: Top 5 Countries")
    plt.xlabel("Year")
    plt.ylabel("t CO2 per Capita")

    save("05_top5_co2_per_capita_time_series.png")


def add_gdp_quartile(latest: pd.DataFrame) -> pd.DataFrame:
    """
    Assign countries to GDP-per-capita quartiles.

    Args:
        latest: Latest available country-level observations.

    Returns:
        A DataFrame with an additional GDP quartile column.
    """
    out = latest.copy()
    out["gdp_quartile"] = pd.qcut(
        out["gdp_per_capita"],
        4,
        labels=["Q1", "Q2", "Q3", "Q4"],
    )
    return out


def plot_06_boxplot_gdp_quartile(latest_q: pd.DataFrame) -> None:
    """
    Plot CO2 per capita by GDP quartile using a boxplot.

    Args:
        latest_q: Latest country-level observations with GDP quartile labels.
    """
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=latest_q, x="gdp_quartile", y="co2_pc")
    plt.title("CO2 per Capita by GDP per Capita Quartile")
    plt.xlabel("GDP Quartile")
    plt.ylabel("t CO2 per Capita")

    save("06_co2_per_capita_by_gdp_quartile_boxplot.png")


def plot_07_violin_gdp_quartile(latest_q: pd.DataFrame) -> None:
    """
    Plot CO2 per capita by GDP quartile using a violin plot.

    Args:
        latest_q: Latest country-level observations with GDP quartile labels.
    """
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=latest_q, x="gdp_quartile", y="co2_pc")
    plt.title("Distribution of CO2 per Capita by GDP Quartile")
    plt.xlabel("GDP Quartile")
    plt.ylabel("t CO2 per Capita")

    save("07_co2_per_capita_by_gdp_quartile_violin.png")


def plot_08_heatmap(df: pd.DataFrame, latest_q: pd.DataFrame) -> None:
    """
    Plot a heatmap of average CO2 per capita by year and GDP quartile.

    Args:
        df: Cleaned CO2 dataset.
        latest_q: Latest country-level observations with GDP quartile labels.
    """
    quartiles = latest_q[["iso_code", "gdp_quartile"]]
    data = df.merge(quartiles, on="iso_code", how="inner")

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

    save("08_heatmap_avg_co2_per_capita_by_year_gdp_quartile.png")


def plot_09_cumulative_sum_pc(df: pd.DataFrame) -> None:
    """
    Plot the cumulative sum of average CO2 per capita over time.

    Args:
        df: Cleaned CO2 dataset.
    """
    data = df.groupby("year", as_index=False)["co2_pc"].sum().sort_values("year")
    data["cumulative_co2_pc"] = data["co2_pc"].cumsum()

    plt.figure(figsize=(10, 6))
    plt.plot(data["year"], data["cumulative_co2_pc"])
    plt.title("Cumulative Sum of CO2 per Capita Over Time")
    plt.xlabel("Year")
    plt.ylabel("Cumulative t CO2 per Capita")
    plt.grid(True)

    save("09_cumulative_sum_co2_per_capita.png")


def plot_10_yearly_percent_change(df: pd.DataFrame) -> None:
    """
    Plot year-over-year percentage change in average CO2 per capita.

    Args:
        df: Cleaned CO2 dataset.
    """
    data = df.groupby("year", as_index=False)["co2_pc"].mean().sort_values("year")
    data["percent_change"] = data["co2_pc"].pct_change() * 100

    plt.figure(figsize=(10, 6))
    plt.plot(data["year"], data["percent_change"])
    plt.title("Year-over-Year % Change in Global Avg CO2 per Capita")
    plt.xlabel("Year")
    plt.ylabel("% Change")
    plt.grid(True)

    save("10_year_over_year_change_global_avg_co2_pc.png")


def plot_11_co2_pc_vs_total_co2(latest: pd.DataFrame) -> None:
    """
    Plot CO2 per capita against total CO2 emissions.

    Args:
        latest: Latest available country-level observations.
    """
    data = latest[(latest["total_co2"] > 0) & latest["co2_pc"].notna()]

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

    save("11_co2_per_capita_vs_total_co2.png")


def main() -> None:
    """
    Generate all CO2 analysis figures and save them to outputs/figures.
    """
    df = pd.read_csv(CLEAN_FILE)
    latest = latest_country_data(df)
    latest_q = add_gdp_quartile(latest)

    plot_01_global_avg_co2_pc(df)
    plot_02_gdp_vs_co2_pc(latest)
    plot_03_linear_regression(latest)
    plot_04_top10_co2_pc(latest)
    plot_05_top5_time_series(df, latest)
    plot_06_boxplot_gdp_quartile(latest_q)
    plot_07_violin_gdp_quartile(latest_q)
    plot_08_heatmap(df, latest_q)
    plot_09_cumulative_sum_pc(df)
    plot_10_yearly_percent_change(df)
    plot_11_co2_pc_vs_total_co2(latest)


if __name__ == "__main__":
    main()