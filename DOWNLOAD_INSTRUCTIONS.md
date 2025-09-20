# 📥 VulnGuard v2.0 Download Instructions

## 🎯 Distribution Package Details

**File:** `vulnguard-v2.0-final-distribution.tar.gz`  
**Size:** ~46 MB  
**Location:** `/app/executables/vulnguard-v2.0-final-distribution.tar.gz`  
**Created:** September 20, 2024

## 📦 What's Inside the Package

The distribution contains platform-specific executables and scripts for:

### 🐧 Linux Components:
- `vulnguard-agent.sh` - Lightweight scanning agent
- `vulnguard-cli.sh` - Command-line interface
- `vulnguard-desktop.sh` - GUI application
- `vulnguard-installer.sh` - Platform installer
- `quick_start.sh` - Quick setup script

### 🖥️ Windows Components:
- `vulnguard-agent.exe` - Lightweight scanning agent
- `vulnguard-cli.exe` - Command-line interface  
- `vulnguard-desktop.exe` - GUI application
- `vulnguard-installer.exe` - Platform installer
- `quick_start.bat` - Quick setup script

## 💾 Download Methods

### Method 1: Direct File Access (If you have server access)
```bash
# Copy the file to your local machine
scp user@server:/app/executables/vulnguard-v2.0-final-distribution.tar.gz ./

# Or using rsync
rsync -avz user@server:/app/executables/vulnguard-v2.0-final-distribution.tar.gz ./
```

### Method 2: HTTP Download (If web server is configured)
```bash
# If the application server is running, the file might be accessible via HTTP
curl -O http://your-server-domain/executables/vulnguard-v2.0-final-distribution.tar.gz

# Or using wget
wget http://your-server-domain/executables/vulnguard-v2.0-final-distribution.tar.gz
```

### Method 3: Container Volume Mount (If using Docker/Kubernetes)
```bash
# If running in container, copy from container to host
docker cp container-name:/app/executables/vulnguard-v2.0-final-distribution.tar.gz ./

# Or if using kubectl
kubectl cp pod-name:/app/executables/vulnguard-v2.0-final-distribution.tar.gz ./vulnguard-v2.0-final-distribution.tar.gz
```

## 📂 Extraction & Installation

### 1. Extract the Distribution
```bash
# Extract the tar.gz file
tar -xzf vulnguard-v2.0-final-distribution.tar.gz

# Navigate to the extracted directory
cd vulnguard_final_distribution
```

### 2. Directory Structure After Extraction
```
vulnguard_final_distribution/
├── MANIFEST.json          # Package manifest
├── VERSION.json           # Version information
├── README.md             # Main documentation
├── linux/                # Linux executables and scripts
│   ├── quick_start.sh
│   ├── vulnguard-agent.sh
│   ├── vulnguard-cli.sh
│   ├── vulnguard-desktop.sh
│   ├── vulnguard-installer.sh
│   └── README.md
└── windows/              # Windows executables and scripts
    ├── quick_start.bat
    ├── vulnguard-agent.exe
    ├── vulnguard-cli.exe
    ├── vulnguard-desktop.exe
    ├── vulnguard-installer.exe
    └── README.md
```

## 🚀 Quick Start Guide

### For Linux:
```bash
# Make scripts executable
cd linux
chmod +x *.sh

# Quick platform setup
./quick_start.sh

# Or run individual components:
./vulnguard-installer.sh  # Install full platform
./vulnguard-agent.sh      # Run vulnerability agent
./vulnguard-cli.sh        # Use CLI interface
./vulnguard-desktop.sh    # Launch GUI application
```

### For Windows:
```cmd
# Navigate to Windows directory
cd windows

# Quick platform setup
quick_start.bat

# Or run individual components:
vulnguard-installer.exe   # Install full platform
vulnguard-agent.exe       # Run vulnerability agent
vulnguard-cli.exe         # Use CLI interface
vulnguard-desktop.exe     # Launch GUI application
```

## 🔧 Usage Examples

### VulnGuard Agent (Scanning)
```bash
# Linux
./vulnguard-agent.sh --server https://your-vulnguard-server.com --api-key YOUR_API_KEY

# Windows
vulnguard-agent.exe --server https://your-vulnguard-server.com --api-key YOUR_API_KEY
```

### VulnGuard CLI (Automation)
```bash
# Linux
./vulnguard-cli.sh assets list
./vulnguard-cli.sh scan network 192.168.1.0/24

# Windows
vulnguard-cli.exe assets list
vulnguard-cli.exe scan network 192.168.1.0/24
```

### VulnGuard Desktop (GUI)
```bash
# Linux
./vulnguard-desktop.sh

# Windows
vulnguard-desktop.exe
```

### Full Platform Installation
```bash
# Linux
./vulnguard-installer.sh

# Windows
vulnguard-installer.exe
```

## 📋 System Requirements

### Minimum Requirements:
- **RAM:** 2GB (4GB recommended)
- **Disk Space:** 1GB for installation
- **Network:** Internet connection for vulnerability database updates
- **OS:** Windows 10+ or Linux (Ubuntu 18.04+, CentOS 7+, etc.)

### Dependencies:
- **Linux:** Most dependencies are bundled in the executables
- **Windows:** Visual C++ Redistributable (usually pre-installed)

## 🔒 Security Notes

1. **Verify File Integrity:** Check the file size matches ~46MB
2. **Scan for Malware:** Run through your organization's security tools
3. **Test in Staging:** Test the executables in a non-production environment first
4. **API Keys:** Keep your VulnGuard API keys secure and rotate them regularly

## 🆘 Troubleshooting

### Common Issues:

#### Linux:
```bash
# If permission denied:
chmod +x *.sh

# If Python-related errors:
sudo apt-get install python3 python3-pip python3-tkinter

# If dependencies missing:
pip3 install -r requirements.txt  # If requirements.txt is provided
```

#### Windows:
```cmd
# If executable blocked by Windows Defender:
# Right-click → Properties → Unblock

# If missing Visual C++ Redistributable:
# Download from Microsoft's official website

# If Python errors:
# Install Python 3.8+ from python.org
```

## 📞 Support & Documentation

- **Main Documentation:** See `README.md` in each platform directory
- **API Documentation:** Available after running the installer
- **Issue Reporting:** Contact your system administrator
- **Update Process:** Re-download and replace executables

## 🎉 Success Verification

After installation, verify everything works:

```bash
# Check if platform is running (after installer)
curl http://localhost:8001/api/health    # Backend health check
curl http://localhost:3000               # Frontend access

# Test CLI functionality
./vulnguard-cli.sh --help               # Should show help menu

# Test agent functionality  
./vulnguard-agent.sh --version          # Should show version info
```

---

## 📈 Next Steps After Download

1. **Extract** the distribution package
2. **Choose your platform** (Linux or Windows directory)
3. **Run the installer** for full platform setup, OR
4. **Use individual components** as needed
5. **Configure** your server endpoints and API keys
6. **Start scanning** your infrastructure!

**Happy Vulnerability Management! 🛡️**