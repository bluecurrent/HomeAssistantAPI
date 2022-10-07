install:
	pip install -r requirements.txt

lint:
	pylint src

test:
	python -m pytest

test-cov:
	python -m pytest -cov=src --cov-report term-missing

build:
	python -m build

publish:
	twine upload dist/*