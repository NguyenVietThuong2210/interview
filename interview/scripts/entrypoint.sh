#!/bin/bash

# Exit on error
set -e

echo "Waiting for PostgreSQL..."
sleep 2
echo "PostgreSQL started"

# Run migrations
echo "Running database migrations..."
# python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec "$@"