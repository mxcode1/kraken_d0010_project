# Deployment Scripts

Professional deployment automation tools for Kraken D0010.

## Quick Start (Recommended)

For immediate deployment:

```bash
./run_demo_server.sh
```

Fully automated: virtual environment, dependencies, migrations, demo user, server startup.

## Individual Scripts

### **setup_system_dependencies.sh**
Installs Python 3.13 and optional PostgreSQL.

```bash
./deployment_scripts/setup_system_dependencies.sh
```

### **setup_python_environment.sh**
Creates virtual environment and installs Python packages.

```bash
cd kraken_d0010_project
../deployment_scripts/setup_python_environment.sh
```

### **setup_databases.sh**
Configures SQLite (dev) or PostgreSQL (prod) with migrations.

```bash
cd kraken_d0010_project
../deployment_scripts/setup_databases.sh sqlite
# or
../deployment_scripts/setup_databases.sh postgresql
```

## Manual Deployment

Step-by-step alternative:

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8001
```

Visit http://127.0.0.1:8001/admin/
