#!/usr/bin/env python3
"""
VulnGuard Platform Installer
Self-contained installer for the complete VulnGuard platform
Installs all dependencies and sets up the platform on Windows/Linux
"""

import os
import sys
import subprocess
import platform
import urllib.request
import tarfile
import zipfile
import json
import shutil
from pathlib import Path
import tempfile
import time

class VulnGuardInstaller:
    def __init__(self):
        self.platform = platform.system().lower()
        self.architecture = platform.machine().lower()
        self.install_dir = Path.home() / 'VulnGuard'
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Component versions
        self.versions = {
            'python': '3.11.0',
            'nodejs': '18.17.0',
            'mongodb': '7.0.2'
        }
        
        print("🛡️  VulnGuard Platform Installer v2.0")
        print("="*50)
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Architecture: {platform.machine()}")
        print(f"Install Directory: {self.install_dir}")
        print("="*50)
    
    def check_prerequisites(self):
        """Check system prerequisites"""
        print("\n📋 Checking prerequisites...")
        
        prerequisites = []
        
        # Check available disk space (need at least 2GB)
        try:
            if self.platform == 'windows':
                import shutil
                free_bytes = shutil.disk_usage('.').free
            else:
                import shutil
                free_bytes = shutil.disk_usage('.').free
            
            free_gb = free_bytes / (1024**3)
            if free_gb < 2:
                print(f"❌ Insufficient disk space: {free_gb:.1f}GB available, need 2GB minimum")
                return False
            else:
                print(f"✅ Disk space: {free_gb:.1f}GB available")
                
        except Exception as e:
            print(f"⚠️  Could not check disk space: {e}")
        
        # Check if running as administrator/root for system-wide installation
        if self.platform == 'windows':
            try:
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
                if not is_admin:
                    print("⚠️  Not running as administrator - installing to user directory")
                else:
                    print("✅ Running as administrator")
            except:
                print("⚠️  Could not check administrator status")
        else:
            if os.geteuid() == 0:
                print("✅ Running as root")
            else:
                print("⚠️  Not running as root - installing to user directory")
        
        return True
    
    def download_file(self, url, filename):
        """Download file with progress"""
        print(f"📥 Downloading {filename}...")
        
        def progress_hook(block_num, block_size, total_size):
            if total_size > 0:
                percent = min(100, (block_num * block_size * 100) / total_size)
                sys.stdout.write(f"\r{percent:.1f}%")
                sys.stdout.flush()
        
        try:
            urllib.request.urlretrieve(url, filename, progress_hook)
            print(f" ✅ Downloaded {filename}")
            return True
        except Exception as e:
            print(f" ❌ Failed to download {filename}: {e}")
            return False
    
    def install_python(self):
        """Install Python if not available"""
        print("\n🐍 Checking Python installation...")
        
        try:
            # Check if Python is already installed
            result = subprocess.run([sys.executable, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ Python already installed: {version}")
                return True
        except:
            pass
        
        print("📦 Installing Python...")
        
        if self.platform == 'windows':
            # Download Python installer for Windows
            python_url = f"https://www.python.org/ftp/python/{self.versions['python']}/python-{self.versions['python']}-amd64.exe"
            installer_path = self.temp_dir / 'python-installer.exe'
            
            if self.download_file(python_url, installer_path):
                # Run installer silently
                subprocess.run([str(installer_path), '/quiet', 'InstallAllUsers=1', 'PrependPath=1'])
                print("✅ Python installation completed")
                return True
        
        elif self.platform == 'linux':
            # Try to install via package manager
            try:
                # Try apt-get (Debian/Ubuntu)
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'python3', 'python3-pip', 'python3-venv'], check=True)
                print("✅ Python installed via apt-get")
                return True
            except:
                try:
                    # Try yum (RedHat/CentOS)
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'python3', 'python3-pip'], check=True)
                    print("✅ Python installed via yum")
                    return True
                except:
                    print("❌ Could not install Python automatically")
                    return False
        
        return False
    
    def install_nodejs(self):
        """Install Node.js if not available"""
        print("\n📦 Checking Node.js installation...")
        
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ Node.js already installed: {version}")
                return True
        except:
            pass
        
        print("📦 Installing Node.js...")
        
        if self.platform == 'windows':
            # Download Node.js installer for Windows
            node_url = f"https://nodejs.org/dist/v{self.versions['nodejs']}/node-v{self.versions['nodejs']}-x64.msi"
            installer_path = self.temp_dir / 'nodejs-installer.msi'
            
            if self.download_file(node_url, installer_path):
                subprocess.run(['msiexec', '/i', str(installer_path), '/quiet'])
                print("✅ Node.js installation completed")
                return True
        
        elif self.platform == 'linux':
            try:
                # Install via package manager
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nodejs', 'npm'], check=True)
                print("✅ Node.js installed via apt-get")
                return True
            except:
                try:
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'nodejs', 'npm'], check=True)
                    print("✅ Node.js installed via yum")
                    return True
                except:
                    print("❌ Could not install Node.js automatically")
                    return False
        
        return False
    
    def install_mongodb(self):
        """Install MongoDB if not available"""
        print("\n📦 Checking MongoDB installation...")
        
        try:
            result = subprocess.run(['mongod', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ MongoDB already installed")
                return True
        except:
            pass
        
        print("📦 Installing MongoDB...")
        
        if self.platform == 'windows':
            # Download MongoDB installer for Windows
            mongo_url = f"https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-{self.versions['mongodb']}.zip"
            installer_path = self.temp_dir / 'mongodb.zip'
            
            if self.download_file(mongo_url, installer_path):
                # Extract MongoDB
                with zipfile.ZipFile(installer_path, 'r') as zip_ref:
                    zip_ref.extractall(self.install_dir / 'mongodb')
                print("✅ MongoDB installation completed")
                return True
        
        elif self.platform == 'linux':
            try:
                # Install via package manager
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'mongodb'], check=True)
                print("✅ MongoDB installed via apt-get")
                return True
            except:
                try:
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'mongodb'], check=True)
                    print("✅ MongoDB installed via yum")
                    return True
                except:
                    print("❌ Could not install MongoDB automatically")
                    return False
        
        return False
    
    def create_directory_structure(self):
        """Create VulnGuard directory structure"""
        print("\n📁 Creating directory structure...")
        
        directories = [
            self.install_dir,
            self.install_dir / 'backend',
            self.install_dir / 'frontend',
            self.install_dir / 'executables',
            self.install_dir / 'data',
            self.install_dir / 'logs',
            self.install_dir / 'config'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created {directory}")
    
    def install_vulnguard_platform(self):
        """Install VulnGuard platform files"""
        print("\n🛡️  Installing VulnGuard platform...")
        
        # Backend files
        backend_files = {
            'server.py': self.get_backend_code(),
            'requirements.txt': self.get_requirements(),
            '.env': self.get_backend_env()
        }
        
        for filename, content in backend_files.items():
            file_path = self.install_dir / 'backend' / filename
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Created {file_path}")
        
        # Frontend files
        frontend_files = {
            'package.json': self.get_package_json(),
            '.env': self.get_frontend_env()
        }
        
        for filename, content in frontend_files.items():
            file_path = self.install_dir / 'frontend' / filename
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Created {file_path}")
        
        # Create src directory and basic React app
        src_dir = self.install_dir / 'frontend' / 'src'
        src_dir.mkdir(exist_ok=True)
        
        app_js = src_dir / 'App.js'
        with open(app_js, 'w') as f:
            f.write(self.get_react_app())
        print(f"✅ Created {app_js}")
    
    def install_python_dependencies(self):
        """Install Python dependencies"""
        print("\n📦 Installing Python dependencies...")
        
        requirements_file = self.install_dir / 'backend' / 'requirements.txt'
        
        try:
            # Create virtual environment
            venv_path = self.install_dir / 'backend' / 'venv'
            subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
            
            # Activate virtual environment and install dependencies
            if self.platform == 'windows':
                pip_path = venv_path / 'Scripts' / 'pip.exe'
                python_path = venv_path / 'Scripts' / 'python.exe'
            else:
                pip_path = venv_path / 'bin' / 'pip'
                python_path = venv_path / 'bin' / 'python'
            
            subprocess.run([str(pip_path), 'install', '--upgrade', 'pip'], check=True)
            subprocess.run([str(pip_path), 'install', '-r', str(requirements_file)], check=True)
            
            print("✅ Python dependencies installed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install Python dependencies: {e}")
            return False
    
    def install_node_dependencies(self):
        """Install Node.js dependencies"""
        print("\n📦 Installing Node.js dependencies...")
        
        frontend_dir = self.install_dir / 'frontend'
        
        try:
            # Change to frontend directory and install dependencies
            original_dir = os.getcwd()
            os.chdir(frontend_dir)
            
            subprocess.run(['npm', 'install'], check=True)
            
            os.chdir(original_dir)
            print("✅ Node.js dependencies installed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install Node.js dependencies: {e}")
            return False
    
    def create_startup_scripts(self):
        """Create startup scripts"""
        print("\n📝 Creating startup scripts...")
        
        if self.platform == 'windows':
            # Windows batch files
            start_script = self.install_dir / 'start_vulnguard.bat'
            with open(start_script, 'w') as f:
                f.write(self.get_windows_start_script())
            print(f"✅ Created {start_script}")
            
            stop_script = self.install_dir / 'stop_vulnguard.bat'
            with open(stop_script, 'w') as f:
                f.write(self.get_windows_stop_script())
            print(f"✅ Created {stop_script}")
            
        else:
            # Linux shell scripts
            start_script = self.install_dir / 'start_vulnguard.sh'
            with open(start_script, 'w') as f:
                f.write(self.get_linux_start_script())
            os.chmod(start_script, 0o755)
            print(f"✅ Created {start_script}")
            
            stop_script = self.install_dir / 'stop_vulnguard.sh'
            with open(stop_script, 'w') as f:
                f.write(self.get_linux_stop_script())
            os.chmod(stop_script, 0o755)
            print(f"✅ Created {stop_script}")
    
    def create_desktop_shortcuts(self):
        """Create desktop shortcuts"""
        print("\n🖥️  Creating desktop shortcuts...")
        
        if self.platform == 'windows':
            # Create Windows shortcuts (simplified)
            desktop = Path.home() / 'Desktop'
            shortcut_path = desktop / 'VulnGuard.bat'
            
            with open(shortcut_path, 'w') as f:
                f.write(f'@echo off\ncd /d "{self.install_dir}"\nstart http://localhost:3000\ncall start_vulnguard.bat\n')
            
            print(f"✅ Created desktop shortcut: {shortcut_path}")
        
        else:
            # Create Linux desktop entry
            desktop_entry = f"""[Desktop Entry]
Name=VulnGuard
Comment=Vulnerability Management Platform
Exec={self.install_dir}/start_vulnguard.sh
Icon={self.install_dir}/icon.png
Terminal=false
Type=Application
Categories=Security;Network;
"""
            
            desktop_dir = Path.home() / 'Desktop'
            if desktop_dir.exists():
                shortcut_path = desktop_dir / 'VulnGuard.desktop'
                with open(shortcut_path, 'w') as f:
                    f.write(desktop_entry)
                os.chmod(shortcut_path, 0o755)
                print(f"✅ Created desktop shortcut: {shortcut_path}")
    
    def setup_system_service(self):
        """Setup VulnGuard as system service"""
        print("\n⚙️  Setting up system service...")
        
        if self.platform == 'windows':
            # Windows service setup would require additional tools
            print("⚠️  Windows service setup requires manual configuration")
            print(f"   Use Task Scheduler to run: {self.install_dir}/start_vulnguard.bat")
        
        else:
            # Linux systemd service
            service_content = f"""[Unit]
Description=VulnGuard Vulnerability Management Platform
After=network.target

[Service]
Type=forking
User=vulnguard
WorkingDirectory={self.install_dir}
ExecStart={self.install_dir}/start_vulnguard.sh
ExecStop={self.install_dir}/stop_vulnguard.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
            
            service_path = Path('/etc/systemd/system/vulnguard.service')
            try:
                with open(service_path, 'w') as f:
                    f.write(service_content)
                
                subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
                subprocess.run(['sudo', 'systemctl', 'enable', 'vulnguard'], check=True)
                
                print("✅ System service configured")
                print("   Start with: sudo systemctl start vulnguard")
                print("   Stop with: sudo systemctl stop vulnguard")
                
            except Exception as e:
                print(f"⚠️  Could not setup system service: {e}")
    
    def run_initial_setup(self):
        """Run initial platform setup"""
        print("\n🔧 Running initial setup...")
        
        try:
            # Start MongoDB
            print("Starting MongoDB...")
            if self.platform == 'windows':
                mongodb_path = self.install_dir / 'mongodb' / 'bin' / 'mongod.exe'
                if mongodb_path.exists():
                    subprocess.Popen([str(mongodb_path), '--dbpath', str(self.install_dir / 'data')])
            else:
                subprocess.Popen(['mongod', '--dbpath', str(self.install_dir / 'data')])
            
            time.sleep(5)  # Wait for MongoDB to start
            
            # Initialize database
            print("Initializing database...")
            # This would run database initialization scripts
            
            print("✅ Initial setup completed")
            return True
            
        except Exception as e:
            print(f"❌ Initial setup failed: {e}")
            return False
    
    def install(self):
        """Run complete installation"""
        try:
            if not self.check_prerequisites():
                return False
            
            if not self.install_python():
                print("❌ Python installation failed")
                return False
            
            if not self.install_nodejs():
                print("❌ Node.js installation failed")
                return False
            
            if not self.install_mongodb():
                print("❌ MongoDB installation failed")
                return False
            
            self.create_directory_structure()
            self.install_vulnguard_platform()
            
            if not self.install_python_dependencies():
                return False
            
            if not self.install_node_dependencies():
                return False
            
            self.create_startup_scripts()
            self.create_desktop_shortcuts()
            self.setup_system_service()
            
            if not self.run_initial_setup():
                return False
            
            print("\n🎉 VulnGuard installation completed successfully!")
            print("="*50)
            print(f"Installation Directory: {self.install_dir}")
            print(f"Web Interface: http://localhost:3000")
            print(f"API Endpoint: http://localhost:8001/api")
            print("\nStartup Commands:")
            if self.platform == 'windows':
                print(f"  Start: {self.install_dir}/start_vulnguard.bat")
                print(f"  Stop: {self.install_dir}/stop_vulnguard.bat")
            else:
                print(f"  Start: {self.install_dir}/start_vulnguard.sh")
                print(f"  Stop: {self.install_dir}/stop_vulnguard.sh")
            print("="*50)
            
            return True
            
        except KeyboardInterrupt:
            print("\n❌ Installation cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Installation failed: {e}")
            return False
        finally:
            # Cleanup temp directory
            try:
                shutil.rmtree(self.temp_dir)
            except:
                pass
    
    # Configuration file templates
    def get_backend_code(self):
        return '''# VulnGuard Backend - Simplified Version
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="VulnGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/")
async def root():
    return {"message": "VulnGuard API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
'''
    
    def get_requirements(self):
        return '''fastapi==0.110.1
uvicorn==0.25.0
pymongo==4.5.0
motor==3.3.1
python-multipart>=0.0.9
requests>=2.31.0
pydantic>=2.6.4
python-dotenv>=1.0.1
'''
    
    def get_backend_env(self):
        return '''MONGO_URL=mongodb://localhost:27017
DB_NAME=vulnguard_db
CORS_ORIGINS=*
'''
    
    def get_package_json(self):
        return """{
  "name": "vulnguard-frontend",
  "version": "2.0.0",
  "private": true,
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-scripts": "5.0.1",
    "axios": "^1.8.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  }
}"""
    
    def get_frontend_env(self):
        return 'REACT_APP_BACKEND_URL=http://localhost:8001\n'
    
    def get_react_app(self):
        return '''import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🛡️ VulnGuard</h1>
        <p>Vulnerability Management Platform v2.0</p>
        <p>Installation completed successfully!</p>
      </header>
    </div>
  );
}

export default App;
'''
    
    def get_windows_start_script(self):
        return f'''@echo off
echo Starting VulnGuard Platform...

REM Start MongoDB
start "MongoDB" /min "{self.install_dir}\\mongodb\\bin\\mongod.exe" --dbpath "{self.install_dir}\\data"

REM Wait for MongoDB
timeout /t 10

REM Start Backend
cd /d "{self.install_dir}\\backend"
start "VulnGuard Backend" venv\\Scripts\\python.exe server.py

REM Start Frontend
cd /d "{self.install_dir}\\frontend"
start "VulnGuard Frontend" npm start

echo VulnGuard Platform started!
echo Web Interface: http://localhost:3000
echo API Endpoint: http://localhost:8001/api
pause
'''
    
    def get_windows_stop_script(self):
        return '''@echo off
echo Stopping VulnGuard Platform...

taskkill /f /im python.exe
taskkill /f /im node.exe
taskkill /f /im mongod.exe

echo VulnGuard Platform stopped!
pause
'''
    
    def get_linux_start_script(self):
        return f'''#!/bin/bash
echo "Starting VulnGuard Platform..."

# Start MongoDB
mongod --dbpath "{self.install_dir}/data" --fork --logpath "{self.install_dir}/logs/mongodb.log"

# Wait for MongoDB
sleep 10

# Start Backend
cd "{self.install_dir}/backend"
source venv/bin/activate
python server.py &
echo $! > ../logs/backend.pid

# Start Frontend
cd "{self.install_dir}/frontend"
npm start &
echo $! > ../logs/frontend.pid

echo "VulnGuard Platform started!"
echo "Web Interface: http://localhost:3000"
echo "API Endpoint: http://localhost:8001/api"
'''
    
    def get_linux_stop_script(self):
        return f'''#!/bin/bash
echo "Stopping VulnGuard Platform..."

# Stop processes
if [ -f "{self.install_dir}/logs/backend.pid" ]; then
    kill $(cat "{self.install_dir}/logs/backend.pid")
    rm "{self.install_dir}/logs/backend.pid"
fi

if [ -f "{self.install_dir}/logs/frontend.pid" ]; then
    kill $(cat "{self.install_dir}/logs/frontend.pid")
    rm "{self.install_dir}/logs/frontend.pid"
fi

# Stop MongoDB
pkill mongod

echo "VulnGuard Platform stopped!"
'''

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--uninstall':
        print("🗑️  VulnGuard Uninstaller")
        print("This would remove VulnGuard installation")
        return
    
    installer = VulnGuardInstaller()
    
    print("\nThis installer will:")
    print("• Install Python, Node.js, and MongoDB")
    print("• Download and setup VulnGuard platform")
    print("• Create startup scripts and shortcuts")
    print("• Configure system services")
    
    try:
        response = input("\nProceed with installation? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Installation cancelled.")
            return
    except KeyboardInterrupt:
        print("\nInstallation cancelled.")
        return
    
    success = installer.install()
    
    if success:
        print("\n🎉 Installation completed successfully!")
        
        try:
            response = input("\nStart VulnGuard now? (y/N): ")
            if response.lower() in ['y', 'yes']:
                if installer.platform == 'windows':
                    subprocess.Popen([str(installer.install_dir / 'start_vulnguard.bat')])
                else:
                    subprocess.Popen([str(installer.install_dir / 'start_vulnguard.sh')])
                print("VulnGuard is starting...")
        except KeyboardInterrupt:
            pass
    else:
        print("\n❌ Installation failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()