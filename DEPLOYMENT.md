# CivicFlow Grievance Hub - Setup & Deployment Guide

## Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose (optional)
- PostgreSQL (optional, SQLite by default)

## Local Development Setup

### 1. Frontend Setup
```bash
cd '/home/deepak/Documents/BGI HACKTHON'

# Install dependencies
npm install --legacy-peer-deps

# Create .env file
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env.local

# Start development server
npm run dev
```
Frontend will be available at `http://localhost:5173`

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()

# Run backend
python app.py
```
Backend API will be available at `http://localhost:5000/api`

### 3. Health Check
```bash
curl http://localhost:5000/api/health
```

## Deployment with Docker

### Build & Run
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Database: postgres://admin:admin123@db:5432/civicflow

## Features Implemented

### ✅ Core Features
- Multi-page React app (Home, Submit, Result, Admin, About)
- Flask REST API backend
- SQLAlchemy database models
- User authentication
- Complaint classification with ML

### ✅ Advanced Features
- Dashboard with statistics
- Status filters and search
- Email notifications
- Multilingual support (English, Hindi)
- Responsive design with dark mode
- Animations and transitions
- Docker containerization

### ✅ API Endpoints

**Complaints:**
- POST `/api/complaints/submit` - Submit complaint
- GET `/api/complaints/<id>` - Get complaint
- GET `/api/complaints/<ref_id>` - Get by reference
- PUT `/api/complaints/<id>` - Update complaint
- GET `/api/complaints/search` - Search with filters

**Admin:**
- GET `/api/admin/dashboard` - Dashboard stats
- GET `/api/admin/complaints` - All complaints
- PUT `/api/admin/complaints/<id>/assign` - Assign complaint

**Auth:**
- POST `/api/auth/register` - Register user
- POST `/api/auth/login` - Login user

**Classification:**
- POST `/api/classify` - Classify complaint text

## Environment Configuration

### Backend (.env)
```
DATABASE_URL=sqlite:///grievances.db
FLASK_ENV=development
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Frontend (.env.local)
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Deployment to Production

### Option 1: Heroku
```bash
heroku create civicflow-grievance-hub
git push heroku main
heroku config:set FLASK_ENV=production
```

### Option 2: AWS
1. Create EC2 instance
2. Setup RDS for PostgreSQL
3. Deploy using Docker
4. Setup CloudFront CDN

### Option 3: DigitalOcean
1. Create App Platform app
2. Connect GitHub repository
3. Configure environment variables
4. Deploy

## Testing

```bash
# Test API
curl -X POST http://localhost:5000/api/complaints/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "9876543210",
    "location": "Downtown",
    "complaint_text": "No electricity power outage"
  }'

# Build frontend for production
npm run build

# Preview production build
npm run preview
```

## Troubleshooting

**Port already in use:**
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

**Database error:**
```bash
# Reset database
rm backend/grievances.db
python backend/app.py
```

**CORS error:**
- Ensure backend CORS is configured
- Check API URL in frontend .env

## Next Steps

1. Add SMS notifications (Twilio integration)
2. Implement real ML model
3. Add image upload to cloud storage
4. Create mobile app
5. Setup CI/CD pipeline
6. Add payment gateway for fees

## Support

For issues or questions, refer to the documentation or create an issue in the repository.
