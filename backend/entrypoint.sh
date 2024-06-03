#!/bin/sh

# Wait for Postgres to start
echo "Waiting for postgres..."
while ! nc -z database 5432; do
	sleep 0.1
done
echo "PostgreSQL started"

# Migration
echo "Making migrations..."
python manage.py makemigrations --noinput # --noinput is used to avoid the prompt
# python manage.py migrate chat zero
echo "Migrating..."
python manage.py migrate
echo "Migrations done"

# collect static files
# python manage.py collectstatic

# Websockets servers
echo "Starting game websocket server in the background..."
./websockets/pong_server/launch_pong_server.sh &
export DJANGO_SETTINGS_MODULE=core.settings

# Start server
python manage.py runserver 0.0.0.0:8000
#daphne -b 0.0.0.0 -p 8001 core.asgi:application