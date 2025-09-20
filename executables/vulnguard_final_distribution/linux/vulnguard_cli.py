#!/usr/bin/env python3
"""
VulnGuard CLI Tool
Command-line interface for VulnGuard vulnerability management
Supports automation, CI/CD integration, and batch operations
"""

import os
import sys
import json
import requests
import argparse
import time
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VulnGuardCLI:
    def __init__(self, server_url=None, api_key=None):
        self.server_url = server_url or os.getenv('VULNGUARD_SERVER', 'https://vulnguard-3.preview.emergentagent.com')
        self.api_key = api_key or os.getenv('VULNGUARD_API_KEY', '')
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def make_request(self, method, endpoint, data=None):
        """Make API request to VulnGuard server"""
        url = f"{self.server_url}/api/{endpoint.lstrip('/')}"
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=30)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, timeout=30)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, timeout=30)
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
    
    def list_assets(self, format_output='table'):
        """List all assets"""
        logger.info("Fetching assets...")
        assets = self.make_request('GET', '/assets')
        
        if not assets:
            print("No assets found or API error")
            return
        
        if format_output == 'json':
            print(json.dumps(assets, indent=2))
        else:
            # Table format
            print(f"{'Hostname':<20} {'IP Address':<15} {'Type':<15} {'Environment':<12} {'Criticality':<10}")
            print("-" * 80)
            for asset in assets:
                print(f"{asset['hostname']:<20} {asset.get('ip_address', 'N/A'):<15} "
                      f"{asset['asset_type']:<15} {asset['environment']:<12} {asset['criticality']:<10}")
    
    def create_asset(self, hostname, ip_address=None, asset_type='server', environment='production', 
                    criticality=3, owner=None, business_unit=None, location=None):
        """Create new asset"""
        asset_data = {
            'hostname': hostname,
            'ip_address': ip_address,
            'asset_type': asset_type,
            'environment': environment,
            'criticality': criticality,
            'owner': owner,
            'business_unit': business_unit,
            'location': location
        }
        
        # Remove None values
        asset_data = {k: v for k, v in asset_data.items() if v is not None}
        
        logger.info(f"Creating asset: {hostname}")
        result = self.make_request('POST', '/assets', asset_data)
        
        if result:
            print(f"Asset created successfully: {result['id']}")
            return result['id']
        else:
            print("Failed to create asset")
            return None
    
    def list_findings(self, asset_id=None, severity=None, finding_type=None, cross_host=False, format_output='table'):
        """List vulnerability findings"""
        logger.info("Fetching findings...")
        
        params = {}
        if asset_id:
            params['asset_id'] = asset_id
        if severity:
            params['severity'] = severity
        if finding_type:
            params['finding_type'] = finding_type
        if cross_host:
            params['cross_host'] = 'true'
        
        endpoint = '/findings'
        if params:
            param_str = '&'.join([f"{k}={v}" for k, v in params.items()])
            endpoint += f"?{param_str}"
        
        findings = self.make_request('GET', endpoint)
        
        if not findings:
            print("No findings found or API error")
            return
        
        if format_output == 'json':
            print(json.dumps(findings, indent=2))
        else:
            # Table format
            print(f"{'Title':<40} {'Severity':<10} {'Type':<15} {'CVE IDs':<20}")
            print("-" * 90)
            for finding in findings:
                cve_str = ', '.join(finding.get('cve_ids', [])[:2])  # Show first 2 CVEs
                if len(finding.get('cve_ids', [])) > 2:
                    cve_str += '...'
                print(f"{finding['title'][:38]:<40} {finding['severity'].upper():<10} "
                      f"{finding.get('finding_type', 'vuln'):<15} {cve_str:<20}")
    
    def start_network_scan(self, targets, scan_name=None, include_misconfigs=True):
        """Start network vulnerability scan"""
        if isinstance(targets, str):
            targets = [t.strip() for t in targets.split(',')]
        
        scan_data = {
            'targets': targets,
            'scan_name': scan_name or f'CLI Scan {datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'include_misconfigs': include_misconfigs
        }
        
        logger.info(f"Starting network scan for {len(targets)} targets...")
        result = self.make_request('POST', '/scan/network', scan_data)
        
        if result:
            print(f"Scan started successfully:")
            print(f"  Scan ID: {result['scan_id']}")
            print(f"  Status: {result['status']}")
            print(f"  Findings: {result.get('findings_count', 0)}")
            print(f"  Misconfigurations: {result.get('misconfigurations', 0)}")
            return result['scan_id']
        else:
            print("Failed to start scan")
            return None
    
    def upload_scan_file(self, file_path, asset_id, scan_name=None):
        """Upload vulnerability scan file"""
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"File not found: {file_path}")
            return None
        
        # For CLI, we'll read and send the file content
        logger.info(f"Processing scan file: {file_path}")
        
        # Simple file processing for demonstration
        # In production, you'd properly parse different formats
        if file_path.suffix.lower() == '.json':
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Convert to expected format
                scan_result = {
                    'scan_name': scan_name or f'File Upload {file_path.name}',
                    'asset_id': asset_id,
                    'findings': self.parse_scan_file(data)
                }
                
                print(f"Processed {len(scan_result['findings'])} findings from {file_path}")
                return scan_result
                
            except Exception as e:
                print(f"Error processing file: {e}")
                return None
        else:
            print(f"Unsupported file format: {file_path.suffix}")
            return None
    
    def parse_scan_file(self, data):
        """Parse scan file data into findings"""
        findings = []
        
        # Handle various JSON formats
        if 'vulnerabilities' in data:
            for vuln in data['vulnerabilities']:
                finding = {
                    'title': vuln.get('name', 'Unknown Vulnerability'),
                    'description': vuln.get('description', ''),
                    'severity': vuln.get('severity', 'medium').lower(),
                    'cve_ids': vuln.get('cve', []),
                    'finding_type': 'vulnerability'
                }
                findings.append(finding)
        
        return findings
    
    def generate_ansible_remediation(self, finding_id, guided=False):
        """Generate Ansible remediation for finding"""
        logger.info(f"Generating Ansible remediation for finding: {finding_id}")
        
        endpoint = f'/findings/{finding_id}/remediation/ansible'
        if guided:
            endpoint += '?guided=true'
        
        result = self.make_request('POST', endpoint)
        
        if result:
            print(f"Ansible remediation generated:")
            print(f"  Playbook ID: {result['id']}")
            print(f"  Estimated Time: {result.get('estimated_time', 'N/A')} minutes")
            print(f"  Risk Level: {result.get('risk_level', 'N/A')}")
            
            if result.get('ansible_playbook'):
                print("\nAnsible Playbook:")
                print("-" * 50)
                print(result['ansible_playbook'][:500] + '...' if len(result['ansible_playbook']) > 500 else result['ansible_playbook'])
            
            return result['id']
        else:
            print("Failed to generate remediation")
            return None
    
    def create_change_request(self, title, description, remediation_id, requestor, priority='medium'):
        """Create change management request"""
        change_data = {
            'title': title,
            'description': description,
            'remediation_id': remediation_id,
            'requestor': requestor,
            'priority': priority
        }
        
        logger.info(f"Creating change request: {title}")
        result = self.make_request('POST', '/change-requests', change_data)
        
        if result:
            print(f"Change request created:")
            print(f"  Request ID: {result['id']}")
            print(f"  Status: {result['status']}")
            print(f"  Priority: {result['priority']}")
            return result['id']
        else:
            print("Failed to create change request")
            return None
    
    def get_audit_logs(self, action=None, resource_type=None, limit=50):
        """Get audit logs"""
        logger.info("Fetching audit logs...")
        
        params = {'limit': limit}
        if action:
            params['action'] = action
        if resource_type:
            params['resource_type'] = resource_type
        
        endpoint = '/audit-logs'
        if params:
            param_str = '&'.join([f"{k}={v}" for k, v in params.items()])
            endpoint += f"?{param_str}"
        
        logs = self.make_request('GET', endpoint)
        
        if not logs:
            print("No audit logs found or API error")
            return
        
        print(f"{'Timestamp':<20} {'User':<15} {'Action':<10} {'Resource':<15} {'Resource ID':<15}")
        print("-" * 80)
        for log in logs:
            timestamp = datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{timestamp:<20} {log['user_id']:<15} {log['action']:<10} "
                  f"{log['resource_type']:<15} {log['resource_id'][:13]:<15}")
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        logger.info("Fetching dashboard statistics...")
        
        stats = self.make_request('GET', '/dashboard/stats')
        
        if not stats:
            print("Failed to fetch dashboard stats")
            return
        
        summary = stats.get('summary', {})
        
        print("=== VulnGuard Dashboard Statistics ===")
        print(f"Total Assets: {summary.get('total_assets', 0)}")
        print(f"Total Findings: {summary.get('total_findings', 0)}")
        print(f"Cross-Host Vulnerabilities: {summary.get('cross_host_vulnerabilities', 0)}")
        print(f"Pending Approvals: {summary.get('pending_approvals', 0)}")
        print(f"Change Requests: {summary.get('change_requests', 0)}")
        
        if 'severity_breakdown' in stats:
            print("\nSeverity Breakdown:")
            for severity, count in stats['severity_breakdown'].items():
                print(f"  {severity.capitalize()}: {count}")
        
        if 'finding_types' in stats:
            print("\nFinding Types:")
            for type_name, count in stats['finding_types'].items():
                print(f"  {type_name.replace('_', ' ').title()}: {count}")

