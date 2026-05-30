import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class CO2Visualizer:
    """
    Creates visualizations similar to the reference R project.
    """

    def __init__(self, output_dir: str = "outputs/figures"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _minimal_theme(self):
        """
        Apply a simple theme similar to ggplot2 theme_minimal().
        """
        plt.grid(True, color="#e5e5e5", linewidth=1)
        ax = plt.gca()
        ax.set_facecolor("white")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    def _save(self, filename: str):
        """
        Save current plot to the output folder.
        """
        plt.tight_layout()
        plt.savefig(
            os.path.join(self.output_dir, filename),
            bbox_inches="tight",
            dpi=150,
        )
        plt.close()

    def _latest_per_country(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Return the latest available row for each country.
        """
        country_df = df[
            df["iso_code"].notna()
            & ~df["iso_code"].astype(str).str.startswith("OWID")
        ]

        idx = country_df.groupby(["iso_code", "country"])["year"].idxmax()
        return country_df.loc[idx].reset_index(drop=True)

    def plot_all(self, df: pd.DataFrame):
        """
        Generate and save all visualizations from the reference R workflow.
        """

        df = df.copy()
        latest = self._latest_per_country(df)

        # ------------------------------------------------------------------
        # 1. Global average CO2 per capita over time
        # ------------------------------------------------------------------
        global_ts = (
            df.groupby("year", as_index=False)["co2_pc"]
            .mean()
            .rename(columns={"co2_pc": "avg_co2_pc"})
        )

        plt.figure(figsize=(10, 6))
        plt.plot(global_ts["year"], global_ts["avg_co2_pc"], color="forestgreen")
        self._minimal_theme()
        plt.title("Global Average CO2 per Capita Over Time", fontsize=18)
        plt.xlabel("Date", fontsize=13)
        plt.ylabel("t CO2 per Capita", fontsize=13)
        self._save("01_global_average_co2_per_capita.png")

        # ------------------------------------------------------------------
        # 2. GDP per capita vs CO2 per capita with smooth curve
        # ------------------------------------------------------------------
        latest_gdp = latest.dropna(subset=["gdp_pc", "co2_pc"])

        x = latest_gdp["gdp_pc"].to_numpy()
        y = latest_gdp["co2_pc"].to_numpy()

        order = np.argsort(x)
        x_sorted = x[order]
        y_sorted = y[order]

        # Polynomial smoothing as a simple replacement for R loess
        x_scaled = (x_sorted - x_sorted.mean()) / x_sorted.std()
        smooth_coeff = np.polyfit(x_scaled, y_sorted, deg=3)
        smooth_line = np.poly1d(smooth_coeff)(x_scaled)

        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, alpha=0.5, color="gray", edgecolor="black", linewidth=0.3)
        plt.plot(x_sorted, smooth_line, color="darkred", linewidth=3)
        self._minimal_theme()
        plt.title("GDP per Capita vs CO2 per Capita (Latest)", fontsize=18)
        plt.xlabel("GDP per Capita (USD)", fontsize=13)
        plt.ylabel("t CO2 per Capita", fontsize=13)
        self._save("02_gdp_per_capita_vs_co2_per_capita.png")

        # ------------------------------------------------------------------
        # 3. Linear regression plot
        # ------------------------------------------------------------------
        regression_coeff = np.polyfit(x, y, deg=1)
        regression_line = np.poly1d(regression_coeff)

        y_pred = regression_line(x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        x_line = np.linspace(x.min(), x.max(), 300)
        y_line = regression_line(x_line)

        residual_std = np.std(y - y_pred)
        upper = y_line + 1.96 * residual_std
        lower = y_line - 1.96 * residual_std

        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, alpha=0.35, color="gray", edgecolor="black", linewidth=0.3)
        plt.plot(x_line, y_line, color="blue", linewidth=3)
        plt.fill_between(x_line, lower, upper, color="gray", alpha=0.25)
        self._minimal_theme()
        plt.title(
            "Linear Regression: CO2 per Capita ~ GDP per Capita",
            fontsize=18,
        )
        plt.suptitle(f"R²={r_squared:.3f}", x=0.14, y=0.88, ha="left", fontsize=13)
        plt.xlabel("GDP per Capita (USD)", fontsize=13)
        plt.ylabel("t CO2 per Capita", fontsize=13)
        self._save("03_linear_regression_gdp_co2.png")

        # ------------------------------------------------------------------
        # 4. Top 10 countries by CO2 per capita
        # ------------------------------------------------------------------
        top10_pc = latest.sort_values("co2_pc", ascending=False).head(10)

        plt.figure(figsize=(10, 6))
        plt.barh(top10_pc["country"], top10_pc["co2_pc"], color="darkslateblue")
        plt.gca().invert_yaxis()
        self._minimal_theme()
        plt.title("Top 10 Countries by CO2 per Capita (Latest)", fontsize=18)
        plt.xlabel("t CO2 per Capita", fontsize=13)
        plt.ylabel("")
        self._save("04_top_10_co2_per_capita.png")

        # ------------------------------------------------------------------
        # 5. CO2 per capita over time: Top 5 countries
        # ------------------------------------------------------------------
        top5_codes = top10_pc["iso_code"].head(5).tolist()
        ts_top5 = df[df["iso_code"].isin(top5_codes)]

        plt.figure(figsize=(10, 6))
        for country, group in ts_top5.groupby("country"):
            plt.plot(group["year"], group["co2_pc"], label=country, linewidth=2)

        self._minimal_theme()
        plt.title("CO2 per Capita Over Time: Top 5 Countries", fontsize=18)
        plt.xlabel("Date", fontsize=13)
        plt.ylabel("t CO2 per Capita", fontsize=13)
        plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc="upper left")
        self._save("05_top_5_time_series.png")

        # ------------------------------------------------------------------
        # 6. GDP quartile boxplot
        # ------------------------------------------------------------------
        latest_q = latest.dropna(subset=["gdp_pc", "co2_pc"]).copy()
        latest_q["gdp_q"] = pd.qcut(
            latest_q["gdp_pc"],
            4,
            labels=["1", "2", "3", "4"],
        )

        quartile_groups = [
            latest_q[latest_q["gdp_q"] == q]["co2_pc"] for q in ["1", "2", "3", "4"]
        ]

        plt.figure(figsize=(10, 6))
        box = plt.boxplot(
            quartile_groups,
            labels=["1", "2", "3", "4"],
            patch_artist=True,
        )

        colors = ["#440154", "#31688e", "#35b779", "#fde725"]
        for patch, color in zip(box["boxes"], colors):
            patch.set_facecolor(color)

        self._minimal_theme()
        plt.title("CO2 per Capita by GDP per Capita Quartile", fontsize=18)
        plt.xlabel("GDP Quartile", fontsize=13)
        plt.ylabel("t CO2 per Capita", fontsize=13)
        self._save("06_boxplot_co2_by_gdp_quartile.png")

        # ------------------------------------------------------------------
        # 7. GDP quartile violin plot
        # ------------------------------------------------------------------
        plt.figure(figsize=(10, 6))
        violin = plt.violinplot(quartile_groups, showmeans=False, showmedians=False)

        violin_colors = ["#440154", "#22c7a9", "#f9a825", "#8b0000"]
        for body, color in zip(violin["bodies"], violin_colors):
            body.set_facecolor(color)
            body.set_edgecolor("black")
            body.set_alpha(0.85)

        plt.xticks([1, 2, 3, 4], ["1", "2", "3", "4"])
        self._minimal_theme()
        plt.title("Distribution of CO2 per Capita by GDP Quartile", fontsize=18)
        plt.xlabel("GDP Quartile", fontsize=13)
        plt.ylabel("t CO2 per Capita", fontsize=13)
        self._save("07_violin_co2_by_gdp_quartile.png")

        # ------------------------------------------------------------------
        # 8. Heatmap: avg CO2 per capita by year and GDP quartile
        # ------------------------------------------------------------------
        heat_data = df.merge(
            latest_q[["iso_code", "gdp_q"]],
            on="iso_code",
            how="inner",
        )

        heat_data = (
            heat_data.groupby(["year", "gdp_q"], as_index=False)["co2_pc"]
            .mean()
            .rename(columns={"co2_pc": "avg_pc"})
        )

        heat_pivot = heat_data.pivot(
            index="gdp_q",
            columns="year",
            values="avg_pc",
        )

        plt.figure(figsize=(12, 6))
        plt.imshow(
            heat_pivot,
            aspect="auto",
            cmap="viridis",
            origin="lower",
        )
        plt.colorbar(label="Avg t CO2 per Capita")
        plt.yticks(range(len(heat_pivot.index)), heat_pivot.index)
        plt.xticks(
            ticks=np.linspace(0, len(heat_pivot.columns) - 1, 6),
            labels=[
                int(heat_pivot.columns[int(i)])
                for i in np.linspace(0, len(heat_pivot.columns) - 1, 6)
            ],
        )
        plt.title("Avg CO2 per Capita by Year & GDP Quartile", fontsize=18)
        plt.xlabel("Year", fontsize=13)
        plt.ylabel("GDP Quartile", fontsize=13)
        self._save("08_heatmap_year_gdp_quartile.png")

        # ------------------------------------------------------------------
        # 9. Cumulative sum of CO2 per capita over time
        # ------------------------------------------------------------------
        cum_pc = (
            df.groupby("year", as_index=False)["co2_pc"]
            .sum()
            .rename(columns={"co2_pc": "sum_pc"})
        )
        cum_pc["cum_pc"] = cum_pc["sum_pc"].cumsum()

        plt.figure(figsize=(10, 6))
        plt.plot(cum_pc["year"], cum_pc["cum_pc"], color="purple", linewidth=2)
        self._minimal_theme()
        plt.title("Cumulative Sum of CO2 per Capita Over Time", fontsize=18)
        plt.xlabel("Date", fontsize=13)
        plt.ylabel("Cumulative t CO2 per Capita", fontsize=13)
        self._save("09_cumulative_co2_per_capita.png")

        # ------------------------------------------------------------------
        # 10. Year-over-year percentage change
        # ------------------------------------------------------------------
        global_ts["pct"] = (
            100
            * (global_ts["avg_co2_pc"] - global_ts["avg_co2_pc"].shift(1))
            / global_ts["avg_co2_pc"].shift(1)
        )

        plt.figure(figsize=(10, 6))
        plt.plot(global_ts["year"], global_ts["pct"], color="orange", linewidth=2)
        self._minimal_theme()
        plt.title(
            "Year-over-Year % Change in Global Avg CO2 per Capita",
            fontsize=18,
        )
        plt.xlabel("Date", fontsize=13)
        plt.ylabel("% Change", fontsize=13)
        self._save("10_yoy_change_global_avg_co2.png")

        # ------------------------------------------------------------------
        # 11. CO2 per capita vs total CO2 emissions
        # ------------------------------------------------------------------
        latest_total = latest.dropna(subset=["total_co2", "co2_pc"]).copy()
        latest_total = latest_total[latest_total["total_co2"] > 0]

        x_total = latest_total["total_co2"].to_numpy()
        y_pc = latest_total["co2_pc"].to_numpy()

        log_x = np.log10(x_total)
        total_coeff = np.polyfit(log_x, y_pc, deg=1)
        total_line = np.poly1d(total_coeff)

        x_line_log = np.linspace(log_x.min(), log_x.max(), 300)
        y_line_total = total_line(x_line_log)

        plt.figure(figsize=(10, 6))
        plt.scatter(x_total, y_pc, alpha=0.5, color="gray", edgecolor="black", linewidth=0.3)
        plt.plot(10**x_line_log, y_line_total, color="darkgreen", linewidth=3)
        plt.xscale("log")
        self._minimal_theme()
        plt.title("CO2 per Capita vs Total CO2 Emissions (Latest)", fontsize=18)
        plt.xlabel("Total CO2 (Mt, log scale)", fontsize=13)
        plt.ylabel("t CO2 per Capita", fontsize=13)
        self._save("11_total_vs_per_capita.png")