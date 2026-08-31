PYTHON ?= python3
.DEFAULT_GOAL := help
.PHONY: help install test tests unit-tests coverage examples fixtures dataset clean format lint

help: ## Show this help
	@$(PYTHON) -c "import re; f=open('Makefile').read(); [print('  {:<24s} {}'.format(*m.groups())) for m in re.finditer(r'^([a-z_-]+):.*?## (.+)', f, re.M)]"

install: ## Editable install with dev extras
	$(PYTHON) -m pip install -e ".[dev]"

fixtures: ## Write examples/mug.jpg
	PYTHONPATH=. $(PYTHON) examples/make_mug.py

dataset: ## Offline 4-swatch visual set
	PYTHONPATH=. $(PYTHON) examples/make_swatches.py

test: tests

tests: fixtures ## Pytest with branch coverage
	PYTHONPATH=. $(PYTHON) -m pytest --cov-branch --cov=tinyeye --cov-report=term-missing --cov-report=html tests

unit-tests: tests ## Alias

coverage: tests ## Alias

examples: fixtures dataset ## Write eye pairs without latent
	mkdir -p examples/out
	PYTHONPATH=. $(PYTHON) tinyeye_encode.py examples/mug.jpg --out examples/out --no-latent --belief "A red square standing in for a mug."
	@ls examples/out/*eye.jpg examples/out/*eye.md examples/out/swatches/*eye.md

format:
	-$(PYTHON) -m ruff format tinyeye examples tests tinyeye_sidecar.py tinyeye_encode.py

lint: format
	-$(PYTHON) -m ruff check tinyeye tests

clean:
	rm -rf .pytest_cache .coverage htmlcov examples/out examples/mug.jpg *.egg-info
