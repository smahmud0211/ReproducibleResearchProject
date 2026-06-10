# CO2 Global Emissions Analysis in Python

This project is a Python reproduction of the original R-based CO2 Global Emissions Analysis project.

The project downloads the Our World in Data CO2 dataset, cleans and prepares the data, generates visualizations, performs a regression analysis, and produces a final Quarto HTML report.

The workflow can be reproduced either locally or inside a Docker container.

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

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Quarto is also required to render the final HTML report locally.

---

## Running the Complete Workflow Locally

Run the full project workflow:

```bash
make all
```

This command automatically:

1. Downloads the dataset
2. Cleans and prepares the data
3. Generates visualizations
4. Runs the regression analysis
5. Generates the report content
6. Renders the final Quarto HTML report

The final report is saved at:

```text
reports/project_report.html
```

---

## Running Step by Step

Download the dataset:

```bash
python src/download_data.py
```

Clean the data:

```bash
python src/clean_data.py
```

Generate visualizations:

```bash
python src/plots.py
```

Run the regression analysis:

```bash
python src/analysis.py
```

Generate the Markdown report:

```bash
python src/generate_report.py
```

Render the Quarto HTML report:

```bash
quarto render reports/project_report.qmd --to html
```

---

## Running with Docker

Docker can reproduce the complete workflow without installing the Python packages or Quarto directly on the local machine.

First, build the Docker image from the project folder:

```bash
docker build -t co2-emissions-python-rr .
```

Then run the complete workflow inside Docker:

```bash
docker run --rm -v "$(pwd)":/app -w /app co2-emissions-python-rr make all
```

This command runs the full project workflow:

1. Downloads the dataset
2. Cleans and prepares the data
3. Generates figures
4. Runs the regression analysis
5. Generates the report
6. Renders the final HTML file

The generated files are saved in the project folder:

```text
reports/project_report.html
outputs/figures/
outputs/tables/
```

The `--rm` option removes the temporary Docker container after the workflow finishes.

The `-v "$(pwd)":/app` option connects the current project folder to the Docker container, so the generated outputs are saved back to the local project folder.

The `-w /app` option sets the working directory inside the Docker container.

---

## Running with Docker Compose

The project can also be run with Docker Compose:

```bash
docker compose up --build
```

This builds the Docker image and runs the full workflow using the configuration in `docker-compose.yml`.

---

## Generated Outputs

Generated figures are saved in:

```text
outputs/figures/
```

The project generates visualizations including:

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

Regression outputs are saved in:

```text
outputs/tables/
```

Files:

```text
regression_summary.txt
regression_coefficients.csv
```

The final Quarto report is saved as:

```text
reports/project_report.html
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

This indicates a moderate positive relationship between GDP per capita and CO2 emissions per capita.

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

Together, these files allow the full project to be reproduced on any machine with either local Python and Quarto installation or Docker.