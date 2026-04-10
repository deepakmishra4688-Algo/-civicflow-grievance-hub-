# 📤 GitHub Deployment Guide

Complete guide to deploy CivicFlow Grievance Hub from your local machine to GitHub and then to production.

## Part 1: Push to GitHub

### Step 1: Create GitHub Repository

1. Go to **https://github.com/new**
2. Repository name: `civicflow-grievance-hub` (or your choice)
3. Description: "AI-powered citizen grievance management system"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README (we have one)
6. Click **Create repository**

### Step 2: Connect Local Repository to GitHub

```bash
# Navigate to project directory
cd "/home/deepak/Documents/BGI HACKTHON"

# Initialize git (if not already initialized)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: CivicFlow Grievance Hub with AI classification"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/civicflow-grievance-hub.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username**

### Step 3: Verify on GitHub

1. Go to your repository: `https://github.com/YOUR_USERNAME/civicflow-grievance-hub`
2. Refresh page
3. You should see all files and projects structure

### Step 4: Set Up GitHub Secrets (for CI/CD)

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - `DATABASE_URL`: Your database connection string
   - `SECRET_KEY`: Your Flask secret key
   - `MAIL_USERNAME`: Your Gmail address
   - `MAIL_PASSWORD`: Your Gmail app password

## Part 2: Deploy to Production

### Option 1: Vercel (Recommended for Frontend)

**Best for: Fast frontend deployment with free tier**

#### Frontend Only (Recommended)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Build for production:
```bash
npm run build
```

3. Deploy:
```bash
vercel
```

4. Follow prompts:
   - Link to GitHub repo? **Yes**
   - Choose production settings
   - Environment variables:
     - `REACT_APP_API_URL=https://your-backend-api.com/api`

**Your frontend will be live at:** `https://your-project.vercel.app`

### Option 2: Heroku (Backend + Simple Deployment)

**Best for: Full-stack quick deployment**

#### Prerequisites
```bash
# Install Heroku CLI
# macOS: brew tap heroku/brew && brew install heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login
```

#### Deploy Backend
```bash
# Create Heroku app
heroku create civicflow-backend

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set DATABASE_URL=postgresql://...
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Run migrations
heroku run "python -c 'from app import app, db; db.create_all()'"
```

**Your backend API will be at:** `https://civicflow-backend.herokuapp.com/api`

#### Deploy Frontend to Vercel with Backend URL
```bash
vercel env add REACT_APP_API_URL
# Enter: https://civicflow-backend.herokuapp.com/api

npm run build
vercel --prod
```

### Option 3: DigitalOcean App Platform (Full Stack)

**Best for: Complete control, reasonable pricing**

#### Step 1: Create Account
1. Go to **https://www.digitalocean.com**
2. Sign up / Log in
3. Create new project: "CivicFlow"

#### Step 2: Create App
1. Click **Create** → **App**
2. Connect to GitHub repository
3. Select your `civicflow-grievance-hub` repository
4. Choose branch: `main`

#### Step 3: Configure Services
1. **Frontend:**
   - Source: `src/` folder (or automatic detection)
   - Build command: `npm install && npm run build`
   - Output directory: `dist/`
   - HTTP port: `3000`

2. **Backend:**
   - Source: `backend/` folder
   - Build command: `pip install -r requirements.txt`
   - Run command: `python app.py`
   - HTTP port: `5000`

3. **Database:**
   - Add PostgreSQL database
   - Set `DATABASE_URL` environment variable

#### Step 4: Environment Variables
Set these in App settings:
```
DATABASE_URL=postgresql://user:pass@host/db
FLASK_ENV=production
SECRET_KEY=your-secret-key
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-app-password
REACT_APP_API_URL=https://your-backend-url/api
```

#### Step 5: Deploy
1. Click **Create App**
2. DigitalOcean will automatically:
   - Build your app
   - Run tests
   - Deploy to production
   - Assign domain

**Your app will be at:** `https://your-project.ondigitalocean.app`

### Option 4: AWS (Enterprise Grade)

**Best for: Scalability, high traffic, enterprise needs**

#### Infrastructure Diagram
```
┌──────────────────────────────────────────────────────┐
│              CloudFront (CDN)                         │
└────────────────────┬─────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
    ┌───▼──────┐          ┌──────▼──────┐
    │  S3 (UI) │          │   ALB       │
    │ Static   │          │ (Backend)   │
    │  Assets  │          │             │
    └──────────┘          └──────┬───────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                ┌───▼──┐    ┌───▼──┐    ┌──▼────┐
                │ EC2  │    │ EC2  │    │ EC2   │
                │ ASG  │    │ ASG  │    │ ASG   │
                └──────┘    └──────┘    └───────┘
                         │
                    ┌────▼──────┐
                    │  RDS      │
                    │PostgreSQL │
                    └───────────┘
```

