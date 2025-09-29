#!/bin/bash

# Restaurant Management System Setup Script
# This script sets up the complete development environment

set -e

echo "Setting up Restaurant Management System..."
echo "============================================="

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Node.js is required but not installed."
    exit 1
fi

# Check MySQL
if ! command -v mysql &> /dev/null; then
    echo "MySQL is required but not installed."
    exit 1
fi

echo "All prerequisites found!"

# Setup Backend
echo ""
echo "Setting up Backend (Flask)..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Setup environment file if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env || cat > .env << EOF
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=mysql+pymysql://root:password@localhost/restaurant_db
EOF
    echo "Please update .env file with your MySQL credentials"
fi

echo "Backend setup complete!"

# Setup Frontend
echo ""
echo "Setting up Frontend (Vue.js)..."
cd ../frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

echo "Frontend setup complete!"

# Final instructions
echo ""
echo "Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Update backend/.env with your MySQL database credentials"
echo "2. Create the MySQL database:"
echo "   mysql> CREATE DATABASE restaurant_db;"
echo ""
echo "3. Start the backend server:"
echo "   cd backend && source venv/bin/activate && flask init-db && python run.py"
echo ""
echo "4. In a new terminal, start the frontend:"
echo "   cd frontend && npm run dev"
echo ""
echo "5. Open http://localhost:3000 in your browser"
echo "   Default login: admin / admin123"

