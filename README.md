# 🦑 Kraken D0010 - Electricity Meter Reading System

Django-based system for processing D0010 electricity meter reading files used in the UK energy industry.

**Author**: Matthew Brenton Hall

**Author:** Matthew Brenton Hall

![python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)
![django 6.0](https://img.shields.io/badge/django-6.0-green.svg)

## Overview

This Django application processes D0010 electricity meter reading flow files. It provides a file import service for pipe-delimited text files containing D0010 meter readings alongside a web admin management interface for browsing and searching the data. The architecture and codebase have been structured with supportive design patterns, tools and documentation to maintain and enhance the project for other developers to extend.

## Features

### ✅ Functional Requirements
- Import D0010 files via command line
- Parse pipe-delimited text format
- Store meter readings with associated metadata
- Django admin interface for data browsing
- Search by MPAN (Meter Point Administration Number)
- Search by meter serial number
- Display source filename for each reading
- Comprehensive test suite

### ✅ Non-Functional Requirements
- Robust error handling with domain-specific exceptions
- Data validation and integrity at model and database levels
- Performance optimized queries with database indexes
- Maintainable code structure with type hints throughout
- Production-ready configuration
- Extensible architecture for adding new record types or API endpoints

## Quick Start

### 1. Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 3. Import Sample Data
```bash
python manage.py import_d0010 sample_data/sample_d0010.uff
```

### 4. Start Server
```bash
python manage.py runserver 8001  # Port 8001 to avoid conflicts
```

Visit `http://localhost:8001/admin/` to access the admin interface.

## Usage

### Command Line Import
```bash
# Import single file
python manage.py import_d0010 /path/to/d0010_file.uff

# Import multiple files
python manage.py import_d0010 file1.uff file2.uff

# Dry run (test without saving)
python manage.py import_d0010 --dry-run file.uff
```

The import command handles errors gracefully—invalid records are logged but don't halt processing, and successful records are saved even when some fail.

### Admin Interface
1. Login at `/admin/` with your superuser credentials
2. Navigate to "Readings" section
3. Use search functionality:
   - Search by MPAN: `1200023305967`
   - Search by Serial: `F75A 00802`
   - Search by Filename: `sample_d0010.uff`

## Testing

### Running Tests
```bash
# Run all tests (79 tests in test suite)
python manage.py test

# Run tests with coverage
python -m coverage run --rcfile=../.coveragerc manage.py test meter_readings.tests
python -m coverage report
python -m coverage html  # Generates coverage_html_report/index.html
```

**Coverage Report Output:**
```
Name                                                 Stmts   Miss    Cover   Missing
------------------------------------------------------------------------------------
config/__init__.py                                       0      0  100.00%
config/urls.py                                           4      0  100.00%
meter_readings/__init__.py                               0      0  100.00%
meter_readings/admin.py                                 77      0  100.00%
meter_readings/admin_views.py                           66      0  100.00%
meter_readings/api_urls.py                              10      0  100.00%
meter_readings/api_views.py                            137      0  100.00%
meter_readings/apps.py                                   5      0  100.00%
meter_readings/exceptions.py                            45      0  100.00%
meter_readings/management/__init__.py                    0      0  100.00%
meter_readings/management/commands/__init__.py           0      0  100.00%
meter_readings/management/commands/import_d0010.py     129      0  100.00%
meter_readings/models.py                                76      0  100.00%
meter_readings/serializers.py                           51      0  100.00%
meter_readings/urls.py                                   4      0  100.00%
meter_readings/utils.py                                 19      0  100.00%
meter_readings/views.py                                  7      0  100.00%
------------------------------------------------------------------------------------
TOTAL                                                  630      0  100.00%
```

## Test Quality Standards

The codebase meets professional testing standards with comprehensive test coverage and quality:

### Test Coverage: 100%

- **79 passing tests** covering all application modules  
- Pre-configured via `.coveragerc` for `meter_readings` and `config` modules
- All modules at 100% coverage:
  - Models (validation, constraints, relationships)
  - Admin interface (actions, filters, customizations)
  - Admin views (testing dashboard, file upload, data management)
  - API views (REST endpoints, filtering, pagination, serialization)
  - Views (dashboard rendering, statistics, HTML generation)
  - Management commands (D0010 import, error handling, dry-run mode)
  - Serializers (data transformation, nested relationships)

### Code Formatting: Black (Zero Violations)

- Consistent code style across entire codebase
- Line length: 88 characters (Black default)
- **Format code**: `black meter_readings/ config/`
- **Verify**: `black --check meter_readings/ config/`

### Linting: Flake8 (Zero Errors or Warnings)

- Pre-configured via `.flake8` with project-specific rules
- No unused imports, undefined names, or style violations
- **Run linting**: `flake8 meter_readings/ config/`
- **Note**: Testing standards can be configured and extended as the project grows to uphold code quality & project structure

## Test Coverage Details

The project includes comprehensive tests covering:

- **Model Tests**: Validation rules, database constraints, unique constraints, foreign key relationships, string representations
- **Admin Tests**: List displays, search functionality, filters, custom actions, inline editing, permissions
- **Admin View Tests**: Testing dashboard, file import (success/error cases), bulk operations, data clearing, sample file detection
- **API Tests**: All REST endpoints (GET/POST), filtering (MPAN, dates, types), pagination, search, ordering, custom actions, error handling
- **View Tests**: Dashboard rendering, statistics accuracy, HTML structure, CSS styling, empty state handling
- **Command Tests**: D0010 import (success/error cases), dry-run mode, file parsing, data validation, error logging, duplicate handling
- **Serializer Tests**: Data transformation, nested relationships, field validation

**Coverage Configuration**: The project uses `.coveragerc` to focus testing on application logic (`meter_readings` and `config` modules), excluding migrations, tests, and deployment files. This configuration can be extended as the project scales.

### Run Tests with Coverage
```bash
# Run all tests with coverage report
python -m coverage run --rcfile=../.coveragerc manage.py test meter_readings.tests
python -m coverage report

# Generate HTML coverage report
python -m coverage html
# View at: coverage_html_report/index.html
```

**Current test coverage**: 100% across all application modules.

## Architecture

### Database Models
- **FlowFile**: Source file tracking
- **MeterPoint**: MPAN-identified consumption points
- **Meter**: Physical devices with serial numbers
- **Reading**: Time-stamped consumption values

### Key Features
- Normalized database schema
- Foreign key relationships
- Database indexes for performance
- Transaction-safe imports (rollback on critical errors)
- Comprehensive validation at multiple layers
- Production-ready logging with appropriate severity levels
- Custom exception hierarchy (`exceptions.py`) for clear error categorisation

## Test Data

The sample file contains 13 meter readings across 11 meter points for demonstration:
- MPANs like `1200023305967`, `1900001059816`
- Meter serials like `F75A 00802`, `S95105287`
- Various register types (S, TO, 01, 02, A1, DY, NT)

With this reference we have created and compiled an expanded data-set to map on to the broader system domain

| File | Readings | Description |
|:----:|:--------:|:-----------:|
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

**Full Documentation** - Review 


## Assumptions Made

This implementation makes the following assumptions about the D0010 file format and business logic based on technical research, D0010 business context and publicly available data protocols:

### D0010 Format Interpretation
- **Pipe-delimited structure**: Fields separated by `|` character
- **Record types**: ZHV (header), 026 (MPAN), 028 (Meter), 030 (Reading), ZPT (trailer)
- **Hierarchy**: One 026 can have multiple 028s, one 028 can have multiple 030s
- **Date format**: Reading dates in `YYYYMMDDHHMMSS` format (14 characters)
- **Timezone**: All reading dates assumed to be in Europe/London timezone
- **Trailing records**: ZPT trailer record is optional (files without it are still valid)

### Business Logic
- **Register IDs**: Register IDs like 'S', 'DY', 'NT', '01', '02', 'A1' map to different consumption types:
  - 'S' = Standard single-rate register
  - 'DY' = Economy 7 day rate
  - 'NT' = Economy 7 night rate
  - '01', '02' = Multi-rate registers
- **Reading types**: Defaulting to 'ACTUAL' readings when not specified (vs CUSTOMER or ESTIMATED)
- **Meter types**: Using single-character codes: D (Debit/Standard), C (Credit), P (Prepayment)
- **Duplicate prevention**: Files with the same name cannot be imported twice (prevents accidental re-import)
- **Data integrity**: Using database transactions to ensure all-or-nothing imports

### Validation Rules
- **MPAN format**: Must be exactly 13 digits
- **Reading values**: Must be non-negative decimal numbers
- **Serial numbers**: Cannot be empty strings
- **Date range**: No future dates allowed for readings

## Ideas for Improvement

The following enhancements could be added to make this a production-ready system:

| # | Feature | Description |
|:-:|:-------:|:-----------:|
| 1 | **Async Processing** | Integrate Celery for background processing of large files |
| 2 | **Export Functionality** | Allow exporting readings back to D0010 format or CSV |
| 3 | **Bulk Operations** | Admin actions for bulk re-processing or data corrections manually or automatically |
| 4 | **Caching Layer** | Add Redis for frequently accessed meter point lookups |
| 5 | **Batch Import Optimization** | Stream-based parsing for files with 100k+ readings |
| 6 | **Import Progress Tracking** | WebSocket-based real-time import progress |
| 7 | **Data Visualization** | Charts showing consumption trends over time |
| 8 | **Audit Trail** | Track who imported which files and when |
| 9 | **Anomaly Detection** | Flag unusual consumption patterns (e.g., sudden spikes) |
| 10 | **Implement Cloud Infrastructure for Production** | Designate and architecture a distributed cloud system for high performance and meter reading management for architecture at scale |
| 11 | **Consider AI / Intelligent Analysis Applications** | To leverage AI / ML insights, analysis and feedback on accumulated meter reading data |

## Demo URLs / Access Points

**Using a browser and making sure to use HTTP** e.g `http://127.0.0.1` (see console for URL / direct link when running `./run_demo_server.sh`)

### Admin Interface

| Feature | URL |
|:-------:|:---:|
| Admin Home | http://127.0.0.1:8001/admin/ |
| Testing Dashboard | http://127.0.0.1:8001/admin/testing/ |
| Flow Files | http://127.0.0.1:8001/admin/meter_readings/flowfile/ |
| Meter Points | http://127.0.0.1:8001/admin/meter_readings/meterpoint/ |
| Meters | http://127.0.0.1:8001/admin/meter_readings/meter/ |
| Readings | http://127.0.0.1:8001/admin/meter_readings/reading/ |

### REST API

| Feature | URL |
|:-------:|:---:|
| API Root | http://127.0.0.1:8001/api/ |
| Swagger UI | http://127.0.0.1:8001/api/docs/ |
| ReDoc | http://127.0.0.1:8001/api/redoc/ |
| OpenAPI Schema | http://127.0.0.1:8001/api/schema/ |

### API Endpoints

| Resource | URL |
|:--------:|:---:|
| Flow Files | http://127.0.0.1:8001/api/flow-files/ |
| Meter Points | http://127.0.0.1:8001/api/meter-points/ |
| Meters | http://127.0.0.1:8001/api/meters/ |
| Readings | http://127.0.0.1:8001/api/readings/ |

## Project Status

**Implementation** - Solution to address the full requirements of the technical challenge

- **Correctness**: Addresses all specified requirements and documented/configured for future development
- **Maintainability**: Clean, documented, tested code with type hints, coverage, linting and consistent code conventions that other developers can follow
- **Robustness**: Graceful error handling via custom exceptions, partial import handling, errors are logged with context and can be reviewed with pre-configured tests - file validation on import process
- **Production Ready**: Deployment processes could be fully automated with dual-database and Postgres already integrated for future builds - .env configuration is secure and production security config has already been initialised and structured

## Additional Documentation

For comprehensive information about the system, see the following documentation:

| Document | Purpose | When to Use |
|:--------:|:-------:|:-----------:|
| [QUICKSTART.md](QUICKSTART.md) | 2-minute setup guide | Getting started quickly, first-time setup |
| [documentation/TESTING_GUIDE.md](documentation/TESTING_GUIDE.md) | Testing dashboard guide | Using the self-service testing interface, importing sample data |
| [documentation/API_DOCUMENTATION.md](documentation/API_DOCUMENTATION.md) | REST API reference | API integration, endpoint usage, authentication |
| [documentation/DEPLOYMENT_GUIDE.md](documentation/DEPLOYMENT_GUIDE.md) | Production deployment | Server deployment, database configuration, scaling |
| [deployment_scripts/README.md](deployment_scripts/README.md) | Automated deployment scripts | macOS/Linux system setup, dependencies installation |
| [documentation/DEVELOPER_GUIDE.md](documentation/DEVELOPER_GUIDE.md) | Architecture & development patterns | Extending features, understanding codebase structure |
| [SYSTEM_SUMMARY.md](SYSTEM_SUMMARY.md) | Complete system overview | High-level understanding, feature summary, release notes |

## Testing

### Running Tests
```bash
# Run all tests (101 comprehensive tests)
python manage.py test

# Run tests with coverage
pip install coverage
coverage run manage.py test
coverage report
coverage html  # Generates htmlcov/index.html
```

### Test Quality Standards

The codebase meets professional testing standards with comprehensive test coverage and quality:

#### Test Coverage: 100%
- **74 passing tests** covering all application modules
- **1199 statements** with full coverage
- All modules at 100% coverage:
  - Models (validation, constraints, relationships)
  - Admin interface (actions, filters, customizations)
  - Admin views (testing dashboard, file upload, data management)
  - API views (REST endpoints, filtering, pagination, serialization)
  - Views (dashboard rendering, statistics, HTML generation)
  - Management commands (D0010 import, error handling, dry-run mode)
  - Serializers (data transformation, nested relationships)

#### Code Formatting: Black (Zero Violations)
- **28 files** formatted with Black
- Line length: 88 characters (Black default)
- Consistent code style across entire codebase
- Run: `black meter_readings/ config/`
- Verify: `black --check meter_readings/ config/`

#### Linting: Flake8 (Zero Errors or Warnings)
- All Python files pass Flake8 linting
- No unused imports, undefined names, or style violations
- Maximum line length: 88 characters (compatible with Black)
- Run: `flake8 meter_readings/ config/ --exclude=migrations,__pycache__,venv --max-line-length=88`

### Test Coverage Details
The project includes comprehensive tests covering:
- **Model Tests**: Validation rules, database constraints, unique constraints, foreign key relationships, string representations
- **Admin Tests**: List displays, search functionality, filters, custom actions, inline editing, permissions
- **Admin View Tests**: Testing dashboard, file import (success/error cases), bulk operations, data clearing, sample file detection
- **API Tests**: All REST endpoints (GET/POST), filtering (MPAN, dates, types), pagination, search, ordering, custom actions, error handling
- **View Tests**: Dashboard rendering, statistics accuracy, HTML structure, CSS styling, empty state handling
- **Command Tests**: D0010 import (success/error cases), dry-run mode, file parsing, data validation, error logging, duplicate handling
- **Serializer Tests**: Data transformation, nested relationships, field validation

Current test coverage: **100% across all modules** (1199 statements covered).

## Assumptions Made

This implementation makes the following assumptions about the D0010 file format and business logic:

### D0010 Format Interpretation
- **Pipe-delimited structure**: Fields separated by `|` character
- **Record types**: ZHV (header), 026 (MPAN), 028 (Meter), 030 (Reading), ZPT (trailer)
- **Hierarchy**: One 026 can have multiple 028s, one 028 can have multiple 030s
- **Date format**: Reading dates in `YYYYMMDDHHMMSS` format (14 characters)
- **Timezone**: All reading dates assumed to be in Europe/London timezone
- **Trailing records**: ZPT trailer record is optional (files without it are still valid)

### Business Logic
- **Register IDs**: Register IDs like 'S', 'DY', 'NT', '01', '02', 'A1' map to different consumption types:
  - 'S' = Standard single-rate register
  - 'DY' = Economy 7 day rate
  - 'NT' = Economy 7 night rate
  - '01', '02' = Multi-rate registers
- **Reading types**: Defaulting to 'ACTUAL' readings when not specified (vs CUSTOMER or ESTIMATED)
- **Meter types**: Using single-character codes: D (Debit/Standard), C (Credit), P (Prepayment)
- **Duplicate prevention**: Files with the same name cannot be imported twice (prevents accidental re-import)
- **Data integrity**: Using database transactions to ensure all-or-nothing imports

### Validation Rules
- **MPAN format**: Must be exactly 13 digits
- **Reading values**: Must be non-negative decimal numbers
- **Serial numbers**: Cannot be empty strings
- **Date range**: No future dates allowed for readings

## Ideas for Improvement

The following enhancements could be added to make this a production-ready system:

### Immediate Enhancements
1. **REST API File Upload**: Add endpoint for uploading D0010 files via HTTP POST
2. **Async Processing**: Integrate Celery for background processing of large files
3. **Validation Reports**: Generate detailed reports of data quality issues found during import
4. **Export Functionality**: Allow exporting readings back to D0010 format or CSV
5. **Bulk Operations**: Admin actions for bulk re-processing or data corrections

### Scalability Improvements
6. **Read Replicas**: Configure PostgreSQL read replicas for admin queries
7. **Caching Layer**: Add Redis for frequently accessed meter point lookups
8. **Batch Import Optimization**: Stream-based parsing for files with 100k+ readings
9. **Partitioning**: Partition readings table by date for better query performance
10. **API Rate Limiting**: Per-user rate limits for API endpoints

### User Experience
11. **Import Progress Tracking**: WebSocket-based real-time import progress
12. **Data Visualization**: Charts showing consumption trends over time
13. **Search Enhancements**: Full-text search across all fields, saved searches
14. **Audit Trail**: Track who imported which files and when
15. **Notifications**: Email alerts for import failures or data anomalies

### Data Quality
16. **Duplicate Detection**: Identify potential duplicate readings across different files
17. **Anomaly Detection**: Flag unusual consumption patterns (e.g., sudden spikes)
18. **Data Reconciliation**: Compare imported totals against expected values from source systems
19. **Schema Validation**: Pre-validate files against D0010 schema before import
20. **Historical Tracking**: Maintain history of reading corrections/updates
