#!/bin/bash

# CivicFlow Quick Setup Script
# Run this after git clone to get up and running in 2 minutes

set -e

echo "🚀 CivicFlow Grievance Hub - Quick Setup"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Step 1: Frontend Setup
echo -e "${BLUE}Step 1: Frontend Setup${NC}"
echo "Installing Node dependencies..."
npm install --legacy-peer-deps
echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
echo ""

# Step 2: Backend Setup  
echo -e "${BLUE}Step 2: Backend Setup${NC}"
cd backend
echo "Creating Python virtual environment..."
python -m venv venv
source venv/bin/activate
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo -e "${GREEN}✅ Backend dependencies installed${NC}"
echo ""

# Step 3: Database Setup
echo -e "${BLUE}Step 3: Database Setup${NC}"
echo "Initializing database..."
python -c "
from app import app, db
with app.app_context():
    db.create_all()
print('✅ Database initialized')
"
echo ""

# Step 4: Instructions
echo -e "${BLUE}Quick Start Instructions${NC}"
echo "=========================="
echo ""
echo -e "${YELLOW}Terminal 1 - Frontend:${NC}"
echo "  cd /path/to/civicflow-grievance-hub"
echo "  npm run dev"
echo "  🌐 Open: http://localhost:5173"
echo ""
echo -e "${YELLOW}Terminal 2 - Backend:${NC}"
echo "  cd /path/to/civicflow-grievance-hub/backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo "  🔌 API: http://localhost:5000/api"
echo ""
echo -e "${YELLOW}Terminal 3 - Test:${NC}"
echo "  bash test_all.sh"
echo ""
echo -e "${GREEN}Setup Complete! ✅${NC}"
echo ""
echo "📚 Documentation:"
echo "  • README.md - Full documentation"
echo "  • GITHUB_READY.md - GitHub & deployment guide"
echo "  • API.md - API endpoints"
echo "  • DEPLOYMENT.md - Deployment options"
echo ""
echo "🎯 Next: Open http://localhost:5173 after starting servers"
