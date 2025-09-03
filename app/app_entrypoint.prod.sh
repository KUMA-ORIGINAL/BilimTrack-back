#!/bin/sh

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn config.wsgi --workers 2 --bind 0.0.0.0:8000 --timeout 60 --log-level info
