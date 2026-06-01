"""
Generate the final project report.

This module creates a Markdown report containing:
- Project overview
- Generated visualizations
- Regression analysis results
- Final conclusions

The report is automatically generated after the analysis workflow
and serves as the basis for the project presentation.
"""

from pathlib import Path

REPORTS_DIR = Path("reports")
FIGURES_DIR = Path("outputs/figures")
TABLES_DIR = Path("outputs/tables")
REPORT_FILE = REPORTS_DIR / "generated_report.md"


def main() -> None:
    """
    Generate a Markdown report summarizing the project results.

    The report includes:
    - Project objective
    - All generated figures
    - Regression analysis summary
    - Final conclusions

    Output:
        reports/generated_report.md
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    regression_summary_path = TABLES_DIR / "regression_summary.txt"

    regression_summary = ""
    if regression_summary_path.exists():
        regression_summary = regression_summary_path.read_text()

    figures = sorted(FIGURES_DIR.glob("*.png"))

    report_lines = [
        "# CO2 Global Emissions Analysis Report",
        "",
        "## Project Goal",
        "",
        "This project reproduces an R-based CO2 emissions analysis in Python.",
        "It uses the Our World in Data CO2 dataset and generates visualizations and a regression analysis.",
        "",
        "## Generated Figures",
        "",
    ]

    for fig in figures:
        report_lines.append(
            f"![{fig.stem}](../outputs/figures/{fig.name})"
        )
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

    REPORT_FILE.write_text("\n".join(report_lines))

    print(f"Generated report saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()