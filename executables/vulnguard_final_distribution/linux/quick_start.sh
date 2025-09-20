#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

clear
echo -e "${GREEN}"
echo " ========================================================"
echo "   🛡️  VulnGuard Security Platform v2.0"
echo "   Complete Vulnerability Management Suite"  
echo " ========================================================"
echo -e "${NC}"
echo
echo -e "Choose your action:"
echo
echo -e "${GREEN}[1]${NC} 🚀 Install Complete Platform"
echo -e "${BLUE}[2]${NC} 🔍 Run Security Agent Scan"
echo -e "${PURPLE}[3]${NC} 💻 Launch Desktop Application"
echo -e "${YELLOW}[4]${NC} ⚙️  Command Line Tools Help"
echo -e "${CYAN}[5]${NC} 📚 View Documentation"
echo -e "${RED}[6]${NC} ❌ Exit"
echo
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo
        echo -e "${GREEN}🚀 Starting VulnGuard Platform Installer...${NC}"
        echo "This will install the complete platform with web UI"
        echo
        read -p "Press Enter to continue..."
        ./vulnguard-installer.sh
        ;;
    2)
        echo  
        echo -e "${BLUE}🔍 Running Security Agent Scan...${NC}"
        echo "This will scan the local system for vulnerabilities"
        echo
        read -p "Press Enter to continue..."
        ./vulnguard-agent.sh --no-upload --verbose
        ;;
    3)
        echo
        echo -e "${PURPLE}💻 Launching Desktop Application...${NC}"
        echo "Starting GUI application..."
        ./vulnguard-desktop.sh &
        echo "Desktop application started in background"
        ;;
    4)
        echo
        echo -e "${YELLOW}⚙️  VulnGuard CLI Tools:${NC}"
        echo
        ./vulnguard-cli.sh --help
        echo
        echo "For more commands try:"
        echo "  ./vulnguard-cli.sh assets --help"
        echo "  ./vulnguard-cli.sh scan --help"  
        echo "  ./vulnguard-cli.sh findings --help"
        ;;
    5)
        echo
        echo -e "${CYAN}📚 Opening documentation...${NC}"
        if [ -f "README.md" ]; then
            if command -v less &> /dev/null; then
                less README.md
            elif command -v more &> /dev/null; then
                more README.md
            else
                cat README.md
            fi
        else
            echo "README.md not found in current directory"
        fi
        ;;
    6)
        echo
        echo -e "${GREEN}Thank you for using VulnGuard! 👋${NC}"
        exit 0
        ;;
    *)
        echo
        echo -e "${RED}❌ Invalid choice. Please try again.${NC}"
        sleep 2
        exec "$0"
        ;;
esac

echo
echo -e "${GREEN}✅ Operation completed!${NC}"
read -p "Press Enter to continue..."
