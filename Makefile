dev:
	poetry run python manage.py runserver

shell:
	poetry run python manage.py shell_plus --ipython

install:
		poetry install