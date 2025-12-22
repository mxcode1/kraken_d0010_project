#!/bin/bash
# Quick demo server launcher with automatic setup

set -e

echo "[START] Kraken D0010 Demo Server Setup"
echo ""

# ============================================
# AUTO-CREATE .env WITH DEMO CREDENTIALS
# ============================================
if [ ! -f .env ]; then
    echo "[SETUP] Creating .env from template..."
    cp .env.example .env
    
    # Populate demo credentials programmatically
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' 's/DEMO_ADMIN_USERNAME=$/DEMO_ADMIN_USERNAME=demo_admin/' .env
        sed -i '' 's/DEMO_ADMIN_PASSWORD=$/DEMO_ADMIN_PASSWORD=KrakenDemo123!/' .env
    else
        # Linux
        sed -i 's/DEMO_ADMIN_USERNAME=$/DEMO_ADMIN_USERNAME=demo_admin/' .env
        sed -i 's/DEMO_ADMIN_PASSWORD=$/DEMO_ADMIN_PASSWORD=KrakenDemo123!/' .env
    fi
    
    echo "[OK] .env created with demo credentials"
    echo "     Username: demo_admin"
    echo "     Password: KrakenDemo123!"
else
    echo "[OK] Using existing .env configuration"
fi

echo ""

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

# ============================================
# VIRTUAL ENVIRONMENT
# ============================================
if [ ! -d "venv" ]; then
    echo "[CREATE] Virtual environment..."
    python3 -m venv venv
    echo "[OK] Virtual environment created"
fi

echo "[INSTALL] Activating environment and installing dependencies..."
source venv/bin/activate
pip install -q -r requirements.txt
echo "[OK] Dependencies installed"
echo ""

# ============================================
# DATABASE SETUP
# ============================================
echo "[SETUP] Database migrations..."
python manage.py migrate --noinput
echo "[OK] Database ready"
echo ""

# ============================================
# DEMO ADMIN USER
# ============================================
USERNAME=${DEMO_ADMIN_USERNAME:-demo_admin}
PASSWORD=${DEMO_ADMIN_PASSWORD:-KrakenDemo123!}

python manage.py shell << PYEOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$USERNAME').exists():
    User.objects.create_superuser('$USERNAME', 'admin@example.com', '$PASSWORD')
    print("[OK] Demo admin created: $USERNAME")
else:
    print("[OK] Demo admin exists: $USERNAME")
PYEOF

echo ""

# ============================================
# START SERVER
# ============================================
PORT=${SERVER_PORT:-8001}

echo "[COMPLETE] Setup finished!"
echo ""
echo "Starting server on http://127.0.0.1:$PORT"
echo "Login: $USERNAME / $PASSWORD"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python manage.py runserver $PORT
