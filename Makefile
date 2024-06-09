install:
	poetry install

build:
	./build.sh

migrate:
	poetry run python3 manage.py migrate

dev:
	poetry run python3 manage.py runserver 8000

start:
	poetry run python3 -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

lint:
	poetry run flake8 page_analyzer

test:
	poetry run python3 manage.py test
