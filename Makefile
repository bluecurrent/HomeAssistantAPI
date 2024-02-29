install:
	pip install -r requirements.txt

install-docs:
	pip install -r docs/requirements.txt

lint:
	pylint src

mypy:
	mypy src

black:
	black src tests

ruff:
	ruff --fix src tests && ruff format src tests

test:
	python -m pytest

test-cov:
	python -m pytest --cov=src --cov-report term-missing

build:
	python -m build

publish:
	twine upload dist/*

html:
	cd docs && make.bat clean && make.bat html