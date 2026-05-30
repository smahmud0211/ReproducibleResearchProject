# CO2 Reproducible Research Project

## Team Members

* Said Mahmud
* Sabir Mammadov
* Aykhan Safarli
* Nural Mammadov

## Project Objective

This project reproduces selected CO2 emissions analyses from an existing R-based project using Python while following reproducible research principles.

## Original Project

R implementation:

https://github.com/hoangsonww/CO2-Global-Emissions-Analysis

## Dataset

Our World in Data CO2 Dataset:

https://github.com/owid/co2-data

## Project Structure

text
data/raw/
    owid-co2-data.csv

src/co2_analysis/
    data_loader.py
    processor.py
    analyzer.py
    visualizer.py
    main.py

reports/
    final_report.md

docs/

outputs/figures/


## Features

* Data loading pipeline
* Data preprocessing
* Global CO2 emissions analysis
* Top CO2 emitters analysis
* Visualization generation
* Reproducible execution pipeline
* Git-based collaborative workflow

## Installation

bash
pip install -r requirements.txt


## Running the Project

bash
make run


## Generated Output

The pipeline generates:

text
outputs/figures/global_co2_emissions.png


## Reproducibility

The project includes:

* Git version control
* Branch and pull-request workflow
* Python package structure
* Makefile automation
* Docker configuration
* Reproducible analysis pipeline

## Course Information

This project was developed as part of the Reproducible Research course and demonstrates collaborative software development and reproducible data analysis practices.