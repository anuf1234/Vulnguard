#!/usr/bin/env python3
"""
VulnGuard Executable Builder
Creates standalone executables for all VulnGuard components
Uses PyInstaller to create Windows .exe and Linux binaries
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import json

class VulnGuardBuilder:
    def __init__(self):
        self.platform = platform.system().lower()
        self.build_dir = Path('dist')
        self.spec_dir = Path('build_specs')
        
        # Ensure directories exist
        self.build_dir.mkdir(exist_ok=True)
        self.spec_dir.mkdir(exist_ok=True)
        
        print("🔨 VulnGuard Executable Builder")
        print("="*50)
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Architecture: {platform.machine()}")
        print(f"Build Directory: {self.build_dir.absolute()}")
        print("="*50)
    
    def check_pyinstaller(self):
        """Check if PyInstaller is available"""
        try:
            subprocess.run(['pyinstaller', '--version'], 
                         capture_output=True, check=True)
            print("✅ PyInstaller is available")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ PyInstaller not found")
            print("Installing PyInstaller...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], 
                             check=True)
                print("✅ PyInstaller installed successfully")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install PyInstaller")
                return False
    
    def install_dependencies(self):
        """Install required dependencies for building"""
        print("\n📦 Installing build dependencies...")
        
        dependencies = [
            'requests',
            'psutil',
            'pymongo',
            'fastapi',
            'uvicorn',
            'motor',
            'python-dotenv',
            'pydantic',
            'python-multipart'
        ]
        
        # GUI dependencies
        if self.platform == 'windows':
            # tkinter is included with Python on Windows
            pass
        else:
            # On Linux, might need additional packages
            dependencies.extend(['tkinter'])
        
        try:
            for dep in dependencies:
                print(f"Installing {dep}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                             check=True, capture_output=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def create_spec_file(self, script_name, app_name, description, icon=None, console=True):
        """Create PyInstaller spec file"""
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{script_name}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.protocols.websockets.websockets_impl',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.http.h11_impl',
        'uvicorn.protocols.http.httptools_impl',
        'uvicorn.loops.auto',
        'uvicorn.loops.asyncio',
        'uvicorn.logging',
        'fastapi.security',
        'pydantic.validators',
        'motor.motor_asyncio',
        'pymongo',
        'psutil',
        'requests'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={'true' if console else 'false'},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    {'icon="' + icon + '",' if icon else ''}
)
'''
        
        spec_path = self.spec_dir / f'{app_name}.spec'
        with open(spec_path, 'w') as f:
            f.write(spec_content)
        
        return spec_path
    
    def create_version_info(self, app_name, description):
        """Create version info file for Windows executables"""
        version_info = f'''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 0, 0, 0),
    prodvers=(2, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'VulnGuard Security'),
            StringStruct(u'FileDescription', u'{description}'),
            StringStruct(u'FileVersion', u'2.0.0.0'),
            StringStruct(u'InternalName', u'{app_name}'),
            StringStruct(u'LegalCopyright', u'Copyright © 2024 VulnGuard'),
            StringStruct(u'OriginalFilename', u'{app_name}.exe'),
            StringStruct(u'ProductName', u'VulnGuard Security Platform'),
            StringStruct(u'ProductVersion', u'2.0.0.0')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
        
        version_path = Path('version_info.txt')
        with open(version_path, 'w') as f:
            f.write(version_info)
        
        return version_path
    
    def build_executable(self, script_name, app_name, description, console=True):
        """Build single executable"""
        print(f"\n🔨 Building {app_name}...")
        
        # Create version info
        version_file = self.create_version_info(app_name, description)
        
        # Create spec file
        spec_file = self.create_spec_file(script_name, app_name, description, console=console)
        
        try:
            # Build with PyInstaller
            cmd = [
                'pyinstaller',
                '--clean',
                '--onefile',
                '--distpath', str(self.build_dir),
                str(spec_file)
            ]
            
            if not console:
                cmd.append('--windowed')
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {app_name} built successfully")
                
                # Get the executable path
                if self.platform == 'windows':
                    exe_path = self.build_dir / f'{app_name}.exe'
                else:
                    exe_path = self.build_dir / app_name
                
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    print(f"   Size: {size_mb:.1f} MB")
                    print(f"   Path: {exe_path}")
                    return True
                else:
                    print(f"❌ Executable not found: {exe_path}")
                    return False
            else:
                print(f"❌ Build failed for {app_name}")
                print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Build error for {app_name}: {e}")
            return False
        
        finally:
            # Cleanup
            if version_file.exists():
                version_file.unlink()
    
    def build_all_executables(self):
        """Build all VulnGuard executables"""
        print("\n🏗️  Building all VulnGuard executables...")
        
        executables = [
            {
                'script': 'vulnguard_agent.py',
                'name': 'vulnguard-agent',
                'description': 'VulnGuard Security Scanning Agent',
                'console': True
            },
            {
                'script': 'vulnguard_cli.py',
                'name': 'vulnguard-cli',
                'description': 'VulnGuard Command Line Interface',
                'console': True
            },
            {
                'script': 'vulnguard_desktop.py',
                'name': 'vulnguard-desktop',
                'description': 'VulnGuard Desktop Application',
                'console': False
            },
            {
                'script': 'vulnguard_installer.py',
                'name': 'vulnguard-installer',
                'description': 'VulnGuard Platform Installer',
                'console': True
            }
        ]
        
        successful_builds = 0
        total_builds = len(executables)
        
        for exe_config in executables:
            script_path = Path(exe_config['script'])
            if not script_path.exists():
                print(f"❌ Script not found: {script_path}")
                continue
            
            success = self.build_executable(
                exe_config['script'],
                exe_config['name'],
                exe_config['description'],
                exe_config['console']
            )
            
            if success:
                successful_builds += 1
        
        print(f"\n📊 Build Summary:")
        print(f"   Successful: {successful_builds}/{total_builds}")
        print(f"   Build Directory: {self.build_dir.absolute()}")
        
        return successful_builds == total_builds
    
    def create_package(self):
        """Create distribution package"""
        print("\n📦 Creating distribution package...")
        
        package_name = f"vulnguard-v2.0-{self.platform}-{platform.machine().lower()}"
        package_dir = Path(package_name)
        
        # Create package directory
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir()
        
        # Copy executables
        executables_dir = package_dir / 'executables'
        executables_dir.mkdir()
        
        for exe_file in self.build_dir.glob('vulnguard-*'):
            if exe_file.is_file():
                shutil.copy2(exe_file, executables_dir)
                print(f"✅ Packaged {exe_file.name}")
        
        # Create documentation
        readme_content = f"""# VulnGuard Security Platform v2.0
