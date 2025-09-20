#!/bin/bash
# VulnGuard Security Scanning Agent
# Auto-generated wrapper script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Install required dependencies if needed
DEPS_INSTALLED=false
if ! python3 -c "import requests, psutil" &> /dev/null; then
    echo "📦 Installing required dependencies..."
    python3 -m pip install --quiet requests psutil pymongo fastapi uvicorn motor python-dotenv pydantic python-multipart 2>/dev/null || {
        echo "⚠️  Could not install dependencies automatically."
        echo "Please run: pip3 install requests psutil pymongo fastapi uvicorn motor python-dotenv pydantic python-multipart"
    }
    DEPS_INSTALLED=true
fi

# Run the Python script with all arguments
cd "$SCRIPT_DIR"
python3 "vulnguard_agent.py" "$@"
