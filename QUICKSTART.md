# Kraken D0010 - Quick Start Guide

Get up and running in 2 minutes.

## Prerequisites

- Python 3.13+
- pip

## Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run database migrations
python manage.py migrate

# 3. Create admin user
python manage.py createsuperuser
# Username: demo_admin
# Password: KrakenDemo123!

# 4. Start server
python manage.py runserver 8001
```

## Access

- **Home:** http://127.0.0.1:8001/
- **Admin:** http://127.0.0.1:8001/admin/
- **Testing Dashboard:** http://127.0.0.1:8001/admin/testing/

## Quick Test

### Via Testing Dashboard (Recommended)

1. Login to admin (demo_admin / KrakenDemo123!)
2. Click "🧪 Testing & Debug" in sidebar
3. Click "Import All Sample Files"
4. View imported data in admin

### Via Command Line

```bash
# Import a single file
python manage.py import_d0010 sample_data/commercial_properties.uff

# Dry-run (validation only)
python manage.py import_d0010 sample_data/test_file.uff --dry-run
```

## What's Next?

- See [documentation/FUNCTIONAL_SPEC.md](documentation/FUNCTIONAL_SPEC.md) for complete feature documentation
- See [documentation/TESTING_GUIDE.md](documentation/TESTING_GUIDE.md) for testing dashboard details
- See [README.md](README.md) for architecture overview

---

**Ready to process D0010 files!** 🚀