## Comprehensive Vulnerability Management Suite

### Included Executables:

#### 1. VulnGuard Agent (`vulnguard-agent`)
Lightweight scanning agent for deployment on Windows/Linux machines.

**Usage:**
```bash
./vulnguard-agent --server https://your-server.com --api-key YOUR_API_KEY
./vulnguard-agent --no-upload  # Local scan only
./vulnguard-agent --compliance CIS  # Compliance scanning
```

**Features:**
- Local vulnerability scanning
- Configuration misconfiguration detection
- Compliance checking (CIS, NIST)
- System inventory collection
- Automated reporting to central server

#### 2. VulnGuard CLI (`vulnguard-cli`)
Command-line interface for automation and CI/CD integration.

**Usage:**
```bash
./vulnguard-cli assets list
./vulnguard-cli findings list --severity critical
./vulnguard-cli scan network 192.168.1.0/24
./vulnguard-cli remediation ansible FINDING_ID --guided
./vulnguard-cli change create "Security Fix" REMEDIATION_ID
```

**Features:**
- Asset management
- Vulnerability scanning
- AI-powered Ansible remediation
- Change management workflows
- Audit trail access

#### 3. VulnGuard Desktop (`vulnguard-desktop`)
Cross-platform desktop GUI application.

**Features:**
- Professional security dashboard
- Asset inventory management
- Vulnerability findings browser
- Scan management interface
- Remediation playbook viewer
- Audit trail visualization

#### 4. VulnGuard Installer (`vulnguard-installer`)
Complete platform installer with all dependencies.

**Usage:**
```bash
./vulnguard-installer  # Install complete platform
./vulnguard-installer --uninstall  # Remove installation
```

**Features:**
- Automated dependency installation (Python, Node.js, MongoDB)
- Complete platform setup
- System service configuration
- Desktop shortcuts creation
- Startup scripts generation

### Platform Features:

✅ **Vulnerability + Misconfiguration Scanning**
- AI-powered vulnerability detection
- Configuration baseline analysis
- Compliance framework scanning (CIS, NIST, PCI-DSS)

✅ **Ansible Remediation (Manual/Guided)**
- AI-generated Ansible playbooks
- Step-by-step guided execution
- Multi-host deployment support
- Rollback capabilities

✅ **Usable UI + Audit Trails + Cross-Host Tracking**
- Professional enterprise interface
- Comprehensive audit logging
- Multi-system vulnerability correlation
- Real-time security dashboards

✅ **Change Management/Ticketing/Inventory Integration**
- Approval workflows for remediation
- JIRA/ServiceNow integration
- Asset inventory with business unit tracking
- Complete operational workflows

### Installation:

1. **Quick Start (Recommended):**
   ```bash
   ./vulnguard-installer
   ```

2. **Manual Agent Deployment:**
   ```bash
   ./vulnguard-agent --server https://your-vulnguard-server.com
   ```

