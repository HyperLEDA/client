PYTHON := python

environment:
	$(PYTHON) -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	source .venv/bin/activate

install:
	$(PYTHON) -m pip install -r requirements.txt

build:
	$(PYTHON) -m build .