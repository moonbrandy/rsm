#!/bin/bash
python manage_rsm.py collectstatic --noinput
python manage_rsm.py syncdb --noinput
python manage_rsm.py makemigrations
python manage_rsm.py migrate --noinput
# python /code/manage_rsm.py runserver 0.0.0.0:8000

# Start Gunicorn processes
echo Starting Gunicorn
exec gunicorn inst_rsm.wsgi:application \
	--bind 127.0.0.1:8000 \
	--workers 3
