# Testing Dashboard - Complete Guide

**Self-Service Data Management for Kraken D0010**

---

## Overview

The Testing Dashboard provides a web-based interface for:
- Importing D0010 sample files
- Viewing database statistics
- Managing test data
- Resetting for demos
- Streamlined testing GUI for development

When to Use:

- Setting up a new development environment or pre-prod testing
- Regenerating test data or deploying new file formats / features
- Creating fresh demo datasets
- Testing import functionality
- Platform / Application Development

**Access:** http://127.0.0.1:8001/admin/testing/

**Requirements:** Admin login required

---

## Sample Data Generation

### Automated Sample Files

The project includes `sample_files_generator.sh` to create an expanded test data set to test for diverse data in the domain:

**Location:** `kraken_d0010_project/sample_files_generator.sh`

**Usage:**
```bash
# Generate 12 diverse D0010 test files
bash sample_files_generator.sh
```

**What It Creates:**

**Generated Test Files (10):**
- `residential_smart_meters.uff` - Smart meters with day/night registers
- `commercial_properties.uff` - Business consumption data
- `industrial_meters.uff` - High-volume industrial sites
- `prepayment_meters.uff` - Prepay meter data
- `mixed_recent_readings.uff` - Various recent dates
- `economy7_meters.uff` - Dual-rate tariff meters
- `small_business.uff` - SME consumption patterns
- `march_readings.uff` - Monthly billing cycle data
- `multiple_daily_readings.uff` - Frequent reading patterns
- `register_showcase.uff` - Multi-register examples

