#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
    echo "✓ Environment variables loaded"
else
    echo "✗ .env file not found. Please create one with your API keys."
    exit 1
fi

# Check if FIRECRAWL_API_KEY is set
if [ -z "$FIRECRAWL_API_KEY" ]; then
    echo "✗ FIRECRAWL_API_KEY not found in .env file"
    echo "Please add FIRECRAWL_API_KEY=your_api_key to your .env file"
    exit 1
fi

echo "Starting Firecrawl MCP Server..."
echo "API Key: ${FIRECRAWL_API_KEY:0:10}..."  # Show first 10 chars for verification

# Change to firecrawl directory and start server
cd firecrawl-mcp-server

if [ ! -d "dist" ]; then
    echo "Building Firecrawl server..."
    npm run build
fi

echo "Starting server..."
npm start 