# CivicFlow Troubleshooting Guide

## Common Issues & Solutions

### Frontend Issues

#### 1. npm install fails
**Error**: `npm ERR! peer dep missing`

**Solution**:
```bash
npm install --legacy-peer-deps
# or
npm install --force
```

**Cause**: Conflicting peer dependencies in React/React Router

---

#### 2. Port 3000 already in use
**Error**: `Error: listen EADDRINUSE: address already in use :::3000`

**Solution**:
```bash
# Kill process on port 3000
lsof -i :3000
kill -9 <PID>

# Or use a different port
npm run dev -- --port 3001
```

**Alternative (Windows)**:
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

---

#### 3. API calls return 404
**Error**: `Failed to fetch: 404 Not Found`

**Solution**: 
1. Check backend is running on port 5000
2. Verify API URL in code matches backend URL
3. Check CORS is enabled in backend (app.py)

```javascript
// In complaints.js, verify:
const API_BASE_URL = 'http://localhost:5000/api';
```

---

#### 4. CORS Error
**Error**: `Access to XMLHttpRequest has been blocked by CORS policy`

**Solution**: Backend CORS is not configured

**Fix in backend/app.py**:
```python
from flask_cors import CORS

CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:3001"
])
```

---

#### 5. CSS not loading / Styles not applied
**Error**: Page appears unstyled

**Solution**:
```bash
# Clear cache and rebuild
rm -rf node_modules dist
npm install --legacy-peer-deps
npm run build
npm run dev
```

**Also check**: Vite CSS import in `src/main.jsx`
```javascript
import './styles.css'
```

---

#### 6. Components not updating after API call
**Error**: Data fetched but component doesn't update

**Solution**: Check useEffect hook:
```javascript
useEffect(() => {
  const fetchData = async () => {
    const data = await getDashboardStats();
    setStats(data);  // Must call setState!
  };
  fetchData();
}, []);  // Empty dependency array for mount only
```

---

### Backend Issues

#### 1. Port 5000 already in use
**Error**: `Address already in use`

**Solution**:
```bash
# Find and kill process
lsof -i :5000
kill -9 <PID>

# Or use different port
FLASK_ENV=development FLASK_PORT=5001 python app.py
```

---

#### 2. ModuleNotFoundError import errors
**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
1. Create and activate virtual environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Verify Python path
```bash
which python  # Show active Python
python -m pip --version  # Verify pip
```

---

#### 3. Database connection error
**Error**: `sqlite3.OperationalError: unable to open database file`

**Solution**:
```bash
# Check .env file has DATABASE_URL
cat backend/.env

# Create database directory
mkdir -p backend

# Reset database
rm backend/grievances.db

# Recreate on startup
python app.py
```

---

#### 4. Flask app not starting
**Error**: `ModuleNotFoundError` or app won't start

**Solution**:
1. Check Python version
```bash
python --version  # Should be 3.11+
```

2. Verify requirements installed
```bash
pip list | grep -i flask
```

3. Check app.py exists and has no syntax errors
```bash
python -m py_compile app.py
```

4. Start with debug output
```bash
FLASK_ENV=development python app.py
```

---

#### 5. Email not sending
**Error**: `SMTPAuthenticationError` or emails don't arrive

**Solution**: Check .env credentials
```bash
# In backend/.env:
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password  # Not your account password!
```

**Gmail**: 
1. Enable 2-factor authentication
2. Generate app-specific password
3. Use that password in .env

---

#### 6. ML Classifier not working
**Error**: `ValueError: y should be a 1d array` or classifier errors

**Solution**:
```python
# In classifier.py, verify training data format:
training_texts = [...]  # List of strings
training_labels = [...]  # List of category strings

# Check lengths match
assert len(training_texts) == len(training_labels)
```

---

#### 7. Import order errors
**Error**: `AttributeError: 'NoneType' object has no attribute 'Column'`

**Solution**: Models imported before db initialization

**Fix in app.py**:
```python
# ✓ Correct order:
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

# Import models AFTER db initialization
from models import User, Complaint

# Register blueprints
app.register_blueprint(routes.complaints_bp)
```

---

### Database Issues

#### 1. Database locked
**Error**: `database is locked`

**Solution**:
```bash
# Kill all Python processes
pkill python

# Reset database
rm backend/grievances.db

# Restart
python app.py
```

---

#### 2. Migrations not working
**Error**: Schema mismatch

**Solution**: Use raw schema recreation
```python
from app import app, db

with app.app_context():
    db.drop_all()  # Warning: deletes all data
    db.create_all()
    print("Database created")
```

---

### Docker Issues

#### 1. Container won't start
**Error**: `docker-compose up` fails

**Solution**:
```bash
# View detailed logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild images
docker-compose build --no-cache

# Start with verbose output
docker-compose up --verbose
```

---

#### 2. Port conflicts in Docker
**Error**: `port is already allocated`

