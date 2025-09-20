# VulnGuard Linux Components

## Quick Start
1. Run `./quick_start.sh` for guided setup
2. Or execute scripts directly from terminal

## Components  
- **vulnguard-agent.sh** - Security scanning agent
- **vulnguard-cli.sh** - Automation and CI/CD tool
- **vulnguard-desktop.sh** - Professional GUI (requires X11)
- **vulnguard-installer.sh** - Complete platform setup

## Requirements
- Linux (Ubuntu 18.04+, CentOS 7+, or equivalent)
- Python 3.8+ (auto-installed if needed)
- 4GB RAM, 2GB disk space
- Internet connection for dependencies and updates
- X11 server for GUI components

## Examples
```bash
# Agent scan
./vulnguard-agent.sh --help
./vulnguard-agent.sh --server https://your-server.com --api-key YOUR_KEY

# CLI automation
./vulnguard-cli.sh assets list  
./vulnguard-cli.sh scan network 192.168.1.0/24

# Desktop GUI
./vulnguard-desktop.sh

# Platform installer
./vulnguard-installer.sh
```

All Python dependencies are automatically installed!
