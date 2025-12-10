#!/bin/bash
set -e

echo "🧠 Second Brain Assistant - Quick Start Setup"
echo "=============================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start Neo4j
echo "📦 Starting Neo4j database..."
docker-compose up -d
echo "✅ Neo4j is running on http://localhost:7474"
echo ""

# Setup Backend
echo "🐍 Setting up Python backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Setup .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your OPENAI_API_KEY"
    echo ""
fi

cd ..

# Setup Frontend
echo "⚛️  Setting up React frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install --silent

# Setup .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Add your OpenAI API key to backend/.env"
echo "   2. Start the backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   3. Start the frontend: cd frontend && npm run dev"
echo "   4. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For more information, see README.md"
