#!/bin/bash
# VulnGuard Command Line Interface
# VulnGuard Security Platform v2.0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    echo "Please install Python 3.8+ and try again:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
REQUIRED_VERSION="3.8"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${GREEN}✅ Python ${PYTHON_VERSION} detected${NC}"
else
    echo -e "${RED}❌ Python ${PYTHON_VERSION} detected, but 3.8+ required${NC}"
    exit 1
fi

# Install dependencies if needed
echo -e "${YELLOW}📦 Checking dependencies...${NC}"
if ! python3 -c "import requests, psutil" &> /dev/null; then
    echo -e "${YELLOW}Installing required packages...${NC}"
    
    # Try different installation methods
    if python3 -m pip install --quiet --user requests psutil pymongo fastapi uvicorn motor python-dotenv pydantic python-multipart 2>/dev/null; then
        echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
    else
        echo -e "${YELLOW}⚠️  Standard installation failed, trying alternative method...${NC}"
        if python3 -m pip install --quiet --break-system-packages requests psutil pymongo fastapi uvicorn motor python-dotenv pydantic python-multipart 2>/dev/null; then
            echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
        else
            echo -e "${RED}❌ Could not install dependencies automatically.${NC}"
            echo "Please run manually:"
            echo "  pip3 install requests psutil pymongo fastapi uvicorn motor python-dotenv pydantic python-multipart"
            echo "Or:"
            echo "  python3 -m pip install --user requests psutil pymongo fastapi uvicorn motor python-dotenv pydantic"
            exit 1
        fi
    fi
fi

# Run the Python script with all arguments
cd "$SCRIPT_DIR"
python3 "vulnguard_cli.py" "$@"
