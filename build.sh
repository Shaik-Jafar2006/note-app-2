#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status.
set -o errexit  

echo "🔧 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build complete!"
