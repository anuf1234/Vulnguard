# VulnGuard Windows Executables

## Installation
1. Extract all files to a directory (e.g., C:\VulnGuard)
2. Run `vulnguard-installer.exe` for complete platform setup
3. Or run individual executables directly

## Executables
- **vulnguard-agent.exe** - Security scanning agent (13-15 MB)
- **vulnguard-cli.exe** - Command-line interface (12-14 MB)
- **vulnguard-desktop.exe** - GUI application (15-18 MB)
- **vulnguard-installer.exe** - Platform installer (10-12 MB)

## Quick Start
```cmd
# Run installer
vulnguard-installer.exe

# Or start with agent
vulnguard-agent.exe --help
vulnguard-agent.exe --server https://your-server.com

# CLI usage
vulnguard-cli.exe dashboard
vulnguard-cli.exe assets list

# Desktop app
vulnguard-desktop.exe
```

## System Requirements
- Windows 10 or later
- 4GB RAM minimum
- 2GB disk space
- Internet connection (for updates)

All dependencies are bundled - no additional software required!
