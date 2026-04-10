# CivicFlow Grievance Hub - API Documentation

## Base URL
- **Development**: `http://localhost:5000/api`
- **Production**: `https://api.civicflow.example.com/api`

## Authentication
Currently uses basic authentication. JWT tokens will be added in v2.

## Response Format
All responses are JSON:
```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful"
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

---

## Complaint Endpoints

### Submit Complaint
**POST** `/complaints/submit`

Submit a new citizen complaint with automatic classification.

**Request:**
```json
{
  "name": "John Doe",
  "phone": "9876543210",
  "email": "john@example.com",
  "language": "en",
  "location": "Downtown, City",
  "complaint_text": "No electricity in my area for 3 days"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "ref_id": "GRV-0001-2024",
    "category": "Electricity",
    "priority": "High",
    "department": "Power Distribution",
    "status": "New"
  },
  "message": "Complaint submitted successfully"
}
```

**Status Codes:**
- `201` - Created successfully
- `400` - Invalid input
- `500` - Server error

---

### Get Complaint by ID
**GET** `/complaints/{id}`

Retrieve complaint details by ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "ref_id": "GRV-0001-2024",
    "name": "John Doe",
    "phone": "9876543210",
    "email": "john@example.com",
    "location": "Downtown",
    "complaint_text": "No electricity...",
    "category": "Electricity",
    "priority": "High",
    "department": "Power Distribution",
    "status": "New",
    "assigned_to": null,
    "resolution_notes": "",
    "created_at": "2024-01-15T10:30:00",
    "resolved_at": null
  }
}
```

---

### Get Complaint by Reference ID
**GET** `/complaints/{ref_id}`

Retrieve complaint using reference ID (e.g., GRV-0001-2024).

**Response:**
Same format as above.

---

### Update Complaint Status
**PUT** `/complaints/{id}`

Update complaint status and add resolution notes.

**Request:**
```json
{
  "status": "In Progress",
  "resolution_notes": "Issue assigned to maintenance team"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "In Progress",
    "assigned_to": "Admin User",
    "updated_at": "2024-01-15T11:00:00"
  }
}
```

**Status Values:**
- `New` - Just submitted
- `In Progress` - Being handled
- `Resolved` - Issue fixed
- `Closed` - Case closed

---

### Search Complaints
**GET** `/complaints/search`

Search complaints with filters and pagination.

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `per_page` (integer, default: 10) - Results per page
- `category` (string) - Filter by category
- `status` (string) - Filter by status
- `priority` (string) - Filter by priority (High, Medium, Normal)
- `location` (string) - Filter by location
- `search` (string) - Search in complaint text

**Example:**
```
GET /complaints/search?page=1&status=New&priority=High&category=Electricity
```

**Response:**
```json
{
  "success": true,
  "data": {
    "complaints": [
      {
        "id": 1,
        "ref_id": "GRV-0001-2024",
        "category": "Electricity",
        "priority": "High",
        "status": "New",
        "location": "Downtown"
      }
    ],
    "total": 150,
    "page": 1,
    "pages": 15
  }
}
```

---

## Classification Endpoint

### Classify Text
**POST** `/classify`

Get classification for custom text.

**Request:**
```json
{
  "text": "Water is not coming in my area for a week"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "category": "Water Supply",
    "department": "Water Resources",
    "priority": "High"
  }
}
```

---

## Admin Endpoints

### Get Dashboard Statistics
**GET** `/admin/dashboard`

