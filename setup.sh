#!/bin/bash

# CivicFlow Grievance Hub - Quick Setup Script
# This script sets up the development environment for CivicFlow

set -e  # Exit on any error

echo "🚀 CivicFlow Grievance Hub - Development Setup"
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Node.js is installed
echo -e "${BLUE}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Node.js not found. Please install Node.js 18+${NC}"
    echo "Visit: https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}✓ Node.js $(node -v)${NC}"

# Check if Python is installed
echo -e "${BLUE}Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python not found. Please install Python 3.11+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $(python3 --version)${NC}"

# Setup Frontend
echo -e "${BLUE}Setting up Frontend...${NC}"
npm install --legacy-peer-deps
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

# Setup Backend
echo -e "${BLUE}Setting up Backend...${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
source venv/bin/activate || . venv/Scripts/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}  Please edit backend/.env with your configuration${NC}"
fi

cd ..

# Create startup scripts
echo -e "${BLUE}Creating startup scripts...${NC}"

# Frontend start script
cat > start_frontend.sh << 'EOF'
#!/bin/bash
echo "Starting Frontend on http://localhost:5173..."
npm run dev
EOF
chmod +x start_frontend.sh

# Backend start script
cat > start_backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate || . venv/Scripts/activate
echo "Starting Backend on http://localhost:5000..."
python app.py
EOF
chmod +x start_backend.sh

echo -e "${GREEN}✓ Startup scripts created${NC}"

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${BLUE}To start development:${NC}"
echo ""
echo "1. Terminal 1 (Frontend):"
echo -e "   ${YELLOW}./start_frontend.sh${NC}"
echo ""
echo "2. Terminal 2 (Backend):"
echo -e "   ${YELLOW}./start_backend.sh${NC}"
echo ""
echo "3. Access application at:"
echo -e "   ${YELLOW}Frontend: http://localhost:5173${NC}"
echo -e "   ${YELLOW}Backend:  http://localhost:5000${NC}"
echo ""
echo "4. Or use Docker Compose:"
echo -e "   ${YELLOW}docker-compose up${NC}"
echo ""
