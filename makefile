PYTHON := python

environment:
	$(PYTHON) -m venv .venv
	$(PYTHON) -m pip install --upgrade pip

install:
	$(PYTHON) -m pip install -r requirements.txt

build:
	$(PYTHON) -m build .

# to use the model one needs to start the server on localhost:8000
generate-model:
	mkdir -p hyperleda/gen
	curl localhost:8000/api/docs/swagger.json > hyperleda/gen/swagger.json
	datamodel-codegen --input hyperleda/gen/swagger.json --output hyperleda/model.py --output-model-type dataclasses.dataclass --input-file-type openapi
	make fix

# Testing

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
