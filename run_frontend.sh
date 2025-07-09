#!/bin/bash

# Startup script for AI Lending Research Agent Frontend

echo "🏦 Starting AI Lending Research Agent Frontend..."

# Load environment variables
if [ -f .env ]; then
    echo "Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  .env file not found. Some features may not work."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install frontend requirements
echo "Installing frontend requirements..."
pip install -r frontend_requirements.txt

# Install existing requirements if they exist
if [ -f requirements.txt ]; then
    echo "Installing existing requirements..."
    pip install -r requirements.txt
fi

# Check if MCP server is running
echo "Checking MCP server status..."
if ! pgrep -f "firecrawl-mcp" > /dev/null; then
    echo "⚠️  MCP server not running. Starting it..."
    cd firecrawl-mcp-server
    npm start &
    MCP_PID=$!
    cd ..
    echo "MCP server started with PID: $MCP_PID"
    sleep 3
else
    echo "✅ MCP server is already running"
fi

# Start Streamlit app
echo "🚀 Starting Streamlit frontend..."
echo "The app will be available at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"

streamlit run frontend_app.py --server.port 8501 --server.address 0.0.0.0

# Cleanup on exit
trap 'echo "Stopping services..."; kill $MCP_PID 2>/dev/null; exit' INT TERM EXIT