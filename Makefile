install:
	poetry install

build:
	./build.sh

migrate:
	poetry run python3 manage.py migrate

makemigrations:
	poetry run python3 manage.py makemigrations

dev:
	poetry run python3 manage.py runserver 8000

start:
	poetry run python3 -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

lint:
	poetry run flake8

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

selfcheck:
	poetry check

check: lint test

.PHONY: install test lint selfcheck check build