3. **CLI Usage:**
   ```bash
   export VULNGUARD_SERVER=https://your-server.com
   export VULNGUARD_API_KEY=your-api-key
   ./vulnguard-cli dashboard
   ```

### System Requirements:

- **Operating System:** Windows 10+ or Linux (Ubuntu 18.04+, CentOS 7+)
- **Memory:** 4GB RAM minimum, 8GB recommended
- **Disk Space:** 2GB for installation, 10GB for data storage
- **Network:** Internet access for vulnerability feeds and updates

### Support:

- Documentation: https://vulnguard.io/docs
- Issues: https://github.com/vulnguard/platform/issues
- Community: https://vulnguard.io/community

---
Built with ❤️ for cybersecurity professionals
"""
        
        readme_path = package_dir / 'README.md'
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        # Create startup script
        if self.platform == 'windows':
            startup_script = package_dir / 'quick_start.bat'
            with open(startup_script, 'w') as f:
                f.write("""@echo off
echo VulnGuard Security Platform v2.0
echo ====================================
echo.
echo Choose an option:
echo 1. Install complete platform
echo 2. Run desktop application
echo 3. Run agent scan
echo 4. Show CLI help
echo.
set /p choice="Enter choice (1-4): "

if %choice%==1 (
    cd executables
    vulnguard-installer.exe
) else if %choice%==2 (
    cd executables
    vulnguard-desktop.exe
) else if %choice%==3 (
    cd executables
    vulnguard-agent.exe --help
) else if %choice%==4 (
    cd executables
    vulnguard-cli.exe --help
) else (
    echo Invalid choice
)

pause
""")
        else:
            startup_script = package_dir / 'quick_start.sh'
            with open(startup_script, 'w') as f:
                f.write("""#!/bin/bash
echo "VulnGuard Security Platform v2.0"
echo "===================================="
echo
echo "Choose an option:"
echo "1. Install complete platform"
echo "2. Run desktop application"
echo "3. Run agent scan"
echo "4. Show CLI help"
echo
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        cd executables
        ./vulnguard-installer
        ;;
    2)
        cd executables
        ./vulnguard-desktop
        ;;
    3)
        cd executables
        ./vulnguard-agent --help
        ;;
    4)
        cd executables
        ./vulnguard-cli --help
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
""")
            os.chmod(startup_script, 0o755)
        
        # Create archive
        if self.platform == 'windows':
            # Create ZIP archive
            shutil.make_archive(package_name, 'zip', '.', package_name)
            archive_path = Path(f"{package_name}.zip")
        else:
            # Create tar.gz archive
            shutil.make_archive(package_name, 'gztar', '.', package_name)
            archive_path = Path(f"{package_name}.tar.gz")
        
        # Cleanup
        shutil.rmtree(package_dir)
        
        if archive_path.exists():
            size_mb = archive_path.stat().st_size / (1024 * 1024)
            print(f"✅ Package created: {archive_path}")
            print(f"   Size: {size_mb:.1f} MB")
            return True
        else:
            print("❌ Failed to create package")
            return False
    
    def cleanup(self):
        """Cleanup build artifacts"""
        print("\n🧹 Cleaning up build artifacts...")
        
        cleanup_dirs = ['build', '__pycache__']
        cleanup_files = ['*.spec']
        
        for cleanup_dir in cleanup_dirs:
            dir_path = Path(cleanup_dir)
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"✅ Removed {cleanup_dir}")
        
        # Remove spec files
        for spec_file in Path('.').glob('*.spec'):
            spec_file.unlink()
            print(f"✅ Removed {spec_file}")
        
        # Remove spec directory
        if self.spec_dir.exists():
            shutil.rmtree(self.spec_dir)
            print(f"✅ Removed {self.spec_dir}")

def main():
    builder = VulnGuardBuilder()
    
    print("\nThis builder will create standalone executables for:")
    print("• VulnGuard Scanning Agent")
    print("• VulnGuard CLI Tool")
    print("• VulnGuard Desktop Application")
    print("• VulnGuard Platform Installer")
    
    try:
        response = input("\nProceed with build? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Build cancelled.")
            return
    except KeyboardInterrupt:
        print("\nBuild cancelled.")
        return
    
    try:
        if not builder.check_pyinstaller():
            return
        
        if not builder.install_dependencies():
            return
        
        if not builder.build_all_executables():
            print("❌ Some builds failed")
            return
        
        if not builder.create_package():
            print("❌ Package creation failed")
            return
        
        print("\n🎉 Build completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Test the executables in the 'dist' directory")
        print("2. Distribute the package archive")
        print("3. Update documentation with usage instructions")
        
    except KeyboardInterrupt:
        print("\nBuild cancelled by user")
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
    finally:
        builder.cleanup()

if __name__ == '__main__':
    main()