Get overview statistics for admin dashboard.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_complaints": 1250,
    "high_priority_count": 45,
    "new_complaints": 120,
    "in_progress": 85,
    "resolved": 1000,
    "closed": 45,
    "category_distribution": {
      "Electricity": 350,
      "Water Supply": 280,
      "Sanitation": 210,
      "Roads": 250,
      "Public Services": 160
    },
    "priority_breakdown": {
      "High": 45,
      "Medium": 200,
      "Normal": 1005
    }
  }
}
```

---

### Get All Complaints (Admin)
**GET** `/admin/complaints`

Get paginated list of all complaints with admin details.

**Query Parameters:**
- `page` (integer, default: 1)
- `per_page` (integer, default: 20)
- `status` (string) - Filter by status
- `priority` (string) - Filter by priority
- `assigned_to` (string) - Filter by assignee
- `sort_by` (string) - Sort field (created_at, priority, status)
- `sort_order` (string) - asc or desc

**Response:**
```json
{
  "success": true,
  "data": {
    "complaints": [
      {
        "id": 1,
        "ref_id": "GRV-0001-2024",
        "name": "John Doe",
        "category": "Electricity",
        "priority": "High",
        "status": "New",
        "assigned_to": null,
        "created_at": "2024-01-15T10:30:00"
      }
    ],
    "total": 1250,
    "page": 1,
    "pages": 63
  }
}
```

---

### Assign Complaint to Staff
**PUT** `/admin/complaints/{id}/assign`

Assign complaint to staff and mark as In Progress.

**Request:**
```json
{
  "assigned_to": "Officer Name",
  "priority": "High"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "In Progress",
    "assigned_to": "Officer Name"
  }
}
```

---

### Mark Complaint as Resolved
**PUT** `/admin/complaints/{id}/resolve`

Mark complaint as resolved with notes.

**Request:**
```json
{
  "resolution_notes": "Electricity restored at 2 PM",
  "attachments": ["receipt.pdf"]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "Resolved",
    "resolved_at": "2024-01-16T14:00:00"
  }
}
```

---

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Create new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "phone": "9876543210",
  "password": "secure_password123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "phone": "9876543210"
  },
  "message": "User registered successfully"
}
```

---

### Login
**POST** `/auth/login`

Authenticate user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "is_admin": false,
    "token": "jwt_token_here"
  }
}
```

---

## Health Check

### Check API Status
**GET** `/health`

Verify API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T12:00:00",
  "version": "1.0.0"
}
```

---

## Error Codes

| Code | Status | Meaning |
|------|--------|---------|
| `400` | Bad Request | Invalid input parameters |
| `401` | Unauthorized | Authentication required |
| `403` | Forbidden | Insufficient permissions |
| `404` | Not Found | Resource not found |
| `409` | Conflict | Resource conflict (duplicate) |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Server Error | Internal server error |
| `503` | Service Unavailable | Maintenance in progress |

---

## Rate Limiting

Currently not enforced. Will be added in production.

**Future Limits:**
- 100 requests per minute per IP
- 1000 requests per hour per user

---

## Pagination

For endpoints that return lists:
- Default page: 1
- Default per_page: 10-20
- Maximum per_page: 100

```
GET /complaints/search?page=2&per_page=50
```

---

## Sorting

Sortable fields:
- `created_at` - Complaint creation date
- `priority` - Complaint priority
- `status` - Current status
- `updated_at` - Last update time

```
GET /complaints/search?sort_by=priority&sort_order=desc
```

---

## Request Headers

```
Content-Type: application/json
Accept: application/json
Authorization: Bearer <token>  (future)
```

---

## Response Status Codes

- `200` - OK (successful GET/PUT)
- `201` - Created (successful POST)
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Server Error

---

## Example Workflow

1. **Submit complaint**
   ```
   POST /complaints/submit
   ```
   Response: `ref_id: GRV-0001-2024`

2. **Check status (citizen)**
   ```
   GET /complaints/GRV-0001-2024
   ```
   Response: Status and details

3. **View dashboard (admin)**
   ```
   GET /admin/dashboard
   ```
   Response: Statistics and metrics

4. **Assign complaint**
   ```
   PUT /admin/complaints/1/assign
   ```

5. **Resolve complaint**
   ```
   PUT /admin/complaints/1/resolve
   ```

---

## Testing with cURL

```bash
# Submit complaint
curl -X POST http://localhost:5000/api/complaints/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "9876543210",
    "location": "City Center",
    "complaint_text": "Road is full of potholes"
  }'

# Get complaint
curl http://localhost:5000/api/complaints/1

# Search complaints
curl "http://localhost:5000/api/complaints/search?status=New&priority=High"

# Get dashboard
curl http://localhost:5000/api/admin/dashboard

# Classify text
curl -X POST http://localhost:5000/api/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Water supply is contaminated"}'
```

---

## WebSocket Support (Future)

Real-time complaint updates via WebSocket:
```
ws://localhost:5000/socket.io
```

---

## API Versioning

Current version: v1 (implicit)

Future versions will be under:
- `/api/v2/complaints/...`

---

## CORS Configuration

Allowed Origins (development):
- `http://localhost:3000`
- `http://localhost:5173`

Production origins configured via environment variables.

---

## Rate Limiting (Future)

Planned rate limits:
- Anonymous: 30 requests/minute
- Authenticated: 300 requests/minute
- Admin: 1000 requests/minute

---

**Last Updated**: 2024
**API Version**: 1.0.0
