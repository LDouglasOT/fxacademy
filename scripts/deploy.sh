#!/bin/bash

# Deployment script for fxAcademy Django app

echo "Starting deployment..."

# Activate virtual environment (adjust path as needed)
# source /path/to/your/venv/bin/activate

# Install dependencies
pip install -r req.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart gunicorn (adjust service name)
sudo systemctl restart gunicorn

# Restart nginx
sudo systemctl restart nginx

echo "Deployment completed!"