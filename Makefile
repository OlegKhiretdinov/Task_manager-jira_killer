PORT ?= 8000

dev:
	poetry run python manage.py runserver

start:
	poetry run python -m gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

shell:
	poetry run python manage.py shell_plus --ipython

install:
	poetry install

lint:
	poetry run flake8 task_manager

build:
	./build.sh

test:
	poetry run coverage run manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report xml
