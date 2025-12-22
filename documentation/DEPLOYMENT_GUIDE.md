# Kraken D0010 - Deployment Guide

Django Admin Dashboard for processing D0010 meter reading files with full CRUD operations, file import, and comprehensive testing.

## Quick Start

```bash
tar -xzf kraken_d0010_project.tar.gz
cd kraken_d0010_project
./run_demo_server.sh
```

The demo server will be running at http://127.0.0.1:8001

**Login:** demo_admin / KrakenDemo123!

## Manual Setup (Alternative)

If you prefer step-by-step control:

### **Step 1: Extract**
```bash
tar -xzf kraken_d0010_project.tar.gz
cd kraken_d0010_project
```

### **Step 2: Setup Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Step 3: Database & Server**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8001
```

Visit http://127.0.0.1:8001/admin/ to access the system.

## System Dependencies (Optional)

If you need to install Python 3.8+ or PostgreSQL:

```bash
./deployment_scripts/setup_system_dependencies.sh
```

This script installs:
- Python 3.13 (via Homebrew on macOS or apt on Ubuntu)
- PostgreSQL 16 (optional, prompted during install)

## What's Included

**Sample Data:**
- 78+ meter readings across multiple scenarios
- 51 unique MPANs (residential, commercial, industrial)
- 13 sample D0010 files

**Features:**
- SQLite database (default) with PostgreSQL support
- Full admin interface with search and filtering
- REST API endpoints
- Comprehensive test coverage
- Sample data for testing

## Access & Testing

**Admin Interface:** http://127.0.0.1:8001/admin/
- Username: `demo_admin`
- Password: `KrakenDemo123!`

**Test Searches:**
- MPAN: `1200023305967` (original sample)
- MPAN: `1400056789012` (smart meter)
- Serial: `F75A 00802`
- Serial: `SM1A 12345`

## Troubleshooting

**Permission Issues:**
```bash
chmod +x run_demo_server.sh
```

**Python Version:**
```bash
python3 --version  # Should be 3.8+
```

**Manual Database Check:**
```bash
source venv/bin/activate
python manage.py shell -c "from meter_readings.models import Reading; print(Reading.objects.count())"
```

---

**Questions?** Check [README.md](../kraken_d0010_project/README.md) for feature details.