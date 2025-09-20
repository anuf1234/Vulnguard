#!/bin/bash

echo
echo "========================================"
echo "  VulnGuard Security Platform v2.0"
echo "========================================"
echo
echo "Choose an option:"
echo "1. Install complete platform"
echo "2. Run security agent scan"
echo "3. Launch desktop application"
echo "4. Show CLI help"
echo "5. Exit"
echo
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "Starting platform installer..."
        ./vulnguard-installer.sh
        ;;
    2)
        echo "Starting security scan..."
        ./vulnguard-agent.sh --no-upload --verbose
        ;;
    3)
        echo "Launching desktop application..."
        ./vulnguard-desktop.sh &
        ;;
    4)
        echo "VulnGuard CLI Help:"
        ./vulnguard-cli.sh --help
        ;;
    5)
        exit 0
        ;;
    *)
        echo "Invalid choice. Please try again."
        ;;
esac

echo
read -p "Press Enter to continue..."
