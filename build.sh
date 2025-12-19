#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python config/manage.py migrate --noinput

echo "Collecting static files..."
python config/manage.py collectstatic --noinput
