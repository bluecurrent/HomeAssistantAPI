install:
	pip install -r requirements.txt

lint:
	pylint src

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
	
build-ha:
	make build
	docker cp dist\bluecurrent_api-1.0.0-py3-none-any.whl $(container):/workspaces/core/
	docker exec $(container) pip install core/bluecurrent_api-1.0.0-py3-none-any.whl --no-deps --force-reinstall
	docker exec $(container) rm core/bluecurrent_api-1.0.0-py3-none-any.whl