#!/bin/bash
# Quick demo server launcher

echo "🦑 Kraken D0010 Demo Server"
echo "=========================="
echo ""

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate --no-input

# Check for superuser
echo ""
echo "Checking for admin user..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='demo_admin').exists():
    User.objects.create_superuser('demo_admin', 'admin@kraken.energy', 'KrakenDemo123!')
    print('✓ Created demo_admin user')
else:
    print('✓ demo_admin already exists')
"

# Start server
echo ""
echo "Starting demo server on http://127.0.0.1:8001/"
echo ""
echo "Admin Login:"
echo "  Username: demo_admin"
echo "  Password: KrakenDemo123!"
echo ""
echo "URLs:"
echo "  Home:     http://127.0.0.1:8001/"
echo "  Admin:    http://127.0.0.1:8001/admin/"
echo "  Testing:  http://127.0.0.1:8001/admin/testing/"
echo ""
echo "Press Ctrl+C to stop server"
echo ""

python manage.py runserver 8001
