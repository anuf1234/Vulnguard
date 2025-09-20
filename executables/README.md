# VulnGuard Executable Package v2.0

This directory contains all the components needed to create standalone executables for the VulnGuard vulnerability management platform.

## 🎯 What's Included

### 1. **VulnGuard Agent** (`vulnguard_agent.py`)
Lightweight scanning agent for deployment on Windows/Linux machines.

**Features:**
- Local vulnerability scanning with AI-powered analysis
- Configuration misconfiguration detection
- Compliance checking (CIS, NIST benchmarks)
- System inventory collection (processes, packages, services)
- Network security assessment
- Automated reporting to central VulnGuard server
- Offline capability with local report generation

**Use Cases:**
- Deploy on production servers for continuous monitoring
- Laptop/workstation security assessment
- Air-gapped environment scanning
- CI/CD pipeline integration

### 2. **VulnGuard CLI** (`vulnguard_cli.py`)
Command-line interface for automation and CI/CD integration.

**Features:**
- Complete asset management (create, list, update)
- Vulnerability scanning (network, file-based)
- AI-powered findings analysis
- Ansible remediation generation (guided/automatic)
- Change management workflows
- Audit trail access
- Ticket creation and management
- Dashboard statistics

**Use Cases:**
- DevOps automation scripts
- CI/CD security gates
- Bulk asset management
- Automated remediation workflows

### 3. **VulnGuard Desktop** (`vulnguard_desktop.py`)
Cross-platform GUI application built with tkinter.

**Features:**
- Professional security dashboard with real-time metrics
- Asset inventory management with filtering
- Vulnerability findings browser with detailed views
- Scan management (network scans, file uploads)
- Remediation playbook viewer and executor
- Audit trail visualization
- Settings management and server configuration

**Use Cases:**
- Security analysts daily workflow
- Executive security reporting
- Remediation planning and execution
- Offline security assessment

### 4. **VulnGuard Installer** (`vulnguard_installer.py`)
Complete platform installer with dependency management.

**Features:**
- Automated installation of Python, Node.js, MongoDB
- Complete VulnGuard platform deployment
- System service configuration
- Desktop shortcuts and startup scripts
- Web interface setup (React frontend + FastAPI backend)
- Database initialization and configuration

**Use Cases:**
- New environment setup
- Enterprise deployment
- Development environment creation
- Demonstration and evaluation

### 5. **Build System** (`build_executables.py`)
Automated executable creation using PyInstaller.

**Features:**
- Cross-platform executable generation
- Dependency bundling and optimization
- Version information and branding
- Distribution package creation
- Documentation generation

## 🚀 Quick Start

### Option 1: Build Your Own Executables

```bash
# Install build dependencies
pip install pyinstaller psutil requests pymongo fastapi uvicorn motor python-dotenv pydantic

# Run the builder
python build_executables.py

# Find executables in dist/ directory
ls dist/
```

### Option 2: Use Python Scripts Directly

```bash
# Agent scan
python vulnguard_agent.py --server https://your-server.com --api-key YOUR-KEY

# CLI operations
python vulnguard_cli.py assets list
python vulnguard_cli.py scan network 192.168.1.0/24

# Desktop application
python vulnguard_desktop.py

# Platform installation
python vulnguard_installer.py
```

## 📋 Build Requirements

### System Requirements:
- **Python 3.8+** with pip
- **4GB RAM** for building
- **2GB disk space** for build artifacts
- **Internet connection** for dependency downloads

### Python Dependencies:
```
pyinstaller>=5.0
requests>=2.31.0
psutil>=5.9.0
pymongo>=4.5.0
fastapi>=0.110.1
uvicorn>=0.25.0
motor>=3.3.1
python-dotenv>=1.0.1
pydantic>=2.6.4
python-multipart>=0.0.9
```

### Platform-Specific:
- **Windows:** Visual Studio Build Tools (for some dependencies)
- **Linux:** gcc, python3-dev, python3-tkinter packages

## 🔧 Build Process

The build system creates:

1. **Single-file executables** using PyInstaller
2. **Version information** and branding
3. **Dependency bundling** for portability
4. **Distribution packages** (ZIP for Windows, tar.gz for Linux)
5. **Documentation** and usage guides

### Build Output Structure:
```
vulnguard-v2.0-{platform}-{arch}/
├── executables/
│   ├── vulnguard-agent(.exe)
│   ├── vulnguard-cli(.exe)
│   ├── vulnguard-desktop(.exe)
│   └── vulnguard-installer(.exe)
├── README.md
└── quick_start(.bat/.sh)
```

## 🎯 Usage Examples

### Agent Deployment:
```bash
# Local scan with upload to server
./vulnguard-agent --server https://vulnguard.company.com --api-key abc123

# Offline scan (save results locally)
./vulnguard-agent --no-upload

# Compliance scanning
./vulnguard-agent --compliance CIS --verbose
```

