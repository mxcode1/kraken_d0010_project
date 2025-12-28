# Kraken D0010 - Quick Start Guide

Get up and running in 2 minutes.

## Prerequisites

- Python 3.13+
- pip

## Installation

```bash
# 0. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

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

## Quickest Demo: One Command

You can use the provided script to set up and launch everything automatically:

```bash
./run_demo_server.sh
```
This will:
- Create a virtual environment (if needed)
- Install dependencies
- Run migrations
- Create the demo admin user (if needed)
- Start the server on http://127.0.0.1:8001/

See the script for details.

## Access

- **Home:** http://127.0.0.1:8001/
- **Admin:** http://127.0.0.1:8001/admin/
- **Testing Dashboard:** http://127.0.0.1:8001/admin/testing/

**Note:** Port 8001 is used to avoid conflicts with other development servers.

## Quick Test

### Via Testing Dashboard (Recommended)

1. Login to admin (demo_admin / KrakenDemo123!)
2. Navigate to http://127.0.0.1:8001/admin/testing/ or click through to testing dashboard
3. Click "Import All Sample Files"
4. Verify statistics (should show 18+ readings)
5. Ready for demo and to work with Admin interface!

### Via Command Line

```bash
# Import a single file
python manage.py import_d0010 sample_data/commercial_properties.uff

# Dry-run (validation only)
python manage.py import_d0010 sample_data/test_file.uff --dry-run
```

## What's Next?

- See [FUNCTIONAL_SPEC.md](FUNCTIONAL_SPEC.md) for complete feature documentation
- See [TESTING_GUIDE.md](TESTING_GUIDE.md) for testing dashboard details
- See [README.md](README.md) for architecture overview

---

## First Login

**Open in Chrome for HTTP:** http://127.0.0.1:8001/admin/

```
Username: demo_admin
Password: KrakenDemo123!
```
- Unless alternate logins are specified in .env
---

## Testing Dashboard

**Access:** http://127.0.0.1:8001/admin/testing/

### What You Can Do:

1. **📊 View Statistics**
   - Current database counts (FlowFiles, MeterPoints, Meters, Readings)
   
2. **📄 Import Sample Data**
   - Individual file import (click "Import" next to any .uff file)
   - Batch import (click "Import All Unimported Files")
   
3. **🧹 Clear Database**
   - Remove all data to reset for testing
   
4. **📋 Track Imports**
   - See which files are imported (✅) vs available (⬜)
   - View recently imported files

### Quick Test Workflow:

```bash
# Fresh start
1. Open Testing Dashboard
2. Click "Clear All Data" (confirms database is empty)
3. Click "Import All Unimported Files" (loads 13 sample files)
4. Verify statistics show: 3 FlowFiles, 18 MeterPoints, 18 Meters, 26 Readings
5. Browse to "Meter Readings > Readings" to see imported data
```

---

## Core Functionality Check

### ✅ Data Import
- [ ] Import single .uff file → Success message shown
- [ ] View imported data in admin interface
- [ ] Verify data relationships (MeterPoint → Meter → Reading)

### ✅ Search & Filter
- [ ] Search by MPAN: `1200023305967`
- [ ] Search by Serial: `F75A 00802`
- [ ] Filter by Flow File

### ✅ Database Management
- [ ] Clear all data → Database empty
- [ ] Re-import → Data restored

---

## System Files

```
kraken_d0010_project/
├── manage.py              # Django management
├── run_demo_server.sh     # Quick server launcher
├── db.sqlite3             # Database (auto-created)
├── sample_data/           # 12 .uff test files
├── venv/                  # Python environment
└── meter_readings/        # Core application
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "This site can't be reached" | Use Chrome Incognito mode |
| SSL_PROTOCOL_ERROR | Server is HTTP-only, use `http://` not `https://` |
| Pages won't load | Clear browser HSTS at `chrome://net-internals/#hsts` |
| Server not starting | Check venv is activated: `which python` |

---

## Next Steps

- **Import Data:** Use Testing Dashboard or Admin UI / CLI Service to load sample files
- **Browse Data:** Explore admin interface at `/admin/meter_readings/`

---

## URLs Reference

| Feature | URL |
|---------|-----|
| Admin Home | http://127.0.0.1:8001/admin/ |
| Testing Dashboard | http://127.0.0.1:8001/admin/testing/ |
| Flow Files | http://127.0.0.1:8001/admin/meter_readings/flowfile/ |
| Meter Points | http://127.0.0.1:8001/admin/meter_readings/meterpoint/ |
| Meters | http://127.0.0.1:8001/admin/meter_readings/meter/ |
| Readings | http://127.0.0.1:8001/admin/meter_readings/reading/ |
| API Docs | http://127.0.0.1:8001/admin/api/docs |
---