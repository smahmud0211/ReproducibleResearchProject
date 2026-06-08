"""
Generate the final project report.

This module defines a ReportGenerator class that creates a Markdown
report containing project overview, generated visualizations,
regression analysis results, and final conclusions.
"""

from pathlib import Path

REPORTS_DIR = Path("reports")
FIGURES_DIR = Path("outputs/figures")
TABLES_DIR = Path("outputs/tables")
REPORT_FILE = REPORTS_DIR / "generated_report.md"


class ReportGenerator:
    """
    Generate a Markdown report from project outputs.
    """

    def __init__(
        self,
        reports_dir: Path = REPORTS_DIR,
        figures_dir: Path = FIGURES_DIR,
        tables_dir: Path = TABLES_DIR,
        report_file: Path = REPORT_FILE,
    ):
        """
        Initialize report input and output paths.
        """
        self.reports_dir = reports_dir
        self.figures_dir = figures_dir
        self.tables_dir = tables_dir
        self.report_file = report_file

    def read_regression_summary(self) -> str:
        """
        Read the regression summary if it exists.

        Returns:
            Regression summary text or an empty string.
        """
        summary_path = self.tables_dir / "regression_summary.txt"

        if summary_path.exists():
            return summary_path.read_text()

        return "Regression summary was not found."

    def collect_figures(self) -> list[Path]:
        """
        Collect generated figure files.

        Returns:
            A sorted list of PNG figure paths.
        """
        return sorted(self.figures_dir.glob("*.png"))

    def build_report_lines(self) -> list[str]:
        """
        Build the Markdown report content.

        Returns:
            A list of lines that form the Markdown report.
        """
        regression_summary = self.read_regression_summary()
        figures = self.collect_figures()

        report_lines = [
            "# CO2 Global Emissions Analysis Report",
            "",
            "## Project Goal",
            "",
            "This project reproduces an R-based CO2 emissions analysis in Python.",
            "It uses the Our World in Data CO2 dataset and generates visualizations and a regression analysis.",
            "",
            "## Dataset",
            "",
            "The project uses the Our World in Data CO2 dataset, which includes CO2 emissions, GDP, population, and country-level indicators.",
            "",
            "## Generated Figures",
            "",
        ]

        for fig in figures:
            report_lines.append(f"![{fig.stem}](../outputs/figures/{fig.name})")
            report_lines.append("")

        report_lines.extend(
            [
                "## Regression Analysis",
                "",
                "The regression model estimates the relationship between GDP per capita and CO2 emissions per capita.",
                "",
                "```text",
                regression_summary,
                "```",
                "",
                "## Conclusion",
                "",
                (
                    "The generated figures and regression results indicate "
                    "that CO2 emissions per capita are associated with economic "
                    "development, although the relationship varies across "
                    "countries and over time."
                ),
            ]
        )

        return report_lines

    def save_report(self) -> None:
        """
        Save the generated Markdown report to disk.
        """
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        report_lines = self.build_report_lines()
        self.report_file.write_text("\n".join(report_lines))

        print(f"Generated report saved to {self.report_file}")

    def run(self) -> None:
        """
        Execute the report generation workflow.
        """
        self.save_report()


def main() -> None:
    """
    Run the report generator.
    """
    generator = ReportGenerator()
    generator.run()


if __name__ == "__main__":
    main()