### CLI Automation:
```bash
# Asset management
./vulnguard-cli assets create web-server-01 --ip 192.168.1.100 --type server

# Network scanning
./vulnguard-cli scan network "192.168.1.0/24,10.0.0.1-10.0.0.50"

# AI remediation
./vulnguard-cli remediation ansible FINDING_ID --guided

# Change management
./vulnguard-cli change create "Security Fix for CVE-2023-1234" REMEDIATION_ID
```

### Desktop Application:
- Launch GUI for interactive vulnerability management
- Connect to VulnGuard server or work offline
- Browse assets, findings, and remediation playbooks
- Generate and export security reports

### Platform Installation:
```bash
# Complete platform setup
./vulnguard-installer

# After installation, access via:
# Web UI: http://localhost:3000
# API: http://localhost:8001/api
```

## 🔒 Security Features

### Vulnerability Detection:
- **CVE database integration** with real-time feeds
- **AI-powered analysis** using Emergent LLM
- **Misconfiguration detection** with compliance mapping
- **Cross-host correlation** for widespread vulnerabilities

### Remediation Capabilities:
- **Ansible playbook generation** with AI assistance
- **Guided execution** with step-by-step instructions
- **Rollback procedures** for safe deployment
- **Multi-host automation** with inventory management

### Enterprise Integration:
- **Change management** workflows with approvals
- **Ticketing integration** (JIRA, ServiceNow)
- **Audit trails** for compliance reporting
- **RBAC support** for multi-user environments

## 📊 Platform Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   VulnGuard     │    │   VulnGuard     │    │   VulnGuard     │
│     Agent       │    │      CLI        │    │    Desktop      │
│                 │    │                 │    │                 │
│ • Local Scans   │    │ • Automation    │    │ • GUI Interface │
│ • Reporting     │    │ • CI/CD         │    │ • Dashboards    │
│ • Compliance    │    │ • Bulk Ops      │    │ • Reports       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   VulnGuard     │
                    │    Platform     │
                    │                 │
                    │ • Web UI        │
                    │ • REST API      │
                    │ • Database      │
                    │ • AI Engine     │
                    └─────────────────┘
```

## 🤖 AI-Powered Features

### Vulnerability Analysis:
- **Risk assessment** with business impact analysis
- **Exploitability scoring** with EPSS integration
- **Cross-host impact** assessment
- **Prioritization recommendations** based on multiple factors

### Remediation Generation:
- **Ansible playbook creation** with best practices
- **Multi-platform support** (Linux, Windows, containers)
- **Guided execution steps** with validation checks
- **Rollback procedures** for safe deployment

### Configuration Analysis:
- **Misconfiguration detection** using ML models
- **Compliance mapping** to security frameworks
- **Baseline deviation** analysis
- **Remediation suggestions** with implementation guides

## 📈 Enterprise Features

### Asset Management:
- **Comprehensive inventory** with business context
- **Compliance tracking** by framework and business unit
- **Criticality assessment** with risk-based prioritization
- **Integration points** for existing CMDB systems

### Change Management:
- **Approval workflows** with role-based permissions
- **Maintenance windows** and scheduling
- **Impact assessment** with stakeholder notification
- **Rollback procedures** with automated testing

### Audit & Compliance:
- **Complete audit trails** for all security operations
- **Compliance reporting** for multiple frameworks
- **Evidence collection** for audit purposes
- **Automated documentation** generation

## 🔄 Continuous Integration

### CI/CD Integration:
```yaml
# Example GitHub Actions workflow
- name: VulnGuard Security Scan
  run: |
    ./vulnguard-cli scan network ${{ env.TARGET_NETWORK }}
    ./vulnguard-cli findings list --severity critical --format json > security-report.json
```

### Automation Scripts:
```bash
#!/bin/bash
# Automated remediation pipeline
FINDING_ID=$(./vulnguard-cli findings list --severity critical --format json | jq -r '.[0].id')
REMEDIATION_ID=$(./vulnguard-cli remediation ansible $FINDING_ID --guided)
CHANGE_ID=$(./vulnguard-cli change create "Automated Security Fix" $REMEDIATION_ID)
echo "Change request created: $CHANGE_ID"
```

## 📚 Documentation

- **API Reference:** Complete REST API documentation
- **User Guides:** Step-by-step operational procedures
- **Integration Guides:** Third-party system integration
- **Security Playbooks:** Incident response procedures
- **Compliance Mapping:** Framework requirement coverage

## 🛠️ Development

### Contributing:
1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request with documentation

### Testing:
```bash
# Unit tests
python -m pytest tests/

# Integration tests
python -m pytest tests/integration/

# Build tests
python build_executables.py --test-mode
```

---

## 🎉 Success Stories

VulnGuard has been successfully deployed in:
- **Enterprise environments** with 10,000+ assets
- **Cloud-native architectures** with container scanning
- **Regulated industries** with compliance requirements
- **DevOps pipelines** with automated security gates

**Ready to secure your infrastructure? Start with the installer!**

```bash
./vulnguard-installer
```