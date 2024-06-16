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
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py,*/migrations/*,*/tests/*,tests.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py,*/migrations/*,*/tests/*,tests.py

selfcheck:
	poetry check

check: lint test

.PHONY: install test lint selfcheck check build