**Solution**:
```bash
# Stop all containers
docker-compose down

# List running containers
docker ps

# Remove specific container
docker rm <container_id>

# Or change port in docker-compose.yml:
ports:
  - "3001:3000"  # Use 3001 instead of 3000
```

---

#### 3. Database not persisting
**Error**: Data lost after docker-compose down

**Solution**: Ensure volume is mounted

**Check docker-compose.yml**:
```yaml
services:
  db:
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

---

#### 4. Frontend can't reach backend in Docker
**Error**: `Failed to fetch http://localhost:5000/api`

**Solution**: Use service name instead of localhost

**In frontend .env inside Docker**:
```
REACT_APP_API_URL=http://backend:5000/api
```

**But for local development**:
```
REACT_APP_API_URL=http://localhost:5000/api
```

---

### API Issues

#### 1. 405 Method Not Allowed
**Error**: `405 Method Not Allowed`

**Solution**: Check HTTP method matches endpoint

```python
# ✓ POST endpoint
@app.route('/api/complaints/submit', methods=['POST'])
def submit():
    pass

# ✗ Calling with GET will fail
# curl http://localhost:5000/api/complaints/submit  # Wrong!
# curl -X POST http://localhost:5000/api/complaints/submit  # Correct!
```

---

#### 2. 500 Internal Server Error
**Error**: `500 Internal Server Error`

**Solution**: Check backend logs
```bash
# View console output for errors
# Look for stack trace in terminal running `python app.py`

# Enable debug mode:
FLASK_ENV=development python app.py
```

---

#### 3. JSON parsing error
**Error**: `JSON.parse error` or `BadRequest`

**Solution**: Verify request format
```javascript
// ✓ Correct
fetch('/api/endpoint', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ field: value })
})

// ✗ Wrong
fetch('/api/endpoint', {
  method: 'POST',
  body: { field: value }  // Not JSON!
})
```

---

#### 4. CORS preflight request fails
**Error**: `OPTIONS /api/endpoint 403 Forbidden`

**Solution**: CORS configuration incomplete

**In backend app.py**:
```python
from flask_cors import CORS
CORS(app, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
```

---

### Performance Issues

#### 1. Slow API responses
**Symptoms**: Requests take >1 second

**Solutions**:
```python
# Add database query optimization
from sqlalchemy import select
complaints = db.session.execute(
    select(Complaint).limit(10).offset(0)
).scalars().all()

# Use pagination
page = request.args.get('page', 1, type=int)
per_page = request.args.get('per_page', 20, type=int)
```

---

#### 2. Complaints list takes forever to load
**Symptoms**: Admin dashboard hangs with many complaints

**Solution**: Add pagination & filtering

```python
@complaints_bp.route('/search', methods=['GET'])
def search():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    
    query = Complaint.query
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'complaints': [c.to_dict() for c in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages
    })
```

---

### Deployment Issues

#### 1. Heroku deployment fails
**Error**: Build or deploy errors

**Solution**:
```bash
# Check logs
heroku logs --tail

# Verify Procfile exists
echo "web: gunicorn app:app" > Procfile

# Add buildpacks
heroku buildpacks:add heroku/python
heroku buildpacks:add heroku/nodejs

# Set environment variables
heroku config:set DATABASE_URL=postgresql://...
```

---

#### 2. AWS deployment env vars not set
**Error**: Missing DATABASE_URL or other vars

**Solution**:
- Add to EC2 instance environment
- Or update `.env` on server
- Or use parameter store

```bash
export DATABASE_URL=postgresql://...
export FLASK_ENV=production
python app.py
```

---

### Debugging Tips

#### 1. Enable Flask Debug Mode
```bash
FLASK_ENV=development python app.py
```

#### 2. Add logging to backend
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@complaints_bp.route('/submit', methods=['POST'])
def submit():
    logger.debug(f"Received data: {request.json}")
    # ...
```

#### 3. Debug API calls in frontend
```javascript
// Add to complaints.js
const response = await fetch(url, options);
console.log('API Response:', response);
const data = await response.json();
console.log('Data:', data);
```

#### 4. Check network in browser
1. Open DevTools (F12)
2. Go to Network tab
3. Make API call
4. Check request/response headers and body

#### 5. Test API with curl
```bash
# Test health
curl http://localhost:5000/api/health

# Test submit
curl -X POST http://localhost:5000/api/complaints/submit \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","phone":"123","location":"City","complaint_text":"Test"}'

# Check response
curl -v http://localhost:5000/api/complaints/1
```

---

### Getting Help

1. **Check logs**
   - Browser console (F12)
   - Backend terminal output
   - Docker logs (`docker-compose logs`)

2. **Search error message**
   - Google the exact error
   - Check Stack Overflow
   - Review documentation

3. **Simplify to reproduce**
   - Minimal code example
   - Known working data input
   - Check one thing at a time

4. **Ask for help**
   - Share error stack trace
   - Describe what you did
   - Mention what you expected
   - Include steps to reproduce

---

**Last Updated**: 2024
**Version**: 1.0.0
