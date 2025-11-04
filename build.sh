#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Create logs directory if it doesn't exist
mkdir -p logs

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Run migrations
echo "Running migrations..."
python manage.py migrate
