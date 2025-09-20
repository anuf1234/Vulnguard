#!/usr/bin/env python3
"""
VulnGuard v2.0 Backend API Testing Suite
Comprehensive testing for enhanced vulnerability management platform with:
- Vulnerability + Misconfiguration Scanning
- Ansible Remediation Capabilities  
- Cross-Host Vulnerability Analysis
- Change Management & Approval Workflows
- Ticketing System Integration
- Enhanced Audit Trails
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

class VulnGuardV2APITester:
    def __init__(self, base_url="https://securityscan-15.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.created_assets = []
        self.created_findings = []
        self.created_scans = []
        self.created_remediations = []
        self.created_change_requests = []
        self.created_tickets = []

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED {details}")
        else:
            print(f"❌ {name} - FAILED {details}")

    def make_request(self, method: str, endpoint: str, data: Dict = None, files: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        headers = {'Content-Type': 'application/json'} if not files else {}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                if files:
                    response = requests.post(url, data=data, files=files, timeout=30)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                return False, {}, 0

            try:
                response_data = response.json() if response.content else {}
            except:
                response_data = {"raw_response": response.text}

            return response.status_code < 400, response_data, response.status_code

        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}, 0

    # ===== BASIC CONNECTIVITY TESTS =====
    def test_health_check(self):
        """Test API health check endpoint with v2.0 features"""
        success, data, status = self.make_request('GET', '/')
        expected_keys = ['message', 'status', 'features']
        
        if success and all(key in data for key in expected_keys):
            features = data.get('features', [])
            v2_features = ['ansible_remediation', 'audit_trails', 'cross_host_tracking', 'change_management']
            has_v2_features = any(feature in features for feature in v2_features)
            
            if has_v2_features:
                self.log_test("Health Check v2.0", True, f"Status: {status}, Features: {len(features)}")
                return True
            else:
                self.log_test("Health Check v2.0", False, f"Missing v2.0 features. Got: {features}")
                return False
        else:
            self.log_test("Health Check v2.0", False, f"Status: {status}, Data: {data}")
            return False

    def test_enhanced_dashboard_stats(self):
        """Test enhanced dashboard statistics with v2.0 metrics"""
        success, data, status = self.make_request('GET', '/dashboard/stats')
        
        if success and isinstance(data, dict):
            # Check for v2.0 specific metrics
            v2_keys = ['cross_host_vulnerabilities', 'pending_approvals', 'change_requests', 'finding_types']
            summary = data.get('summary', {})
            
            has_v2_metrics = any(key in summary for key in v2_keys)
            
            if has_v2_metrics:
                self.log_test("Enhanced Dashboard Stats", True, 
                    f"Status: {status}, Cross-host: {summary.get('cross_host_vulnerabilities', 0)}, "
                    f"Pending: {summary.get('pending_approvals', 0)}")
                return data
            else:
                self.log_test("Enhanced Dashboard Stats", False, f"Missing v2.0 metrics. Got: {list(data.keys())}")
                return None
        else:
            self.log_test("Enhanced Dashboard Stats", False, f"Status: {status}, Data: {data}")
            return None

    # ===== ENHANCED ASSET MANAGEMENT =====
    def test_create_enhanced_asset(self):
        """Test enhanced asset creation with inventory management"""
        test_asset = {
            "hostname": f"test-server-{int(time.time())}",
            "ip_address": "192.168.1.100",
            "asset_type": "server",
            "owner": "Security Team",
            "environment": "production",
            "criticality": 2,
            "operating_system": "Ubuntu 20.04 LTS",
            "location": "Data Center A",
            "business_unit": "IT Operations",
            "compliance_requirements": ["CIS", "NIST"]
        }
        
        success, data, status = self.make_request('POST', '/assets', test_asset)
        
        if success and 'id' in data:
            self.created_assets.append(data['id'])
            self.log_test("Create Enhanced Asset", True, 
                f"Status: {status}, Asset ID: {data['id']}, BU: {data.get('business_unit')}")
            return data
        else:
            self.log_test("Create Enhanced Asset", False, f"Status: {status}, Data: {data}")
            return None

    # ===== ENHANCED SCANNING CAPABILITIES =====
    def test_configuration_scanning(self):
        """Test POST /api/scan/configuration - Configuration scanning"""
        if not self.created_assets:
            asset = self.test_create_enhanced_asset()
            if not asset:
                self.log_test("Configuration Scanning", False, "No asset available")
                return None
        
        asset_id = self.created_assets[0]
        config_data = {
            "ssh_config": {
                "PasswordAuthentication": "yes",
                "PermitRootLogin": "yes",
                "Protocol": "1"
            },
            "firewall_rules": [
                {"port": 22, "protocol": "tcp", "source": "0.0.0.0/0"},
                {"port": 80, "protocol": "tcp", "source": "0.0.0.0/0"}
            ]
        }
        
        success, data, status = self.make_request('POST', f'/scan/configuration?asset_id={asset_id}', config_data)
        
        if success and 'misconfigurations_found' in data:
            self.log_test("Configuration Scanning", True, 
                f"Status: {status}, Misconfigs: {data['misconfigurations_found']}")
            return data
        else:
            self.log_test("Configuration Scanning", False, f"Status: {status}, Data: {data}")
            return None

    def test_compliance_scanning(self):
        """Test POST /api/scan/compliance - Compliance scanning"""
        if not self.created_assets:
            self.test_create_enhanced_asset()
        
        if not self.created_assets:
            self.log_test("Compliance Scanning", False, "No assets available")
            return None
        
        scan_data = {
            "asset_ids": self.created_assets[:2],  # Use first 2 assets
            "framework": "CIS"
        }
        
        success, data, status = self.make_request('POST', '/scan/compliance', scan_data)
        
        if success and 'violations_found' in data:
            self.log_test("Compliance Scanning", True, 
                f"Status: {status}, Framework: {data.get('framework')}, Violations: {data['violations_found']}")
            return data
        else:
            self.log_test("Compliance Scanning", False, f"Status: {status}, Data: {data}")
            return None

    def test_enhanced_network_scan(self):
        """Test enhanced network scanning with misconfiguration detection"""
        scan_data = {
            "targets": ["192.168.1.1", "192.168.1.100", "10.0.0.1"],
            "scan_name": f"Enhanced Network Scan {int(time.time())}",
            "include_misconfigs": True
        }
        
        success, data, status = self.make_request('POST', '/scan/network', scan_data)
        
        if success and 'scan_id' in data:
            self.created_scans.append(data['scan_id'])
            self.log_test("Enhanced Network Scan", True, 
                f"Status: {status}, Scan ID: {data['scan_id']}, "
                f"Vulns: {data.get('vulnerabilities', 0)}, Misconfigs: {data.get('misconfigurations', 0)}")
            return data
        else:
            self.log_test("Enhanced Network Scan", False, f"Status: {status}, Data: {data}")
            return None

    # ===== CROSS-HOST VULNERABILITY ANALYSIS =====
    def test_cross_host_analysis(self):
        """Test GET /api/findings/cross-host-analysis - Cross-host vulnerability analysis"""
        success, data, status = self.make_request('GET', '/findings/cross-host-analysis')
        
        if success and 'cross_host_vulnerabilities' in data:
            cross_host_vulns = data['cross_host_vulnerabilities']
            self.log_test("Cross-Host Analysis", True, 
                f"Status: {status}, Cross-host vulns: {len(cross_host_vulns)}")
            return data
        else:
            self.log_test("Cross-Host Analysis", False, f"Status: {status}, Data: {data}")
            return None

    def test_enhanced_findings_filtering(self):
        """Test enhanced findings with cross-host and type filtering"""
        # Test cross-host filtering
        success, data, status = self.make_request('GET', '/findings?cross_host=true')
        
        if success and isinstance(data, list):
            cross_host_findings = [f for f in data if len(f.get('affected_hosts', [])) > 1]
            self.log_test("Cross-Host Findings Filter", True, 
                f"Status: {status}, Cross-host findings: {len(cross_host_findings)}")
        else:
            self.log_test("Cross-Host Findings Filter", False, f"Status: {status}")
        
        # Test finding type filtering
        for finding_type in ['vulnerability', 'misconfiguration', 'compliance']:
            success, data, status = self.make_request('GET', f'/findings?finding_type={finding_type}')
            if success:
                type_findings = [f for f in data if f.get('finding_type') == finding_type]
                self.log_test(f"Findings Filter ({finding_type})", True, 
                    f"Status: {status}, {finding_type} findings: {len(type_findings)}")
            else:
                self.log_test(f"Findings Filter ({finding_type})", False, f"Status: {status}")

    # ===== ANSIBLE REMEDIATION CAPABILITIES =====
    def test_ansible_remediation_generation(self):
        """Test POST /api/findings/{id}/remediation/ansible - Ansible remediation generation"""
        # First ensure we have findings
        success, findings, status = self.make_request('GET', '/findings')
        if not success or not findings:
            self.log_test("Ansible Remediation Generation", False, "No findings available")
            return None
        
        finding_id = findings[0]['id']
        self.created_findings.append(finding_id)
        
        # Test basic Ansible generation
        success, data, status = self.make_request('POST', f'/findings/{finding_id}/remediation/ansible')
        
        if success and 'id' in data:
            self.created_remediations.append(data['id'])
            has_ansible = 'ansible_playbook' in data
            has_inventory = 'ansible_inventory' in data
            has_validation = 'validation_checks' in data
            
            self.log_test("Ansible Remediation Generation", True, 
                f"Status: {status}, Playbook ID: {data['id']}, "
                f"Has Ansible: {has_ansible}, Has Inventory: {has_inventory}")
            return data
        else:
            self.log_test("Ansible Remediation Generation", False, f"Status: {status}, Data: {data}")
            return None

    def test_guided_ansible_remediation(self):
        """Test guided Ansible remediation with step-by-step execution"""
        if not self.created_findings:
            success, findings, status = self.make_request('GET', '/findings')
            if success and findings:
                self.created_findings.append(findings[0]['id'])
        
        if not self.created_findings:
            self.log_test("Guided Ansible Remediation", False, "No findings available")
            return None
        
        finding_id = self.created_findings[0]
        success, data, status = self.make_request('POST', f'/findings/{finding_id}/remediation/ansible?guided=true')
        
        if success and 'guided_steps' in data:
            guided_steps = data['guided_steps']
            self.log_test("Guided Ansible Remediation", True, 
                f"Status: {status}, Guided steps: {len(guided_steps)}")
            return data
        else:
            self.log_test("Guided Ansible Remediation", False, f"Status: {status}, Data: {data}")
            return None

    # ===== CHANGE MANAGEMENT & APPROVAL WORKFLOWS =====
    def test_create_change_request(self):
        """Test POST /api/change-requests - Change management"""
        if not self.created_remediations:
            # Try to create a remediation first
            self.test_ansible_remediation_generation()
        
        if not self.created_remediations:
            self.log_test("Create Change Request", False, "No remediation available")
            return None
        
        change_data = {
            "title": f"Security Remediation Change Request {int(time.time())}",
            "description": "Automated security remediation requiring approval",
            "remediation_id": self.created_remediations[0],
            "requestor": "security-team",
            "priority": "high"
        }
        
        success, data, status = self.make_request('POST', '/change-requests', change_data)
        
        if success and 'id' in data:
            self.created_change_requests.append(data['id'])
            self.log_test("Create Change Request", True, 
                f"Status: {status}, Change Request ID: {data['id']}, Priority: {data.get('priority')}")
            return data
        else:
            self.log_test("Create Change Request", False, f"Status: {status}, Data: {data}")
            return None

    def test_approve_change_request(self):
        """Test POST /api/change-requests/{id}/approve - Approval workflows"""
        if not self.created_change_requests:
            self.test_create_change_request()
        
        if not self.created_change_requests:
            self.log_test("Approve Change Request", False, "No change request available")
            return None
        
        request_id = self.created_change_requests[0]
        approval_data = {
            "approver": "security-manager",
            "approval_notes": "Approved for execution during maintenance window"
        }
        
        success, data, status = self.make_request('POST', f'/change-requests/{request_id}/approve', approval_data)
        
        if success and data.get('status') == 'approved':
            self.log_test("Approve Change Request", True, 
                f"Status: {status}, Approver: {data.get('approver')}")
            return data
        else:
            self.log_test("Approve Change Request", False, f"Status: {status}, Data: {data}")
            return None

    def test_get_change_requests(self):
        """Test GET /api/change-requests - Get change management requests"""
        success, data, status = self.make_request('GET', '/change-requests')
        
        if success and isinstance(data, list):
            pending_requests = [r for r in data if r.get('status') == 'pending']
            approved_requests = [r for r in data if r.get('status') == 'approved']
            
            self.log_test("Get Change Requests", True, 
                f"Status: {status}, Total: {len(data)}, Pending: {len(pending_requests)}, Approved: {len(approved_requests)}")
            return data
        else:
            self.log_test("Get Change Requests", False, f"Status: {status}, Data: {data}")
            return None

    # ===== TICKETING SYSTEM INTEGRATION =====
    def test_create_ticket(self):
        """Test POST /api/tickets - Ticketing integration"""
        if not self.created_findings:
            success, findings, status = self.make_request('GET', '/findings')
            if success and findings:
                self.created_findings.append(findings[0]['id'])
        
        if not self.created_remediations:
            self.test_ansible_remediation_generation()
        
        ticket_data = {
            "title": f"Security Finding Ticket {int(time.time())}",
            "description": "Security vulnerability requiring immediate attention with automated remediation available",
            "finding_id": self.created_findings[0] if self.created_findings else None,
            "remediation_id": self.created_remediations[0] if self.created_remediations else None,
            "priority": "high",
            "external_system": "jira"
        }
        
        success, data, status = self.make_request('POST', '/tickets', ticket_data)
        
        if success and 'id' in data:
            self.created_tickets.append(data['id'])
            has_external_id = 'external_id' in data and data['external_id']
            
            self.log_test("Create Ticket", True, 
                f"Status: {status}, Ticket ID: {data['id']}, External ID: {has_external_id}")
            return data
        else:
            self.log_test("Create Ticket", False, f"Status: {status}, Data: {data}")
            return None

    def test_get_tickets(self):
        """Test GET /api/tickets - Get tickets"""
        success, data, status = self.make_request('GET', '/tickets')
        
        if success and isinstance(data, list):
            open_tickets = [t for t in data if t.get('status') == 'open']
            self.log_test("Get Tickets", True, 
                f"Status: {status}, Total: {len(data)}, Open: {len(open_tickets)}")
            return data
        else:
            self.log_test("Get Tickets", False, f"Status: {status}, Data: {data}")
            return None

    # ===== AUDIT TRAIL =====
    def test_audit_logs(self):
        """Test GET /api/audit-logs - Audit trail"""
        success, data, status = self.make_request('GET', '/audit-logs')
        
        if success and isinstance(data, list):
            recent_logs = [log for log in data if 'timestamp' in log]
            actions = set(log.get('action') for log in data if 'action' in log)
            
            self.log_test("Audit Logs", True, 
                f"Status: {status}, Total logs: {len(data)}, Actions: {len(actions)}")
            return data
        else:
            self.log_test("Audit Logs", False, f"Status: {status}, Data: {data}")
            return None

    def test_filtered_audit_logs(self):
        """Test audit logs with filtering"""
        # Test filtering by action
        for action in ['create', 'scan', 'approve']:
            success, data, status = self.make_request('GET', f'/audit-logs?action={action}')
            if success:
                filtered_logs = [log for log in data if log.get('action') == action]
                self.log_test(f"Audit Logs Filter ({action})", True, 
                    f"Status: {status}, {action} logs: {len(filtered_logs)}")
            else:
                self.log_test(f"Audit Logs Filter ({action})", False, f"Status: {status}")

    # ===== AI-POWERED FEATURES =====
    def test_enhanced_ai_analysis(self):
        """Test enhanced AI vulnerability analysis with cross-host impact"""
        if not self.created_findings:
            success, findings, status = self.make_request('GET', '/findings')
            if success and findings:
                self.created_findings.append(findings[0]['id'])
        
        if not self.created_findings:
            self.log_test("Enhanced AI Analysis", False, "No findings available")
            return None
        
        finding_id = self.created_findings[0]
        success, data, status = self.make_request('POST', f'/findings/{finding_id}/analyze')
        
        if success:
            # Check for enhanced analysis features
            has_cross_host = 'cross_host_impact' in data
            has_compliance = 'compliance_impact' in data
            has_priority_score = 'priority_score' in data
            
            self.log_test("Enhanced AI Analysis", True, 
                f"Status: {status}, Cross-host: {has_cross_host}, "
                f"Compliance: {has_compliance}, Priority: {has_priority_score}")
            return data
        else:
            self.log_test("Enhanced AI Analysis", False, f"Status: {status}, Data: {data}")
            return None

    # ===== COMPREHENSIVE TEST RUNNER =====
    def run_comprehensive_v2_test(self):
        """Run all v2.0 tests in sequence"""
        print("🚀 Starting VulnGuard v2.0 Backend API Tests")
        print("=" * 70)
        
        # Basic connectivity tests
        print("\n📡 Testing Basic Connectivity & v2.0 Features...")
        self.test_health_check()
        self.test_enhanced_dashboard_stats()
        
        # Enhanced asset management tests
        print("\n🏢 Testing Enhanced Asset Management...")
        self.test_create_enhanced_asset()
        
        # Enhanced scanning capabilities
        print("\n🔍 Testing Enhanced Scanning Capabilities...")
        self.test_enhanced_network_scan()
        self.test_configuration_scanning()
        self.test_compliance_scanning()
        
        # Cross-host vulnerability analysis
        print("\n🌐 Testing Cross-Host Vulnerability Analysis...")
        self.test_cross_host_analysis()
        self.test_enhanced_findings_filtering()
        
        # Ansible remediation capabilities
        print("\n🤖 Testing Ansible Remediation Capabilities...")
        print("⏳ Note: AI features may take 10-30 seconds to respond...")
        self.test_ansible_remediation_generation()
        time.sleep(2)  # Brief pause between AI calls
        self.test_guided_ansible_remediation()
        
        # Change management & approval workflows
        print("\n📋 Testing Change Management & Approval Workflows...")
        self.test_create_change_request()
        self.test_approve_change_request()
        self.test_get_change_requests()
        
        # Ticketing system integration
        print("\n🎫 Testing Ticketing System Integration...")
        self.test_create_ticket()
        self.test_get_tickets()
        
        # Audit trail
        print("\n📜 Testing Audit Trail...")
        self.test_audit_logs()
        self.test_filtered_audit_logs()
        
        # Enhanced AI-powered features
        print("\n🧠 Testing Enhanced AI-Powered Features...")
        self.test_enhanced_ai_analysis()
        
        # Print final results
        print("\n" + "=" * 70)
        print("📊 VULNGUARD v2.0 TEST RESULTS SUMMARY")
        print("=" * 70)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        # Print created resources summary
        print(f"\n📝 CREATED RESOURCES:")
        print(f"   Assets: {len(self.created_assets)}")
        print(f"   Scans: {len(self.created_scans)}")
        print(f"   Findings: {len(self.created_findings)}")
        print(f"   Remediations: {len(self.created_remediations)}")
        print(f"   Change Requests: {len(self.created_change_requests)}")
        print(f"   Tickets: {len(self.created_tickets)}")
        
        # Determine overall success
        success_rate = (self.tests_passed/self.tests_run)*100 if self.tests_run > 0 else 0
        overall_success = success_rate >= 80  # 80% success rate threshold
        
        if overall_success:
            print(f"\n🎉 OVERALL RESULT: SUCCESS (≥80% pass rate)")
        else:
            print(f"\n⚠️  OVERALL RESULT: NEEDS ATTENTION (<80% pass rate)")
        
        return overall_success

def main():
    """Main test execution"""
    print("VulnGuard v2.0 Backend API Test Suite")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = VulnGuardV2APITester()
    
    try:
        success = tester.run_comprehensive_v2_test()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())