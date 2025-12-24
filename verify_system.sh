#!/bin/bash
# System verification script with actual health checks

echo "Kraken D0010 System Verification"
echo "===================================="
echo ""

# Check Python
echo "[CHECK] Python installation..."
if command -v python3 &> /dev/null; then
    echo "[OK] Python version: $(python3 --version)"
else
    echo "[ERROR] Python3 not found"
    exit 1
fi

# Check Django
echo ""
echo "[CHECK] Django configuration..."
if python manage.py check --deploy &> /dev/null; then
    echo "[OK] Django configuration valid"
else
    echo "[WARNING] Django configuration has issues:"
    python manage.py check --deploy 2>&1 | head -5
fi

# Check database
echo ""
echo "[CHECK] Database migrations..."
PENDING=$(python manage.py showmigrations meter_readings 2>&1 | grep -c "\[ \]")
if [ "$PENDING" -eq 0 ]; then
    echo "[OK] All migrations applied"
else
    echo "[WARNING] $PENDING pending migrations"
fi

# Check if server is running
echo ""
echo "[CHECK] Server connectivity..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/ | grep -q "200\|302"; then
    SERVER_RUNNING=true
    echo "[OK] Server responding on port 8001"
else
    SERVER_RUNNING=false
    echo "[WARNING] Server not responding on port 8001"
    echo "         Start with: python manage.py runserver 8001"
fi

# Only check endpoints if server is running
if [ "$SERVER_RUNNING" = true ]; then
    echo ""
    echo "[CHECK] API endpoints..."
    
    # Check API root
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/api/flow-files/ | grep -q "200"; then
        echo "[OK] /api/flow-files/ responding"
    else
        echo "[ERROR] /api/flow-files/ not responding"
    fi
    
    # Check admin
    echo ""
    echo "[CHECK] Admin interface..."
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/admin/ | grep -q "200\|302"; then
        echo "[OK] /admin/ responding"
    else
        echo "[ERROR] /admin/ not responding"
    fi
    
    # Check dashboard
    echo ""
    echo "[CHECK] Dashboard..."
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/ | grep -q "200"; then
        echo "[OK] Dashboard responding"
    else
        echo "[ERROR] Dashboard not responding"
    fi
fi

echo ""
echo "===================================="
echo "[COMPLETE] System verification finished"
echo ""

if [ "$SERVER_RUNNING" = false ]; then
    echo "Quick Start:"
    echo "  1. python manage.py migrate"
    echo "  2. python manage.py createsuperuser"
    echo "  3. python manage.py runserver 8001"
    echo "  4. ./verify_system.sh"
fi
