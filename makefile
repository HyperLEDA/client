PYTHON := python

environment:
	$(PYTHON) -m venv .venv
	$(PYTHON) -m pip install --upgrade pip

install:
	$(PYTHON) -m pip install -r requirements.txt

build:
	$(PYTHON) -m build .

check: check-format check-lint

check-format:
	$(PYTHON) -m ruff format --config=pyproject.toml --check

check-lint:
	$(PYTHON) -m ruff check --config=pyproject.toml

fix: fix-format fix-lint

fix-format:
	$(PYTHON) -m ruff format --config=pyproject.toml

fix-lint:
	$(PYTHON) -m ruff check --config=pyproject.toml --fix --unsafe-fixes

# TODO: add target to autogenerate models for client
