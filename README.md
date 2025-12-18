# Kraken D0010 - Electricity Meter Reading System

Django-based system for processing D0010 electricity meter reading files.

## Overview

The D0010 format is a standardized file format used in the UK energy industry for transmitting electricity meter readings between suppliers, distributors, and metering agents.

## Features

- Import and parse D0010 format files
- Normalized database schema for meter readings
- Django admin interface for data management
- Support for multiple meter types and registers

## Technology Stack

- **Python 3.13+**
- **Django 6.0**
- **SQLite** (development) / **PostgreSQL** (production)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver 8001
```

## Project Structure

```
kraken_d0010_project/
├── manage.py
├── config/          # Django project settings
└── meter_readings/          # Main application
```
