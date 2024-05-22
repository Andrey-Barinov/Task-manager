install:
	poetry install

build:
	./build.sh

migrate:
	poetry run python3 migrate

dev:
	poetry run python3 manage.py runserver

start:
	poetry run python3 -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

lint:
	poetry run flake8 page_analyzer
