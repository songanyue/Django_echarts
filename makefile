run:
	python manage.py runserver

generate:
	python manage.py makemigrations && python manage.py migrate

superuser:
	python manage.py createsuperuser