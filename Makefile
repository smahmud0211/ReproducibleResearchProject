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
	mkdir -p reports
	@if [ -f project_report.html ]; then mv -f project_report.html reports/project_report.html; fi
	@if [ -d project_report_files ]; then rm -rf reports/project_report_files && mv project_report_files reports/project_report_files; fi

all: download clean plots analysis report quarto