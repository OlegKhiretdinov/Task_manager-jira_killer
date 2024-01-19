dev:
	poetry run python manage.py runserver

start:
	gunicorn task_manager.wsgi

shell:
	poetry run python manage.py shell_plus --ipython

install:
	poetry install

lint:
	poetry run flake8 task_manager

build:
	./build.sh