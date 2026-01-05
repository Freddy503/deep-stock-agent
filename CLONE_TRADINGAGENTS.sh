#!/bin/bash

# TradingAgents Clone Helper
# Run this script to clone TradingAgents and set it up

set -e

echo "=========================================="
echo "TradingAgents Clone & Setup"
echo "=========================================="
echo ""

# Check if already cloned
if [ -d "TradingAgents" ]; then
    echo "✓ TradingAgents already exists!"
    read -p "Do you want to re-clone? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping clone."
        exit 0
    fi
    echo "Removing old TradingAgents..."
    rm -rf TradingAgents
fi

# Clone TradingAgents
echo "📦 Cloning TradingAgents..."
git clone --depth 1 https://github.com/JosephTLucas/TradingAgents.git

if [ ! -d "TradingAgents" ]; then
    echo "❌ Failed to clone TradingAgents"
    echo ""
    echo "Please clone manually:"
    echo "  git clone https://github.com/JosephTLucas/TradingAgents.git"
    exit 1
fi

echo "✓ TradingAgents cloned successfully"

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv venv"
    exit 1
fi

source venv/bin/activate

# Install TradingAgents
echo ""
echo "📦 Installing TradingAgents..."
cd TradingAgents

if [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    pip install -e .
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️  No installation file found, skipping..."
fi

cd ..

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "TradingAgents is ready to use!"
echo ""
echo "Next steps:"
echo "1. Make sure Supabase schema is deployed (see RUN.md Step 2)"
echo "2. Run the app: ./START.sh"
echo ""
