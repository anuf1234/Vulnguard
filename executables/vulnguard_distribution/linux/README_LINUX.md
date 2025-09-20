# VulnGuard Linux Scripts

## Installation
1. Extract all files: `tar -xf vulnguard-v2.0-distribution.tar`
2. Make scripts executable: `chmod +x *.sh`
3. Run installer: `./vulnguard-installer.sh`

## Scripts
- **vulnguard-agent.sh** - Security scanning agent
- **vulnguard-cli.sh** - Command-line interface
- **vulnguard-desktop.sh** - GUI application (requires X11)
- **vulnguard-installer.sh** - Platform installer

## Dependencies
Scripts will automatically install required Python packages:
- requests, psutil, pymongo, fastapi, uvicorn, motor, python-dotenv, pydantic

## Quick Start
```bash
# Run installer
./vulnguard-installer.sh

# Or start with agent
./vulnguard-agent.sh --help
./vulnguard-agent.sh --server https://your-server.com

# CLI usage
./vulnguard-cli.sh dashboard
./vulnguard-cli.sh assets list

# Desktop app
./vulnguard-desktop.sh
```

## System Requirements
- Linux (Ubuntu 18.04+, CentOS 7+, or equivalent)
- Python 3.8+ 
- 4GB RAM minimum
- 2GB disk space
- Internet connection (for dependencies and updates)

For GUI: X11 server and tkinter support required.
