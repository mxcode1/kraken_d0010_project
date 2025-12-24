# Kraken D0010 REST API Documentation

## Overview

This REST API provides programmatic access to the D0010 meter reading system. The API supports file uploads, data retrieval, and querying across all meter reading entities. Both the Django admin interface and the REST API utilize the same backend processing logic and database models, ensuring consistency across access methods.

## Base URL
```
http://localhost:8001/api/
```

**Interactive API Documentation**: Visit [http://localhost:8001/api/docs/](http://localhost:8001/api/docs/) in your browser to explore the Swagger UI documentation and test endpoints directly.

## Authentication

Currently configured for open access (demo mode). For production deployments, token-based authentication should be enabled.

## Endpoints

### Flow Files
Manage D0010 UFF file imports and track processing history.

- **List**: `GET /api/flow-files/`
- **Detail**: `GET /api/flow-files/{id}/`
- **Upload**: `POST /api/flow-files/upload/`
- **Filters**: `?filename=`, `?ordering=`

#### Upload D0010 File
Upload and process a D0010 UFF file. The API uses the same import logic as the admin interface (`import_d0010` management command).

**Endpoint**: `POST /api/flow-files/upload/`

**Content-Type**: `multipart/form-data`

**Request**:
```bash
curl -X POST http://localhost:8001/api/flow-files/upload/ \
  -F "file=@sample_data/march_readings.uff"
```

**Success Response** (201 Created):
```json
{
  "id": 1,
  "filename": "march_readings.uff",
  "file_reference": "DTC5259515123502080915D0010",
  "record_count": 13,
  "imported_at": "2025-12-30T12:00:00Z"
}
```

**Error Responses**:

400 Bad Request - Invalid file:
```json
{
  "error": "No file provided"
}
```

400 Bad Request - Wrong file type:
```json
{
  "error": "Invalid file type. Only .uff files are supported."
}
```

500 Internal Server Error - Processing failure:
```json
{
  "error": "Failed to process file: [error details]"
}
```

### Meter Points
Access meter point (MPAN) data including associated meters and readings.

- **List**: `GET /api/meter-points/`
- **Detail**: `GET /api/meter-points/{id}/`
- **Readings**: `GET /api/meter-points/{id}/readings/`
- **Search**: `?search=mpan`

**Example**:
```bash
curl "http://localhost:8001/api/meter-points/?search=1900017449838"
```

### Meters
Query meter installations linked to meter points.

- **List**: `GET /api/meters/`
- **Detail**: `GET /api/meters/{id}/`
- **Filters**: `?meter_type=`, `?meter_point=`
- **Search**: `?search=serial_number`

**Example**:
```bash
curl "http://localhost:8001/api/meters/?meter_type=E"
```

### Readings
Access meter reading records with flexible filtering options.

- **List**: `GET /api/readings/`
- **Detail**: `GET /api/readings/{id}/`
- **Summary**: `GET /api/readings/summary/`
- **Filters**: `?reading_date=`, `?meter=`, `?flow_file=`
- **Date range**: `?reading_date__gte=2025-01-01&reading_date__lte=2025-12-31`

**Example**:
```bash
curl "http://localhost:8001/api/readings/?reading_date__gte=2025-03-01&reading_date__lte=2025-03-31"
```

## Common Features

### Pagination
All list endpoints return paginated results:
```json
{
  "count": 1000,
  "next": "http://localhost:8001/api/readings/?page=2",
  "previous": null,
  "results": [...]
}
```

### Browsable API
The API includes Django REST Framework's browsable interface. Visit any endpoint in a web browser to interact with the API through an HTML form interface.

**Access**: Navigate to `http://localhost:8001/api/` in your browser

### Filtering and Ordering
Most endpoints support query parameters for filtering and sorting:
- **Search**: `?search=value`
- **Ordering**: `?ordering=field_name` or `?ordering=-field_name` (descending)
- **Field filters**: `?field_name=value`
- **Date ranges**: `?date_field__gte=start&date_field__lte=end`

## Usage Examples

### Basic Operations

**Upload a D0010 file**:
```bash
curl -X POST http://localhost:8001/api/flow-files/upload/ \
  -F "file=@sample_data/march_readings.uff"
```

**List all flow files**:
```bash
curl http://localhost:8001/api/flow-files/
```

**Search meter points by MPAN**:
```bash
curl "http://localhost:8001/api/meter-points/?search=1900017449838"
```

**Filter readings by date range**:
```bash
curl "http://localhost:8001/api/readings/?reading_date__gte=2025-03-01&reading_date__lte=2025-03-31"
```

**Get readings summary statistics**:
```bash
curl http://localhost:8001/api/readings/summary/
```

**Filter meters by type**:
```bash
curl "http://localhost:8001/api/meters/?meter_type=E"
```

## Technical Details

### File Upload Requirements

- **File extension**: Must be `.uff`
- **Format**: D0010 flow file specification
- **HTTP Method**: POST
- **Content-Type**: `multipart/form-data`
- **Form field name**: `file`
- **Max file size**: Configured by Django settings (default: 2.5MB)
- **Authentication**: Not required in demo mode

### Backend Processing

The file upload endpoint uses the same processing logic as the Django admin interface:

1. **Validation**: File extension and basic format checks
2. **Temporary Storage**: File saved to Django's temp directory
3. **Import Command**: Calls `import_d0010` management command
4. **Parsing**: D0010 parser extracts meter readings and metadata
5. **Database Storage**: Creates/updates MeterPoint, Meter, Reading, and FlowFile records
6. **Response**: Returns FlowFile object with import statistics

This ensures consistent behavior whether files are uploaded via the admin interface or REST API.

### Data Models

The API exposes the following models:

- **FlowFile**: Represents an imported D0010 file
- **MeterPoint**: MPAN (Meter Point Administration Number) records
- **Meter**: Physical meter installations
- **Reading**: Individual meter readings with registers and values

All models include timestamps (`created_at`, `updated_at`) for audit purposes.

### Error Handling

The API returns standard HTTP status codes:

- **200 OK**: Successful GET request
- **201 Created**: Successful file upload
- **400 Bad Request**: Invalid request (missing file, wrong format, validation errors)
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side processing error

Error responses include a descriptive message in the `error` field.

## Architecture Integration

### Shared Backend
Both access methods (Admin UI and REST API) utilize:
- Same Django models (`meter_readings.models`)
- Same import logic (`import_d0010` management command)
- Same database (SQLite dev / PostgreSQL prod)
- Same query optimization and indexing

### Access Layers
- **Admin Interface**: Human-facing UI at `/admin/`
- **REST API**: Programmatic access at `/api/`
- **Management Commands**: CLI access via `python manage.py`

This architecture ensures data consistency and allows flexible access patterns based on use case requirements.

## Integration Examples

### Python

```python
import requests

# Upload and process a D0010 file
with open('sample_data/march_readings.uff', 'rb') as f:
    response = requests.post(
        'http://localhost:8001/api/flow-files/upload/',
        files={'file': f}
    )
    
if response.status_code == 201:
    flow_file = response.json()
    print(f"Successfully imported {flow_file['record_count']} records")
    print(f"File reference: {flow_file['file_reference']}")
else:
    error = response.json()
    print(f"Upload failed: {error.get('error', 'Unknown error')}")

# Query readings for a specific date range
response = requests.get(
    'http://localhost:8001/api/readings/',
    params={
        'reading_date__gte': '2025-03-01',
        'reading_date__lte': '2025-03-31',
        'ordering': '-reading_date'
    }
)
readings = response.json()
print(f"Found {readings['count']} readings in March 2025")

# Search for a specific meter point
response = requests.get(
    'http://localhost:8001/api/meter-points/',
    params={'search': '1900017449838'}
)
meter_points = response.json()
if meter_points['count'] > 0:
    mpan = meter_points['results'][0]
    print(f"MPAN: {mpan['mpan']}")
```

### JavaScript (Fetch API)

```javascript
// Upload D0010 file
async function uploadD0010File(fileInput) {
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  try {
    const response = await fetch('http://localhost:8001/api/flow-files/upload/', {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log(`Imported ${data.record_count} records from ${data.filename}`);
      return data;
    } else {
      const error = await response.json();
      console.error('Upload failed:', error.error);
      throw new Error(error.error);
    }
  } catch (error) {
    console.error('Network error:', error);
    throw error;
  }
}

// Query readings with filters
async function getReadings(startDate, endDate) {
  const params = new URLSearchParams({
    reading_date__gte: startDate,
    reading_date__lte: endDate,
    ordering: '-reading_date'
  });
  
  const response = await fetch(`http://localhost:8001/api/readings/?${params}`);
  const data = await response.json();
  return data.results;
}
```

### cURL Examples

**Upload with error handling**:
```bash
response=$(curl -s -w "\n%{http_code}" -X POST \
  http://localhost:8001/api/flow-files/upload/ \
  -F "file=@sample_data/march_readings.uff")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 201 ]; then
  echo "Upload successful: $body"
else
  echo "Upload failed (HTTP $http_code): $body"
fi
```

**Query with pagination**:
```bash
# Get first page
curl "http://localhost:8001/api/readings/?page=1"

# Get specific page with filters
curl "http://localhost:8001/api/readings/?page=2&reading_date__gte=2025-03-01"
```
