.PHONY: install run

install:
	pip install -r requirements.txt

run:
	PYTHONPATH=src python3 src/co2_analysis/main.py