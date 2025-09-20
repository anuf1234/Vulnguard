# VulnGuard Windows Components

## Quick Start
1. Double-click `quick_start.bat` for guided setup
2. Or run executables directly from command prompt

## Components
- **vulnguard-agent** - Security scanning agent
- **vulnguard-cli** - Automation and CI/CD tool  
- **vulnguard-desktop** - Professional GUI
- **vulnguard-installer** - Complete platform setup

## Requirements
- Windows 10 or later
- Python 3.8+ (auto-installed if needed)
- 4GB RAM, 2GB disk space
- Internet connection for updates

## Examples
```cmd
REM Agent scan
vulnguard-agent.bat --help
vulnguard-agent.bat --server https://your-server.com --api-key YOUR_KEY

REM CLI automation  
vulnguard-cli.bat assets list
vulnguard-cli.bat scan network 192.168.1.0/24

REM Desktop GUI
vulnguard-desktop.bat

REM Platform installer
vulnguard-installer.bat
```

All dependencies are automatically installed!
