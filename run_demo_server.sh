#!/bin/bash
# run_demo_server.sh
# One-command deployment for Kraken D0010

set -e

echo "🦑 Kraken D0010 - Quick Demo Server"
echo "===================================="
echo ""

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Run migrations
echo "Setting up database..."
python manage.py migrate --no-input

# Create demo admin if doesn't exist
echo "Creating demo admin user..."
python manage.py shell << PYEOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='demo_admin').exists():
    User.objects.create_superuser('demo_admin', 'demo@kraken.test', 'KrakenDemo123!')
    print("Demo admin created: demo_admin / KrakenDemo123!")
else:
    print("Demo admin already exists")
PYEOF

# Start server
echo ""
echo "✅ Starting development server..."
echo "   http://127.0.0.1:8001/admin/"
echo "   Username: demo_admin"
echo "   Password: KrakenDemo123!"
echo ""
python manage.py runserver 8001
