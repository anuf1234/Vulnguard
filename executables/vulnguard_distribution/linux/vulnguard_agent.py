#!/usr/bin/env python3
"""
VulnGuard Scanning Agent
Lightweight executable for Windows/Linux deployment
Performs local vulnerability scans and reports to central platform
"""

import os
import sys
import json
import requests
import subprocess
import platform
import socket
import psutil
import argparse
import time
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vulnguard_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class VulnGuardAgent:
    def __init__(self, server_url=None, api_key=None):
        self.server_url = server_url or os.getenv('VULNGUARD_SERVER', 'https://vulnguard-3.preview.emergentagent.com')
        self.api_key = api_key or os.getenv('VULNGUARD_API_KEY', '')
        self.hostname = socket.gethostname()
        self.platform = platform.system()
        self.agent_id = f"{self.hostname}_{int(time.time())}"
        
        # Create results directory
        Path('results').mkdir(exist_ok=True)
        
    def get_system_info(self):
        """Collect comprehensive system information"""
        try:
            info = {
                'hostname': self.hostname,
                'platform': platform.system(),
                'platform_release': platform.release(),
                'platform_version': platform.version(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'ip_addresses': self.get_ip_addresses(),
                'memory': dict(psutil.virtual_memory()._asdict()),
                'disk': [dict(psutil.disk_usage(partition.mountpoint)._asdict()) 
                        for partition in psutil.disk_partitions()],
                'cpu_count': psutil.cpu_count(),
                'boot_time': psutil.boot_time(),
                'users': [user._asdict() for user in psutil.users()],
                'network_interfaces': self.get_network_interfaces(),
                'running_processes': self.get_running_processes()[:50],  # Limit to 50 processes
                'installed_packages': self.get_installed_packages(),
                'services': self.get_services(),
                'scan_timestamp': datetime.now().isoformat()
            }
            return info
        except Exception as e:
            logger.error(f"Error collecting system info: {e}")
            return {}
    
    def get_ip_addresses(self):
        """Get all IP addresses"""
        addresses = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    addresses.append(addr.address)
        return addresses
    
    def get_network_interfaces(self):
        """Get network interface information"""
        interfaces = {}
        for interface, addrs in psutil.net_if_addrs().items():
            interfaces[interface] = []
            for addr in addrs:
                interfaces[interface].append({
                    'family': str(addr.family),
                    'address': addr.address,
                    'netmask': addr.netmask,
                    'broadcast': addr.broadcast
                })
        return interfaces
    
    def get_running_processes(self):
        """Get running processes with security relevance"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline', 'connections']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.error(f"Error getting processes: {e}")
        return processes
    
    def get_installed_packages(self):
        """Get installed packages based on platform"""
        packages = []
        try:
            if self.platform == 'Linux':
                # Try multiple package managers
                package_commands = [
                    ['dpkg', '-l'],  # Debian/Ubuntu
                    ['rpm', '-qa'],  # RedHat/CentOS
                    ['pacman', '-Q']  # Arch
                ]
                
                for cmd in package_commands:
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                        if result.returncode == 0:
                            packages.extend(result.stdout.splitlines())
                            break
                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        continue
                        
            elif self.platform == 'Windows':
                # Use PowerShell to get installed programs
                cmd = ['powershell', '-Command', 'Get-WmiObject -Class Win32_Product | Select-Object Name, Version']
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                    if result.returncode == 0:
                        packages = result.stdout.splitlines()
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
                    
        except Exception as e:
            logger.error(f"Error getting packages: {e}")
        
        return packages[:100]  # Limit to 100 packages
    
    def get_services(self):
        """Get running services"""
        services = []
        try:
            if self.platform == 'Linux':
                # Use systemctl to get services
                result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=active'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    services = result.stdout.splitlines()
            elif self.platform == 'Windows':
                # Use PowerShell to get services
                result = subprocess.run(['powershell', '-Command', 'Get-Service | Where-Object {$_.Status -eq "Running"}'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    services = result.stdout.splitlines()
        except Exception as e:
            logger.error(f"Error getting services: {e}")
        
        return services[:50]  # Limit to 50 services
    
    def check_vulnerabilities(self):
        """Check for common vulnerabilities"""
        vulnerabilities = []
        
        # Check for common misconfigurations
        misconfigs = self.check_misconfigurations()
        vulnerabilities.extend(misconfigs)
        
        # Check for outdated software
        outdated = self.check_outdated_software()
        vulnerabilities.extend(outdated)
        
        # Check network security
        network_issues = self.check_network_security()
        vulnerabilities.extend(network_issues)
        
        return vulnerabilities
    
    def check_misconfigurations(self):
        """Check for common security misconfigurations"""
        misconfigs = []
        
        try:
            if self.platform == 'Linux':
                # Check SSH configuration
                ssh_config = Path('/etc/ssh/sshd_config')
                if ssh_config.exists():
                    with open(ssh_config, 'r') as f:
                        content = f.read()
                        if 'PermitRootLogin yes' in content:
                            misconfigs.append({
                                'type': 'misconfiguration',
                                'title': 'SSH Root Login Enabled',
                                'description': 'SSH is configured to allow direct root login',
                                'severity': 'high',
                                'file': str(ssh_config)
                            })
                        if 'PasswordAuthentication yes' in content:
                            misconfigs.append({
                                'type': 'misconfiguration',
                                'title': 'SSH Password Authentication Enabled',
                                'description': 'SSH allows password authentication instead of key-based only',
                                'severity': 'medium',
                                'file': str(ssh_config)
                            })
                
                # Check for world-writable files
                result = subprocess.run(['find', '/etc', '-type', 'f', '-perm', '-002'], 
                                      capture_output=True, text=True, timeout=30)
                if result.stdout:
                    misconfigs.append({
                        'type': 'misconfiguration',
                        'title': 'World-Writable Configuration Files',
                        'description': 'Found configuration files writable by all users',
                        'severity': 'high',
                        'files': result.stdout.splitlines()[:10]
                    })
                    
        except Exception as e:
            logger.error(f"Error checking misconfigurations: {e}")
        
        return misconfigs
    
    def check_outdated_software(self):
        """Check for outdated software with known vulnerabilities"""
        vulnerabilities = []
        
        # This is a simplified check - in production, you'd integrate with CVE databases
        outdated_patterns = [
            'openssl-1.0',
            'apache2-2.2',
            'nginx-1.0',
            'mysql-5.5',
            'php-5.6'
        ]
        
        packages = self.get_installed_packages()
        for package in packages:
            for pattern in outdated_patterns:
                if pattern in package.lower():
                    vulnerabilities.append({
                        'type': 'vulnerability',
                        'title': f'Outdated Software: {package}',
                        'description': f'Potentially vulnerable version detected: {package}',
                        'severity': 'medium',
                        'package': package,
                        'recommendation': f'Update {pattern} to latest version'
                    })
        
        return vulnerabilities
    
    def check_network_security(self):
        """Check network security configuration"""
        issues = []
        
        try:
            # Check for open ports
            connections = psutil.net_connections(kind='inet')
            listening_ports = [conn.laddr.port for conn in connections if conn.status == 'LISTEN']
            
            # Common vulnerable ports
            vulnerable_ports = {
                21: 'FTP',
                23: 'Telnet', 
                25: 'SMTP',
                53: 'DNS',
                80: 'HTTP',
                110: 'POP3',
                143: 'IMAP',
                443: 'HTTPS',
                993: 'IMAPS',
                995: 'POP3S'
            }
            
            for port in listening_ports:
                if port in vulnerable_ports:
                    issues.append({
                        'type': 'network_exposure',
                        'title': f'{vulnerable_ports[port]} Service Exposed',
                        'description': f'Service {vulnerable_ports[port]} is listening on port {port}',
                        'severity': 'medium' if port in [443, 993, 995] else 'high',
                        'port': port,
                        'service': vulnerable_ports[port]
                    })
                    
        except Exception as e:
            logger.error(f"Error checking network security: {e}")
        
        return issues
    
    def run_compliance_check(self, framework='CIS'):
        """Run compliance checks against security frameworks"""
        compliance_results = []
        
        try:
            if framework == 'CIS' and self.platform == 'Linux':
                # Basic CIS checks
                checks = [
                    {
                        'control': 'CIS-1.1.1',
                        'description': 'Ensure mounting of cramfs filesystems is disabled',
                        'check': self.check_cramfs_disabled()
                    },
                    {
                        'control': 'CIS-2.2.1', 
                        'description': 'Ensure xinetd is not installed',
                        'check': self.check_xinetd_not_installed()
                    },
                    {
                        'control': 'CIS-5.2.1',
                        'description': 'Ensure permissions on /etc/ssh/sshd_config are configured',
                        'check': self.check_sshd_config_permissions()
                    }
                ]
                
                for check in checks:
                    result = check['check']
                    compliance_results.append({
                        'framework': framework,
                        'control': check['control'],
                        'description': check['description'],
                        'status': 'pass' if result else 'fail',
                        'severity': 'medium'
                    })
                    
        except Exception as e:
            logger.error(f"Error running compliance checks: {e}")
        
        return compliance_results
    
    def check_cramfs_disabled(self):
        """Check if cramfs filesystem mounting is disabled"""
        try:
            result = subprocess.run(['modprobe', '-n', '-v', 'cramfs'], 
                                  capture_output=True, text=True)
            return 'install /bin/true' in result.stderr
        except:
            return False
    
    def check_xinetd_not_installed(self):
        """Check if xinetd is not installed"""
        try:
            result = subprocess.run(['which', 'xinetd'], capture_output=True)
            return result.returncode != 0
        except:
            return True
    
    def check_sshd_config_permissions(self):
        """Check SSH config file permissions"""
        try:
            ssh_config = Path('/etc/ssh/sshd_config')
            if ssh_config.exists():
                stat = ssh_config.stat()
                # Should be 600 (owner read/write only)
                return oct(stat.st_mode)[-3:] == '600'
        except:
            pass
        return False
    
    def generate_report(self):
        """Generate comprehensive security report"""
        logger.info("Starting VulnGuard security scan...")
        
        report = {
            'agent_id': self.agent_id,
            'scan_type': 'comprehensive',
            'timestamp': datetime.now().isoformat(),
            'system_info': self.get_system_info(),
            'vulnerabilities': self.check_vulnerabilities(),
            'compliance_results': self.run_compliance_check('CIS'),
            'summary': {}
        }
        
        # Generate summary
        vulns = report['vulnerabilities']
        compliance = report['compliance_results']
        
        report['summary'] = {
            'total_vulnerabilities': len(vulns),
            'critical_vulnerabilities': len([v for v in vulns if v.get('severity') == 'critical']),
            'high_vulnerabilities': len([v for v in vulns if v.get('severity') == 'high']),
            'medium_vulnerabilities': len([v for v in vulns if v.get('severity') == 'medium']),
            'low_vulnerabilities': len([v for v in vulns if v.get('severity') == 'low']),
            'compliance_passed': len([c for c in compliance if c.get('status') == 'pass']),
            'compliance_failed': len([c for c in compliance if c.get('status') == 'fail']),
            'risk_score': self.calculate_risk_score(vulns, compliance)
        }
        
        return report
    
    def calculate_risk_score(self, vulnerabilities, compliance_results):
        """Calculate overall risk score"""
        score = 0
        
        # Vulnerability scoring
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'low')
            if severity == 'critical':
                score += 10
            elif severity == 'high':
                score += 7
            elif severity == 'medium':
                score += 4
            elif severity == 'low':
                score += 1
        
        # Compliance scoring
        failed_controls = len([c for c in compliance_results if c.get('status') == 'fail'])
        score += failed_controls * 2
        
        # Normalize to 0-100 scale
        return min(score, 100)
    
    def save_report(self, report):
        """Save report to local file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"results/vulnguard_report_{self.hostname}_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"Report saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return None
    
    def upload_report(self, report):
        """Upload report to VulnGuard server"""
        if not self.server_url:
            logger.warning("No server URL configured, skipping upload")
            return False
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}' if self.api_key else ''
            }
            
            url = f"{self.server_url}/api/agent/report"
            response = requests.post(url, json=report, headers=headers, timeout=30)
            
            if response.status_code == 200:
                logger.info("Report uploaded successfully")
                return True
            else:
                logger.error(f"Upload failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error uploading report: {e}")
            return False
    
    def run_scan(self, upload=True, save_local=True):
        """Run complete security scan"""
        try:
            logger.info(f"VulnGuard Agent starting scan on {self.hostname}")
            
            # Generate report
            report = self.generate_report()
            
            # Save locally if requested
            filename = None
            if save_local:
                filename = self.save_report(report)
            
            # Upload to server if requested
            uploaded = False
            if upload:
                uploaded = self.upload_report(report)
            
            # Print summary
            summary = report['summary']
            logger.info("=== SCAN RESULTS ===")
            logger.info(f"Total Vulnerabilities: {summary['total_vulnerabilities']}")
            logger.info(f"Critical: {summary['critical_vulnerabilities']}")
            logger.info(f"High: {summary['high_vulnerabilities']}")
            logger.info(f"Medium: {summary['medium_vulnerabilities']}")
            logger.info(f"Low: {summary['low_vulnerabilities']}")
            logger.info(f"Compliance Passed: {summary['compliance_passed']}")
            logger.info(f"Compliance Failed: {summary['compliance_failed']}")
            logger.info(f"Risk Score: {summary['risk_score']}/100")
            
            if filename:
                logger.info(f"Report saved: {filename}")
            if uploaded:
                logger.info("Report uploaded to VulnGuard server")
            
            return report
            
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='VulnGuard Security Scanning Agent')
    parser.add_argument('--server', help='VulnGuard server URL')
    parser.add_argument('--api-key', help='API key for authentication')
    parser.add_argument('--no-upload', action='store_true', help='Skip uploading results to server')
    parser.add_argument('--no-save', action='store_true', help='Skip saving results locally')
    parser.add_argument('--compliance', default='CIS', help='Compliance framework (CIS, NIST)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create agent
    agent = VulnGuardAgent(server_url=args.server, api_key=args.api_key)
    
    # Run scan
    result = agent.run_scan(
        upload=not args.no_upload,
        save_local=not args.no_save
    )
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()