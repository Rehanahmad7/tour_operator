#!/bin/sh
set -e

# Optional: simple wait for DB host (if using external DB)
if [ -n "$DATABASE_HOST" ]; then
  echo "Waiting for DB at $DATABASE_HOST..."
  for i in 1 2 3 4 5; do
    nc -z "$DATABASE_HOST" ${DATABASE_PORT:-5432} && break
    sleep 1
  done
fi

echo "Running migrations..."
python manage.py migrate --noinput || true

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Starting Gunicorn..."
exec gunicorn tour_operator.wsgi:application --bind 0.0.0.0:8000 --workers 3
