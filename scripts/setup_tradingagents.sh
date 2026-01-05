#!/bin/bash

# Setup script for TradingAgents integration
# This script clones the TradingAgents repository and sets it up

set -e  # Exit on error

echo "=========================================="
echo "TradingAgents Setup Script"
echo "=========================================="
echo ""

# Check if TradingAgents directory already exists
if [ -d "TradingAgents" ]; then
    echo "⚠️  TradingAgents directory already exists."
    read -p "Do you want to remove it and re-clone? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing TradingAgents directory..."
        rm -rf TradingAgents
    else
        echo "Keeping existing TradingAgents directory."
        exit 0
    fi
fi

# Clone TradingAgents repository
echo "📦 Cloning TradingAgents repository..."
git clone https://github.com/JosephTLucas/TradingAgents.git

if [ ! -d "TradingAgents" ]; then
    echo "❌ Failed to clone TradingAgents repository"
    exit 1
fi

echo "✅ TradingAgents cloned successfully"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install backend requirements
echo "📦 Installing backend requirements..."
pip install -r backend/requirements.txt

# Install TradingAgents dependencies
echo "📦 Installing TradingAgents dependencies..."
if [ -f "TradingAgents/requirements.txt" ]; then
    pip install -r TradingAgents/requirements.txt
elif [ -f "TradingAgents/pyproject.toml" ]; then
    cd TradingAgents
    pip install -e .
    cd ..
else
    echo "⚠️  Could not find TradingAgents requirements file"
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy backend/.env.example to backend/.env"
echo "2. Add your API keys to backend/.env:"
echo "   - GOOGLE_API_KEY (for Gemini)"
echo "   - ALPHA_VANTAGE_API_KEY"
echo "   - SUPABASE_URL and SUPABASE_KEY"
echo "3. Run the backend server:"
echo "   cd backend && python main.py"
echo ""
