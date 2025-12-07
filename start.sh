#!/bin/bash
# Startup script for Network Monitoring Tool

echo "=========================================="
echo "Network Performance Monitoring Tool"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    exit 1
fi

echo "Starting backend server..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Create logs directory if it doesn't exist
mkdir -p ../logs

# Start backend in background
echo "Backend server starting at http://localhost:5000"
python app.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid

cd ..

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 3

echo "Starting frontend server..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Start frontend
echo "Frontend server starting at http://localhost:5173"
npm run dev

# Cleanup function
cleanup() {
    echo ""
    echo "Shutting down servers..."
    if [ -f logs/backend.pid ]; then
        kill $(cat logs/backend.pid) 2>/dev/null
        rm logs/backend.pid
    fi
    exit 0
}

trap cleanup SIGINT SIGTERM

wait