def main():
    parser = argparse.ArgumentParser(description='VulnGuard CLI Tool')
    parser.add_argument('--server', help='VulnGuard server URL')
    parser.add_argument('--api-key', help='API key for authentication')
    parser.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Assets commands
    assets_parser = subparsers.add_parser('assets', help='Asset management')
    assets_subparsers = assets_parser.add_subparsers(dest='assets_action')
    
    # List assets
    list_assets_parser = assets_subparsers.add_parser('list', help='List assets')
    
    # Create asset
    create_asset_parser = assets_subparsers.add_parser('create', help='Create asset')
    create_asset_parser.add_argument('hostname', help='Asset hostname')
    create_asset_parser.add_argument('--ip', help='IP address')
    create_asset_parser.add_argument('--type', default='server', help='Asset type')
    create_asset_parser.add_argument('--env', default='production', help='Environment')
    create_asset_parser.add_argument('--criticality', type=int, default=3, help='Criticality (1-5)')
    create_asset_parser.add_argument('--owner', help='Asset owner')
    create_asset_parser.add_argument('--business-unit', help='Business unit')
    create_asset_parser.add_argument('--location', help='Location')
    
    # Findings commands
    findings_parser = subparsers.add_parser('findings', help='Findings management')
    findings_subparsers = findings_parser.add_subparsers(dest='findings_action')
    
    # List findings
    list_findings_parser = findings_subparsers.add_parser('list', help='List findings')
    list_findings_parser.add_argument('--asset-id', help='Filter by asset ID')
    list_findings_parser.add_argument('--severity', choices=['critical', 'high', 'medium', 'low'], help='Filter by severity')
    list_findings_parser.add_argument('--type', choices=['vulnerability', 'misconfiguration', 'compliance'], help='Filter by type')
    list_findings_parser.add_argument('--cross-host', action='store_true', help='Show only cross-host vulnerabilities')
    
    # Scanning commands
    scan_parser = subparsers.add_parser('scan', help='Vulnerability scanning')
    scan_subparsers = scan_parser.add_subparsers(dest='scan_action')
    
    # Network scan
    network_scan_parser = scan_subparsers.add_parser('network', help='Start network scan')
    network_scan_parser.add_argument('targets', help='Comma-separated list of targets')
    network_scan_parser.add_argument('--name', help='Scan name')
    network_scan_parser.add_argument('--no-misconfigs', action='store_true', help='Skip misconfiguration detection')
    
    # File upload
    upload_parser = scan_subparsers.add_parser('upload', help='Upload scan file')
    upload_parser.add_argument('file', help='Scan file path')
    upload_parser.add_argument('asset_id', help='Asset ID')
    upload_parser.add_argument('--name', help='Scan name')
    
    # Remediation commands
    remediation_parser = subparsers.add_parser('remediation', help='Remediation management')
    remediation_subparsers = remediation_parser.add_subparsers(dest='remediation_action')
    
    # Generate Ansible remediation
    ansible_parser = remediation_subparsers.add_parser('ansible', help='Generate Ansible remediation')
    ansible_parser.add_argument('finding_id', help='Finding ID')
    ansible_parser.add_argument('--guided', action='store_true', help='Generate guided execution steps')
    
    # Change management commands
    change_parser = subparsers.add_parser('change', help='Change management')
    change_subparsers = change_parser.add_subparsers(dest='change_action')
    
    # Create change request
    create_change_parser = change_subparsers.add_parser('create', help='Create change request')
    create_change_parser.add_argument('title', help='Change request title')
    create_change_parser.add_argument('remediation_id', help='Remediation ID')
    create_change_parser.add_argument('--description', help='Description')
    create_change_parser.add_argument('--requestor', default='cli-user', help='Requestor')
    create_change_parser.add_argument('--priority', choices=['critical', 'high', 'medium', 'low'], default='medium', help='Priority')
    
    # Audit commands
    audit_parser = subparsers.add_parser('audit', help='Audit trail')
    audit_parser.add_argument('--action', help='Filter by action')
    audit_parser.add_argument('--resource-type', help='Filter by resource type')
    audit_parser.add_argument('--limit', type=int, default=50, help='Limit number of results')
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Dashboard statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create CLI instance
    cli = VulnGuardCLI(server_url=args.server, api_key=args.api_key)
    
    # Execute commands
    try:
        if args.command == 'assets':
            if args.assets_action == 'list':
                cli.list_assets(format_output=args.format)
            elif args.assets_action == 'create':
                cli.create_asset(
                    hostname=args.hostname,
                    ip_address=args.ip,
                    asset_type=args.type,
                    environment=args.env,
                    criticality=args.criticality,
                    owner=args.owner,
                    business_unit=args.business_unit,
                    location=args.location
                )
        
        elif args.command == 'findings':
            if args.findings_action == 'list':
                cli.list_findings(
                    asset_id=args.asset_id,
                    severity=args.severity,
                    finding_type=args.type,
                    cross_host=args.cross_host,
                    format_output=args.format
                )
        
        elif args.command == 'scan':
            if args.scan_action == 'network':
                cli.start_network_scan(
                    targets=args.targets,
                    scan_name=args.name,
                    include_misconfigs=not args.no_misconfigs
                )
            elif args.scan_action == 'upload':
                cli.upload_scan_file(
                    file_path=args.file,
                    asset_id=args.asset_id,
                    scan_name=args.name
                )
        
        elif args.command == 'remediation':
            if args.remediation_action == 'ansible':
                cli.generate_ansible_remediation(
                    finding_id=args.finding_id,
                    guided=args.guided
                )
        
        elif args.command == 'change':
            if args.change_action == 'create':
                cli.create_change_request(
                    title=args.title,
                    description=args.description or f"Change request for remediation {args.remediation_id}",
                    remediation_id=args.remediation_id,
                    requestor=args.requestor,
                    priority=args.priority
                )
        
        elif args.command == 'audit':
            cli.get_audit_logs(
                action=args.action,
                resource_type=args.resource_type,
                limit=args.limit
            )
        
        elif args.command == 'dashboard':
            cli.get_dashboard_stats()
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()