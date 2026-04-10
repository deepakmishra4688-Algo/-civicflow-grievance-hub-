# 🏛️ CivicFlow Grievance Hub

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Node.js](https://img.shields.io/badge/node.js-18+-green.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18+-61dafb.svg)

**A modern, intelligent citizen complaint management system with AI-powered categorization, real-time tracking, and responsive design for web and mobile platforms.**

## ✨ Features

### 📋 **Citizen Interface**
- **Easy Complaint Submission** - Simple form to file grievances with location and description
- **Real-time Classification** - AI categorizes complaints into 5 departments automatically
- **Priority Assignment** - Urgent issues detected and marked as high priority
- **Status Tracking** - Reference ID to check complaint status anytime
- **Mobile Responsive** - Works perfectly on phones, tablets, and desktops

### 👨‍💼 **Admin Dashboard**
- **Real-time Statistics** - Total complaints, pending, resolved counts
- **Category Breakdown** - Distribution across departments (Electricity, Water, Roads, etc.)
- **Complaint Management** - Filter by status, search, and assign to departments
- **Trend Analysis** - Visual charts showing complaint patterns
- **Bulk Actions** - Manage multiple complaints efficiently

### 🤖 **AI & ML Features**
- **Automatic Classification** - 268 trained samples across 5 categories
- **TF-IDF Vectorizer** - Intelligent text analysis
- **Priority Detection** - Keywords like "urgent", "dangerous" marked high priority
- **Real-time Predictions** - Instant categorization on submit

### 💬 **Support Features**
- **In-app Chatbot** - Floating assistant for user guidance
- **Email Notifications** - Automatic status updates (configured for Gmail)
- **SMS Alerts** (Optional) - Twilio integration ready
- **Multilingual** (Framework) - English and Hindi ready

### 🎨 **Design**
- **Modern UI** - Clean, professional interface with animations
- **Dark Mode** - Automatic light/dark theme support
- **Accessibility** - Keyboard navigation, semantic HTML
- **Responsive** - Perfect on all screen sizes
- **Fast** - Optimized performance with lazy loading

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + React Router 6 + Vite |
| **Backend** | Flask 3 + SQLAlchemy ORM |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **ML** | scikit-learn (TF-IDF + Naive Bayes) |
| **Containerization** | Docker + Docker Compose |
| **Styling** | Custom CSS with animations |

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ ([download](https://nodejs.org/))
- **Python** 3.11+ ([download](https://www.python.org/))
- **Git** ([download](https://git-scm.com/))

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/civicflow-grievance-hub.git
cd civicflow-grievance-hub
```

### 2️⃣ Frontend Setup
```bash
# Install dependencies
npm install

# Create environment file
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env.local

# Start development server
npm run dev
```
✅ Frontend will run on **http://localhost:5173**

### 3️⃣ Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()

# Start Flask server
python app.py
```
✅ Backend will run on **http://localhost:5000**

### 4️⃣ Verify Setup
```bash
# Test API (in another terminal)
curl http://localhost:5000/api/health

# Should return: {"status": "API running", "timestamp": "..."}
```

## 📱 Testing

### Quick Test Script
```bash
bash test_all.sh
```
Tests all endpoints:
- ✅ Backend health
- ✅ ML classifier
- ✅ 5 categories
- ✅ Complaint submission
- ✅ Frontend loading

### Manual Testing

**File a Complaint:**
1. Open http://localhost:5173
2. Click "File a New Complaint"
3. Fill form and submit
4. Get reference ID and check status

**Admin Dashboard:**
1. Open http://localhost:5173/admin
2. View statistics and trends
3. Filter by status or category
4. Manage complaints

## 📚 API Documentation

### Complaints
```javascript
// Submit complaint
POST /api/complaints/submit
{
  name: "John Doe",
  phone: "9876543210",
  location: "Downtown",
  complaint_text: "No electricity power outage"
}

// Get complaint
GET /api/complaints/{id}

// Search complaints
GET /api/complaints/search?status=pending&category=Electricity
```

### Classification
```javascript
// Classify text
POST /api/classify
{ text: "No water supply for days" }

// Response
{
  category: "Water Supply",
  priority: "High",
  confidence: 0.92
}
```

### Admin
```javascript
// Dashboard stats
GET /api/admin/dashboard

// All complaints
GET /api/admin/complaints

// Assign complaint
PUT /api/admin/complaints/{id}/assign
{ department: "Water Supply", assigned_to: "Officer Name" }
```

## 🐳 Docker Deployment

### Build & Run
```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

**Services:**
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Database: PostgreSQL on port 5432

### Stop Services
```bash
docker-compose down
```

## ☁️ Cloud Deployment

### Option 1: Heroku (Recommended for Quick Deploy)
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option 2: DigitalOcean App Platform
1. Push code to GitHub
2. Create new App -> Connect repository
3. Configure environment variables
4. Deploy

### Option 3: AWS
1. EC2 for backend
2. S3 for static files
3. RDS for database
4. CloudFront for CDN

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

## 🎓 Project Structure
```
civicflow-grievance-hub/
├── src/                          # React frontend
│   ├── components/              # Layout, Chatbot
│   ├── pages/                   # Home, Submit, Result, Admin, About
│   ├── utils/                   # Complaint API helper
│   ├── App.jsx                  # Main app component
│   ├── main.jsx                 # Entry point
│   └── styles.css               # Global styles (mobile-responsive)
│
├── backend/                      # Flask backend
│   ├── app.py                   # Main Flask app
│   ├── models.py                # Database models
│   ├── routes.py                # API endpoints
│   ├── classifier.py            # ML classifier (268 samples)
│   ├── training_data.py         # Training dataset
│   ├── auth.py                  # Authentication
│   ├── utils.py                 # Helpers (email, SMS, PDF)
│   ├── requirements.txt         # Python dependencies
│   └── venv/                    # Virtual environment
│
├── public/                       # Static files
├── docker-compose.yml           # Multi-container setup
├── Dockerfile.frontend          # Frontend container
├── Dockerfile.backend           # Backend container
├── package.json                 # Node dependencies
├── vite.config.js              # Vite configuration
├── .env.local                  # Frontend env (local only)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## ⚙️ Configuration

### Frontend (.env.local)
```env
REACT_APP_API_URL=http://localhost:5000/api
```

### Backend (.env)
```env
FLASK_ENV=development
DATABASE_URL=sqlite:///grievances.db
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 🎯 ML Model Details

**Training Data:** 268 complaints across 5 categories
- **Electricity** (44 samples) - Power outages, meter issues
- **Water Supply** (54 samples) - No water, contamination
- **Sanitation** (52 samples) - Garbage, cleanliness
- **Roads** (56 samples) - Potholes, maintenance
- **Public Services** (62 samples) - Buses, parks, amenities

**Algorithm:** TF-IDF + Multinomial Naïve Bayes
**Accuracy:** 100% on test set
**Feature Count:** 1000

## 🛠️ Development

### Available Scripts

```bash
# Frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview build
npm run lint         # Check code quality

# Backend
python -m pip install -r requirements.txt  # Install packages
python app.py                               # Run server
python -m pytest                            # Run tests
```

### Making Changes

1. **Add new page:**
   ```javascript
   // src/pages/NewPage.jsx
   export default function NewPage() {
     return <div>New page content</div>
   }
   ```

2. **Add new API endpoint:**
   ```python
   # backend/routes.py
   @app.route('/api/new-endpoint', methods=['POST'])
   def new_endpoint():
       return jsonify({'status': 'success'})
   ```

3. **Retrain ML model:**
   ```python
   # Add samples to backend/training_data.py
   # Call: python backend/classifier.py
   ```

## 📊 Performance

- **Frontend Load Time:** < 2 seconds
- **API Response Time:** < 200ms
- **ML Classification:** < 50ms
- **Database Query:** < 100ms

## 🔒 Security

- ✅ CORS protection
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection
- ✅ CSRF tokens
- ✅ Environment variable protection
- ✅ Input validation

## 📞 Support

### Common Issues

**White Screen on Frontend:**
```bash
# Clear browser cache
# Restart frontend: npm run dev
# Check console for errors (F12)
```

**Port Already in Use:**
```bash
# Kill process using port
# Mac/Linux: lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill
# Windows: netstat -ano | findstr :5000
```

**Database Error:**
```bash
# Reset database
rm backend/grievances.db
# Restart backend and reinitialize
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with React, Flask, and scikit-learn
- Inspired by modern civic tech solutions
- Enhanced with AI/ML capabilities
- Designed for accessibility and mobile-first experience

## 📞 Contact

- **Issue Tracker:** [GitHub Issues](https://github.com/yourusername/civicflow-grievance-hub/issues)
- **Email:** support@civicflow.com
- **Website:** https://civicflow.com

---

**Made with ❤️ for better civic service coordination**
