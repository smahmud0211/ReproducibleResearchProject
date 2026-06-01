.PHONY: install download clean plots analysis report quarto all

install:
	pip install -r requirements.txt

download:
	python src/download_data.py

clean:
	python src/clean_data.py

plots:
	python src/plots.py

analysis:
	python src/analysis.py

report:
	python src/generate_report.py
	mkdir -p reports/figures
	cp outputs/figures/*.png reports/figures/

quarto:
	quarto render reports/project_report.qmd --to html

all: download clean plots analysis report quarto