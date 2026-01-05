#!/bin/bash

# TradingAgents Portfolio Monitor - Quick Start Script

echo "=========================================="
echo "TradingAgents Portfolio Monitor"
echo "=========================================="
echo ""

# Check if TradingAgents exists
if [ ! -d "TradingAgents" ]; then
    echo "⚠️  TradingAgents not found!"
    echo "Please clone it first:"
    echo "  git clone https://github.com/JosephTLucas/TradingAgents.git"
    echo ""
fi

# Check environment files
if ! grep -q "your_gemini_api_key" backend/.env 2>/dev/null; then
    echo "✓ Backend environment configured"
else
    echo "⚠️  Please add your API keys to backend/.env"
fi

echo ""
echo "Choose how to start:"
echo "1. Backend only"
echo "2. Frontend only"
echo "3. Both (in background)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "Starting backend..."
        source venv/bin/activate
        cd backend
        python main.py
        ;;
    2)
        echo "Starting frontend..."
        cd frontend
        npm run dev
        ;;
    3)
        echo "Starting both services..."
        echo "Backend: http://localhost:8000"
        echo "Frontend: http://localhost:3000"
        echo ""
        
        # Start backend in background
        source venv/bin/activate
        cd backend
        python main.py > ../backend.log 2>&1 &
        BACKEND_PID=$!
        cd ..
        
        # Start frontend in background
        cd frontend
        npm run dev > ../frontend.log 2>&1 &
        FRONTEND_PID=$!
        
        echo "✓ Services started!"
        echo "  Backend PID: $BACKEND_PID"
        echo "  Frontend PID: $FRONTEND_PID"
        echo ""
        echo "To stop:"
        echo "  kill $BACKEND_PID $FRONTEND_PID"
        echo ""
        echo "Logs:"
        echo "  Backend: tail -f backend.log"
        echo "  Frontend: tail -f frontend.log"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
