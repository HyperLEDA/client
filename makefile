PYTHON := python

environment:
	$(PYTHON) -m venv .venv
	$(PYTHON) -m pip install --upgrade pip

install:
	$(PYTHON) -m pip install -r requirements.txt

build:
	$(PYTHON) -m build .

# to use the model the server needs to be started on localhost:8080
generate-admin-model:
	mkdir -p hyperleda/gen
	curl http://localhost:8080/admin/api/openapi.json > hyperleda/gen/swagger.json
	datamodel-codegen --input hyperleda/gen/swagger.json --output hyperleda/model.py --input-file-type openapi
	make fix

generate-data-model:
	mkdir -p hyperleda/data/gen
	curl http://localhost:8080/api/openapi.json > hyperleda/data/gen/swagger.json
	datamodel-codegen --input hyperleda/data/gen/swagger.json --output hyperleda/data/model.py --output-model-type dataclasses.dataclass --input-file-type openapi
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
