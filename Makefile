.PHONY: help install test test-verbose test-coverage clean docker-build docker-run lint format

help:
	@echo "Available targets:"
	@echo "  make install          - Install dependencies"
	@echo "  make test             - Run tests locally"
	@echo "  make test-verbose     - Run tests with verbose output"
	@echo "  make test-coverage    - Run tests with coverage report"
	@echo "  make lint             - Run linting checks"
	@echo "  make format           - Format code with black"
	@echo "  make clean            - Clean up build artifacts and cache"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-run       - Run Docker container"

install:
	pip install -r requirements.txt
	pip install -r Capabilities/requirements.txt
	pip install -r test-requirements.txt

test: install
	cd testing && python -m pytest utest_translation.py -v

test-verbose: install
	cd testing && python -m pytest utest_translation.py -vv --tb=long

test-coverage: install
	cd testing && python -m pytest utest_translation.py --cov --cov-report=term-pretty

lint:
	pylint testing/utest_translation.py Capabilities/chalicelib/

format:
	black testing/ Capabilities/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete || true
	find . -type d -name .pytest_cache -exec rm -rf {} + || true
	find . -type d -name .coverage -exec rm -rf {} + || true
	rm -rf .pytest_cache/ || true
	rm -rf htmlcov/ || true

docker-build:
	docker build -t anmol-assignment1:latest .

docker-run:
	docker run -it --rm \
		-e AWS_PROFILE=default \
		-v ~/.aws:/root/.aws \
		-p 8000:8000 \
		anmol-assignment1:latest
