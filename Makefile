PYTHON ?= python3
.DEFAULT_GOAL := help
.PHONY: help install test tests examples fixtures clean

help:
	@$(PYTHON) -c "import re; f=open('Makefile').read(); [print('  {:<24s} {}'.format(*m.groups())) for m in re.finditer(r'^([a-z_-]+):.*?## (.+)', f, re.M)]"

install:
	$(PYTHON) -m pip install -e ".[dev]"

fixtures:
	$(PYTHON) examples/make_mug.py

test: tests

tests: fixtures
	$(PYTHON) -m pytest --cov-branch --cov=tinyeye_sidecar --cov-report=term-missing tests

examples: fixtures
	mkdir -p examples/out
	$(PYTHON) tinyeye_encode.py examples/mug.jpg --out examples/out --no-latent --belief "A red square standing in for a mug."

clean:
	rm -rf .pytest_cache .coverage htmlcov examples/out examples/mug.jpg *.egg-info
