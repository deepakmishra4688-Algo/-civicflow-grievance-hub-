# CivicFlow Architecture & System Design

## 1. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│                  (React Frontend - Port 3000)                │
└────────────┬─────────────────┬─────────────────┬────────────┘
             │                 │                 │
             │ HTTP REST       │ HTTP REST       │ HTTP REST
             │                 │                 │
┌────────────▼─────────────────▼─────────────────▼────────────┐
│                     API Gateway Layer                         │
│                 (Flask Backend - Port 5000)                  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Flask Blueprint Routes                        │  │
│  │  • /api/complaints/* (CRUD)                          │  │
│  │  • /api/admin/* (Dashboard)                          │  │
│  │  • /api/auth/* (Auth)                                │  │
│  │  • /api/classify (ML)                                │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬─────────────────┬─────────────────┬────────────┘
             │                 │                 │
             │ ORM             │ ML              │ Email
             │                 │                 │
┌────────────▼──────┬──────────▼────────┬───────▼──────────────┐
│  Data Access      │   ML Classifier   │  Notification Layer   │
│  Layer            │                   │                       │
│  ┌────────────┐   │ ┌─────────────┐   │ ┌────────────────┐    │
│  │ SQLAlchemy │   │ │ scikit-learn│   │ │ Flask-Mail     │    │
│  │ Models     │   │ │ (TF-IDF +   │   │ │ (SMTP)         │    │
│  │            │   │ │  NaiveBayes)│   │ │                │    │
│  └────────────┘   │ └─────────────┘   │ │ ┌────────────┐ │    │
│                   │                    │ │ │ SMS (TBD)  │ │    │
│                   │                    │ │ └────────────┘ │    │
└────────────┬──────┴────────────────────┴──────────────────┘    │
             │
             │ ORM/SQL
             │
┌────────────▼─────────────────────────────────────────────────┐
│              Data Persistence Layer                           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         SQL Database                                 │  │
│  │  • SQLite (Development)                              │  │
│  │  • PostgreSQL (Production)                           │  │
│  │                                                      │  │
│  │  Tables:                                             │  │
│  │  • User                                              │  │
│  │  • Complaint                                         │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## 2. Frontend Architecture

### Component Structure
```
App.jsx (Router)
├── Layout.jsx (Navbar, Footer, Outlet)
│   ├── Home.jsx
│   ├── Submit.jsx
│   │   └── Form Component
│   ├── Result.jsx
│   ├── Admin.jsx
│   │   ├── Statistics Panel
│   │   ├── Filters
│   │   └── Complaints Table
│   └── About.jsx
└── Chatbot.jsx (Floating)
```

### Data Flow
```
User Input → Component State (React Hooks)
    ↓
API Call (complaints.js)
    ↓
Flask Backend
    ↓
Response
    ↓
Update UI (State Update)
    ↓
Render (CSS Animations)
```

### Technologies
- **Framework**: React 18.3.1
- **Router**: React Router v6.14.1
- **Build Tool**: Vite 5.4.0
- **Styling**: CSS3 (with animations, transitions)
- **State Management**: React Hooks (useState, useEffect)

## 3. Backend Architecture

### Flask Application Structure
```
app.py
├── Flask app initialization
├── SQLAlchemy configuration
├── Flask-Mail configuration
├── Blueprint registration
│   ├── routes.py (complaints_bp)
│   └── auth.py (admin_bp)
├── Error handlers
└── Health check endpoint

models.py
├── User model
└── Complaint model

classifier.py
├── ML model training
├── Classification logic
└── Priority detection

routes.py
├── complaint_bp blueprint
│   ├── POST /submit
│   ├── GET /<id>
│   ├── PUT /<id>
│   └── GET /search

auth.py
├── admin_bp blueprint
│   ├── POST /auth/register
│   ├── POST /auth/login
│   ├── GET /admin/dashboard
│   ├── GET /admin/complaints
│   └── PUT /admin/complaints/<id>/assign

utils.py
├── Email functions
├── SMS functions
├── PDF generation
└── Translations
```

### Data Flow
```
HTTP Request
    ↓
Flask Route Handler
    ↓
Business Logic (if needed)
    ↓
Database Query (SQLAlchemy)
    ↓
Data Processing
    ↓
JSON Response
    ↓
HTTP Response
```

### Technologies
- **Framework**: Flask 3.0.0
- **ORM**: SQLAlchemy 3.1.1
- **ML**: scikit-learn 1.3.2
- **Email**: Flask-Mail 0.9.1
- **CORS**: Flask-CORS 4.0.0

## 4. Database Schema

### User Table
```sql
CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  email VARCHAR(120) UNIQUE NOT NULL,
  phone VARCHAR(20),
  password_hash VARCHAR(255) NOT NULL,
  is_admin BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Complaint Table
```sql
CREATE TABLE complaint (
  id INTEGER PRIMARY KEY,
  ref_id VARCHAR(20) UNIQUE NOT NULL,  -- GRV-0001-2024
  user_id INTEGER,
  name VARCHAR(120) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  email VARCHAR(120) NOT NULL,
  location VARCHAR(255) NOT NULL,
  complaint_text TEXT NOT NULL,
  category VARCHAR(50),  -- Electricity, Water Supply, etc.
  department VARCHAR(100),
  priority VARCHAR(20),  -- High, Medium, Normal
  status VARCHAR(20) DEFAULT 'New',
  attachments TEXT,  -- JSON array of file paths
  assigned_to VARCHAR(120),
  resolution_notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  resolved_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Relationships
- User (1) → (Many) Complaint
- One user can have multiple complaints
- Complaints tracked by reference ID (GRV-xxxx-YYYY)

## 5. ML Classification System

### Algorithm
- **Vectorizer**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Classifier**: Multinomial Naïve Bayes
- **Categories**: 5 (Electricity, Water Supply, Sanitation, Roads, Public Services)

### Classification Flow
```
User Input Text
    ↓
Preprocessing (lowercase, tokenization)
    ↓
TF-IDF Vectorization
    ↓
Naïve Bayes Prediction
    ↓
Category + Department + Priority
    ↓
Response to Frontend
```

### Training Data
```python
training_texts = [
  "No electricity power outage",  # Electricity
  "Water contamination health hazard",  # Water Supply
  "Garbage waste management",  # Sanitation
  "Road pothole damage",  # Roads
  "Bus service delay"  # Public Services
]

categories = [
  "Electricity", "Water Supply", "Sanitation", "Roads", "Public Services"
]
```

### Priority Detection
- **High**: Keywords (urgent, emergency, critical) OR text length > 200 chars
- **Medium**: Text length > 100 chars
- **Normal**: Default

## 6. API Contract

### Request Flow
```
1. Frontend (React)
   ↓ HTTP POST/GET/PUT
2. Flask API
   ↓ Route Handler
3. Business Logic
   ↓ Process/Validate
4. Database (SQLAlchemy)
   ↓ Execute Query
5. Response
   ↓ JSON
6. Frontend
   ↓ Update UI
```

### Response Format
```json
{
  "success": true/false,
  "data": {...},
  "message": "...",
  "error": "..." (if failed)
}
```

## 7. Authentication Flow (Current & Future)

### Current (Basic)
```
User submits form
    ↓
Data sent to backend
    ↓
No authentication checked
    ↓
Process complaint
```

### Future (JWT)
```
User logs in
    ↓
Credentials validated
    ↓
JWT token generated and sent
    ↓
Token stored in localStorage
    ↓
Each request includes token in header
    ↓
Backend verifies token
    ↓
Process or reject request
```

## 8. Deployment Architecture

### Local Development
```
User Browser (localhost:5173)
         ↓ HTTP
    React Dev Server
         ↓
    npm run dev
         
Separate Terminal (localhost:5000)
         ↓
    Flask Dev Server
         ↓
    python app.py
         
SQLite Database (grievances.db)
```

### Docker Compose Production
```
┌─────────────────────────────────────┐
│      Docker Compose Network         │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   Frontend Container        │   │
│  │   (Node 18 + Vite build)    │   │
│  │   Port: 3000                │   │
│  └──────────┬────────────────┘   │
│             │                     │
│  ┌──────────▼──────────────────┐  │
│  │   Backend Container         │  │
│  │   (Python 3.11 + Flask)     │  │
│  │   Port: 5000                │  │
│  └──────────┬──────────────────┘  │
│             │                     │
│  ┌──────────▼──────────────────┐  │
│  │   Database Container        │  │
│  │   (PostgreSQL)              │  │
│  │   Port: 5432                │  │
│  │   Volume: db_data           │  │
│  └─────────────────────────────┘  │
│                                   │
└─────────────────────────────────────┘
```

### Services (docker-compose.yml)
1. **frontend**: Node 18 with npm, Vite build
2. **backend**: Python 3.11 with Flask
3. **db**: PostgreSQL 15

## 9. Notification System

### Email Notifications
```
User submits complaint
    ↓
Flask receives request
    ↓
Stores in database
    ↓
Calls send_confirmation_email()
    ↓
Flask-Mail + SMTP
    ↓
Email sent to user
```

### Future: SMS Notifications
```
User submits complaint
    ↓
Twilio API call (optional)
    ↓
SMS sent to phone number
```

## 10. Security Architecture

### Frontend Security
- Input validation (HTML5 + React)
- XSS prevention (React's built-in escaping)
- HTTPS only (production)

### Backend Security
- CORS protection
- Input validation (all fields)
- SQL injection prevention (SQLAlchemy ORM)
- Password hashing (Werkzeug)
- Environment-based secrets

### Database Security
- Parameterized queries (ORM)
- Indexes on query fields
- Foreign key constraints

## 11. Performance Optimization

### Frontend
- Code splitting (React Router lazy loading)
- CSS animations (GPU accelerated)
- Debounced search
- Pagination (for admin dashboard)

### Backend
- Database indexes
- Query optimization
- Caching (future)
- Database connection pooling

### Deployment
- Container image optimization
- Docker layer caching
- Environment-based configurations

## 12. Scalability Considerations

### Current Limitations
- Single Flask instance
- Single database
- No caching layer

### Future Improvements
- Load balancing (multiple Flask instances)
- Redis caching
- Database replication
- CDN for static files
- Message queue (Celery) for email

## 13. Monitoring & Logging

### Current
- Print statements for debugging
- Flask development mode

### Future
- Structured logging (JSON)
- Error tracking (Sentry)
- Performance monitoring
- Dashboard metrics

## 14. Testing Strategy

### Frontend Testing
- Unit tests (Jest)
- Integration tests (React Testing Library)
- E2E tests (Cypress)

### Backend Testing
- Unit tests (pytest)
- Integration tests
- Load testing

## 15. Disaster Recovery

### Backup Strategy
- Database backups (daily)
- Code backups (GitHub)
- Configuration backups (.env)

### Recovery Procedures
- Database restore from backup
- Code rollback from git
- Environment recreation from docker-compose

---

**Reference**: CivicFlow Grievance Hub System Design Document v1.0
