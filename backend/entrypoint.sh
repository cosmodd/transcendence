#!/bin/sh

# Wait for Postgres to start
echo "Waiting for postgres..."
while ! nc -z database 5432; do
	sleep 0.1
done
echo "PostgreSQL started"

# Migration
echo "Making migrations..."
python manage.py makemigrations
echo "Migrating..."
python manage.py migrate
echo "Migrations done"

# Websockets servers
echo "Starting pong websocket server in the background..."
./scripts/pong/launch_server.sh &

# Start server
python manage.py runserver 0.0.0.0:8000