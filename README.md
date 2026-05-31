# CO2 Global Emissions Analysis in Python

This project is a Python reproduction of the original R-based CO2 Global Emissions Analysis project.

The project downloads the Our World in Data CO2 dataset, cleans and prepares the data, generates visualizations, performs a regression analysis, and produces a final report.

The entire workflow is reproducible and can be executed either locally or inside a Docker container.

---

## Dataset

Source:

- Our World in Data CO2 Dataset
- https://github.com/owid/co2-data

The dataset contains information about:

- CO2 emissions
- CO2 emissions per capita
- GDP
- Population
- Cumulative CO2 emissions
- Share of global CO2 emissions

---

## Project Structure

```text
co2-emissions-python-RR-Project/
├── src/
│   ├── __init__.py
│   ├── download_data.py
│   ├── clean_data.py
│   ├── plots.py
│   ├── analysis.py
│   └── generate_report.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── reports/
│   ├── generated_report.md
│   ├── project_report.qmd
│   ├── project_report.html
│   └── figures/
│
├── requirements.txt
├── Makefile
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Local Installation

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

---

## Running the Complete Workflow

Execute the entire project:

```bash
make all
```

This command automatically:

1. Downloads the dataset
2. Cleans the data
3. Generates visualizations
4. Runs the regression analysis
5. Produces the final report

---

## Running Step by Step

### Download Dataset

```bash
python src/download_data.py
```

### Clean Data

```bash
python src/clean_data.py
```

### Generate Visualizations

```bash
python src/plots.py
```

### Run Regression Analysis

```bash
python src/analysis.py
```

### Generate Markdown Report

```bash
python src/generate_report.py
```

---

## Generated Outputs

### Figures

Generated figures are saved in:

```text
outputs/figures/
```

The project generates:

1. Global Average CO2 per Capita Over Time
2. GDP per Capita vs CO2 per Capita
3. Linear Regression Plot
4. Top 10 Countries by CO2 per Capita
5. CO2 per Capita Over Time for Top 5 Countries
6. CO2 per Capita by GDP Quartile Boxplot
7. CO2 per Capita by GDP Quartile Violin Plot
8. Heatmap of Average CO2 per Capita by Year and GDP Quartile
9. Cumulative Sum of CO2 per Capita
10. Year-over-Year Change in Global Average CO2 per Capita
11. CO2 per Capita vs Total CO2 Emissions

### Regression Results

Regression outputs are saved in:

```text
outputs/tables/
```

Files:

```text
regression_summary.txt
regression_coefficients.csv
```

---

## Regression Model

The project estimates the following model:

```text
CO2 per capita ~ GDP per capita
```

The regression is performed using the Statsmodels library.

The resulting model achieved:

```text
R² ≈ 0.556
```

indicating a moderate positive relationship between GDP per capita and CO2 emissions per capita.

---

## Quarto Report

The project includes a Quarto report summarizing the complete analysis.

Generate the report:

```bash
quarto render reports/project_report.qmd --to html
```

The generated report is saved as:

```text
reports/project_report.html
```

The report contains:

- Project overview
- Dataset description
- Workflow explanation
- Generated visualizations
- Regression analysis summary
- Final conclusions

---

## Docker Reproducibility

Build and run the complete workflow inside Docker:

```bash
docker compose up --build
```

This command automatically:

1. Downloads the dataset
2. Cleans the data
3. Generates all visualizations
4. Runs the regression analysis
5. Produces the final report

The project was designed to be fully reproducible inside a Docker container.

---

## Notebook

A Jupyter notebook is included for exploratory analysis:

```text
notebooks/01_data_exploration.ipynb
```

The notebook demonstrates dataset loading and inspection.

The main project workflow is implemented in Python scripts rather than notebooks.

---

## Team Members

- Said Mahmud
- Sabir Mammadov
- Nural Mammadov
- Aykhan Safarli

---

## Reproducibility Summary

This repository contains:

- Python scripts
- Jupyter notebook
- Quarto report
- Makefile workflow
- Docker configuration
- Regression analysis
- Visualizations
- Documentation

allowing the entire project to be reproduced on any machine with Python or Docker installed.