**Reference File (1):**
- `DTC5259515123502080915D0010.uff` - D0010 specification example (13 readings)
- Original source: [D0010 Example File Source](https://gist.github.com/codeinthehole/de956088bab2a9168c7647fdf1be7cc5)

**Duplicate Test File (1):**
- `example_d0010_duplicate.uff` - Copy of DTC file for duplicate detection testing

**Total:** 12 files, 78 meter readings across 51+ unique MPANs

**Result:** Files created in `sample_data/` directory, ready for import via dashboard

**File Discovery:** The Testing Dashboard picks up all .uff files placed in the `sample_data/` directory

---

## Sample Data Reference

| File | Readings | Description |
|------|----------|-------------|
| commercial_properties.uff | 5 | Business meters |
| DTC5259515123502080915D0010.uff | 13 | D0010 specification reference |
| economy7_meters.uff | 8 | Day/night tariff |
| example_d0010 copy.uff | 13 | Duplicate detection test |
| industrial_meters.uff | 6 | High-consumption |
| march_readings.uff | 7 | March 2024 data |
| mixed_recent_readings.uff | 6 | Recent dates |
| multiple_daily_readings.uff | 8 | Multiple per day |
| prepayment_meters.uff | 5 | Prepayment type |
| register_showcase.uff | 10 | All register types |
| residential_smart_meters.uff | 5 | Smart meters |
| small_business.uff | 5 | Small commercial |

**Total:** 91 readings across 12 files


## Dashboard Interface

The testing dashboard at `/admin/testing/` provides a straightforward GUI interface for developers to import D0010 datasets more quickly with these components:

**Statistics Panel** - Real-time counts (FlowFiles, MeterPoints, Meters, Readings)

**Sample Files Table** - Lists `.uff` files with status (✅ imported / ⬜ available) and import buttons

**Import Actions** - Individual file import or batch "Import All Unimported Files" to support development and testing

**Clear All Data** - Red button in danger zone (requires confirmation, deletes all database records)

**Recently Imported** - Shows last 5 imported files with reading counts and timestamps

---

## Common Workflows

### Demo Setup (Clean Start)

```
1. Access /admin/testing/
2. Click "Clear All Data" → Confirm
3. Verify statistics show all zeros
4. Click "Import All Unimported Files"
5. Wait for completion
6. Verify statistics:
   - FlowFiles: 13
   - MeterPoints: 51
   - Meters: 51
   - Readings: 78
7. Navigate to /admin/meter_readings/reading/
8. Demo data ready!
```

**Time:** ~30 seconds

---

### Selective Import Test

```
1. Clear all data
2. Import only: sample_b_d0010.uff
3. Verify: 13 readings, 11 meter points
4. Test search for MPAN: 1200023305967
5. Should find 1 reading
6. Import: commercial_properties.uff
7. Verify: 19 readings total
8. Test search still works
```

**Purpose:** Validate incremental import behavior

---

## Testing Standards & Configuration

### Pre-Configured Quality Tools

The project includes pre-configured testing and code quality tools:

**`.coveragerc`** - Test coverage configuration:
- Focuses on application logic (`meter_readings`, `config` modules)
- Excludes migrations, test files, and deployment scripts
- Achieves 100% coverage of relevant codebase

**`.flake8`** - Linting configuration:
- Enforces code style consistency
- Compatible with Black formatter (88 char line length)
- Excludes virtual environments and generated files

### Running Tests

**Test Suite** (79 tests):
```bash
python manage.py test
```

**With Coverage Report**:
```bash
python -m coverage run --rcfile=../.coveragerc manage.py test meter_readings.tests
python -m coverage report
python -m coverage html  # Generate HTML report (output: coverage_html_report/index.html)
```

**Code Formatting** (Black):
```bash
black meter_readings/ config/          # Format code
black --check meter_readings/ config/  # Verify formatting
```

**Linting** (Flake8):
```bash
flake8 meter_readings/ config/  # Run linter
```

**Note**: These standards can be configured and extended as the project grows or scales.

---

### Duplicate Prevention Test

```
1. Import 'DTC5259515123502080915D0010.uff`
2. Note reading count (13)
3. Try `example_d0010_duplicate.uff`
4. Verify reading count unchanged (13)
5. Check FlowFile count
```

**Purpose:** Confirm duplicate detection works (no collision)

---

### Full Reset Cycle

```
1. Import all files → 78 readings
2. Browse data in admin
3. Clear all data → 0 readings
4. Import all files again → 78 readings
5. Data should be identical to step 1
```

**Purpose:** Test repeatability and data consistency

---

## Technical Details

### File Discovery

```python
sample_dir = settings.BASE_DIR / 'sample_data'
sample_files = list(sample_dir.glob('*.uff'))
```

**Scans:** `kraken_d0010_project/sample_data/`  
**Filter:** Files ending in `.uff`  
**Sort:** Alphabetical order

---

### Import Status Logic

```python
# Check if file already imported
imported_filenames = FlowFile.objects.values_list('filename', flat=True)

for file in sample_files:
    is_imported = file.name in imported_filenames
    # Show ✅ if imported, ⬜ if not
```

---

### Import Process

```python
# Individual import
subprocess.run([
    'python', 'manage.py', 'import_d0010', 
    f'sample_data/{filename}'
], capture_output=True)

# Parse output for success/error messages
# Update UI with results
```

---

## Permissions

### Access Control

```python
@staff_member_required
def testing_dashboard(request):
    # Only admin / logged in user can access data management
    ...
```

**Required:** User must be:
- Authenticated (logged in)
- Staff member (`is_staff=True`)

**Non-staff users:** 404 error

---

## Error Handling

### Import Errors

```python
try:
    result = subprocess.run([...])
    if result.returncode != 0:
        messages.error(request, f"Import failed: {result.stderr}")
except Exception as e:
    messages.error(request, f"Error: {str(e)}")
```

**Shown in UI:**
```
❌ Import failed for industrial_meters.uff
   Error: Invalid D0010 header format
```

---

### File Not Found

```python
if not sample_dir.exists():
    messages.warning(request, "Sample data directory not found")
```

**Shown in UI:**
```
⚠️ Sample data directory not found
   Create sample_data/ directory with .uff files
```

---


## Troubleshooting

### "No files shown"

**Check:**
```bash
ls sample_data/*.uff
```

**Should show:** 12 .uff files

**If empty:** Run `bash sample_files_generator.sh`

---

### "Import does nothing"

**Check server logs:**
```bash
# Test import manually
python manage.py import_d0010 sample_data/sample_b_d0010.uff
```

---

### "Clear button not working / UI does not load"

**Check:**
1. JavaScript enabled in browser?
2. Check Console / Server Logs / Error Code?
3. Check browser console for errors

**Try:** Different browser (Chrome Incognito)

---

**Quick Reference Card**

```
Access: http://127.0.0.1:8001/admin/testing/
Login:  demo_admin / KrakenDemo123!

Actions:
├─ Import single file: Click "Import" next to filename
├─ Import all files:   Click "Import All Unimported Files"
└─ Clear database:     Click "Clear All Data" (confirm)

Statistics Updated:    Every page load
File Status:           ✅ = imported, ⬜ = available
```