#### Deployment Steps

1. **Create S3 Bucket for Frontend:**
```bash
aws s3api create-bucket \
  --bucket civicflow-frontend \
  --region us-east-1

# Build and upload
npm run build
aws s3 sync dist/ s3://civicflow-frontend/

# Make public
aws s3api put-bucket-policy \
  --bucket civicflow-frontend \
  --policy '{...}'
```

2. **Create RDS Database:**
```bash
aws rds create-db-instance \
  --db-instance-identifier civicflow-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --allocated-storage 20
```

3. **Deploy Backend on EC2:**
```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@your-instance-ip

# Clone repository
git clone https://github.com/YOUR_USERNAME/civicflow-grievance-hub.git

# Setup backend
cd civicflow-grievance-hub/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn

# Start in background
nohup gunicorn -w 4 -b 0.0.0.0:5000 app:app &
```

4. **Setup CloudFront CDN:**
```bash
aws cloudfront create-distribution \
  --origin-domain-name civicflow-frontend.s3.amazonaws.com \
  --default-root-object index.html
```

## Part 3: Domain & SSL

### Assign Custom Domain

#### Using Heroku/DigitalOcean/Vercel (Free SSL)
```bash
# Heroku
heroku domains:add civicflow.com

# Verify DNS
heroku domains:wait civicflow.com
```

#### Using AWS Route 53
1. Go to Route 53 → Hosted zones
2. Create hosted zone for your domain
3. Add A record pointing to your CloudFront distribution
4. AWS automatically provisions SSL certificate

### Enable Auto-Renewal
- Most platforms auto-renew SSL certificates
- Verify in settings/certificates section

## Part 4: Monitoring & Maintenance

### Monitor Performance
```bash
# Heroku
heroku logs --tail
heroku ps:scale web=2:standard-2x

# Vercel
# Dashboard: vercel.com/dashboard

# DigitalOcean
# Go to: Insights/Metrics
```

### Backup Database
```bash
# Weekly backup for Heroku
heroku pg:backups:schedule --at "02:00 UTC"

# Manual backup
heroku pg:backups:capture
heroku pg:backups:url
wget $(heroku pg:backups:url)
```

### Monitor Uptime
1. Use UptimeRobot (free account)
2. Set to ping your API every 5 minutes
3. Get alerts if service goes down

## Part 5: CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: civicflow-backend
          
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

## Part 6: Testing Before Deployment

### Checklist

- [ ] All tests pass: `npm test`, `pytest`
- [ ] No console errors in browser (F12)
- [ ] Backend health check passes
- [ ] ML classifier works
- [ ] Form submission works
- [ ] Admin dashboard loads
- [ ] Responsive design works on mobile (test at 480px, 768px, 1024px)
- [ ] Dark mode works
- [ ] Email notification configured
- [ ] Database migrations pass
- [ ] Environment variables set correctly

### Load Testing
```bash
# Install Apache Bench
# macOS: brew install httpd
# Linux: sudo apt-get install apache2-utils

# Test backend
ab -n 1000 -c 100 http://localhost:5000/api/health

# Test frontend
ab -n 1000 -c 100 http://localhost:5173
```

## Part 7: Troubleshooting

### App won't deploy
```bash
# Check build logs
vercel logs
heroku logs --tail

# Verify environment variables
heroku config
```

### Database connection error
```bash
# Check DATABASE_URL
heroku config | grep DATABASE_URL

# Verify database is running
heroku pg:info
```

### Slow performance
```bash
# Check memory usage
heroku ps

# Scale if needed
heroku ps:scale web=2:standard-2x

# Check logs for slow queries
heroku logs --tail | grep -i slow
```

### CORS error
```python
# Update in backend/app.py
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com", "https://www.yourdomain.com"]
    }
})
```

## Part 8: Post-Deployment Tasks

### Update Dashboard
1. Go to **Settings** → **Custom Domain**
2. Update `REACT_APP_API_URL` in frontend
3. Redeploy frontend

### Monitor Errors
1. Use Sentry for error tracking:
```bash
npm install @sentry/react
```

2. Monitor database performance

3. Set up alerts for downtime

### Version Control
```bash
# Tag releases
git tag v1.0.0
git push origin v1.0.0

# Create GitHub release
# Go to Releases → Create new release with notes
```

## 🎉 Done!

Your CivicFlow Grievance Hub is now live!

### URLs
- **Frontend:** https://your-domain.com
- **Backend API:** https://your-backend-domain.com/api
- **Admin Dashboard:** https://your-domain.com/admin
- **API Documentation:** https://your-backend-domain.com/api/docs

### Next Steps
1. Share with users
2. Monitor analytics
3. Gather feedback
4. Plan improvements
5. Scale infrastructure as needed

---

**Happy deploying! 🚀**
