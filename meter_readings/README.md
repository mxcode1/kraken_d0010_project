# Meter Readings App

Django app for D0010 meter reading data management.

## Models

### FlowFile
Tracks imported D0010 files to prevent duplicate processing.

### MeterPoint
MPAN (Meter Point Administration Number) - unique electricity supply identifier.

### Meter
Physical meter device with serial number, linked to MeterPoint.

### Reading
Individual meter reading with date, value, and register information.

## Relationships

```
FlowFile ──┐
           ├─→ Reading ─→ Meter ─→ MeterPoint
           │
           └─→ Reading ─→ Meter ─→ MeterPoint
```

## Data Flow

1. Import D0010 file → Create FlowFile
2. Parse readings → Link to existing or create new Meters/MeterPoints
3. Store Reading records with all relationships

## Import Command

```bash
# Import file
python manage.py import_d0010 sample_data/file.uff

# Dry-run (validation only)
python manage.py import_d0010 sample_data/file.uff --dry-run
```
