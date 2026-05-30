# Project Documentation

## Project Structure

data/raw/
- OWID CO2 dataset

src/co2_analysis/
- data_loader.py
- processor.py
- analyzer.py
- visualizer.py
- main.py

reports/
- final_report.md

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt

Run the pipeline:

make run

## Output

The pipeline generates:

- global_co2_emissions.png

inside outputs/figures/