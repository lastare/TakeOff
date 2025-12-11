.PHONY: install test lint format clean run help

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .
	mypy .

format:
	ruff format .

clean:
	rm -rf build dist .egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

run:
	python -m takeoff.main

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies (including dev tools)"
	@echo "  make test     - Run tests with coverage"
	@echo "  make lint     - Run static analysis (Ruff, Mypy)"
	@echo "  make format   - Format code using Ruff"
	@echo "  make clean    - Cleanup build artifacts"
	@echo "  make run      - Run the application"
