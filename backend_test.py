#!/usr/bin/env python3
"""
VulnGuard Backend API Testing Suite
Tests all backend endpoints for the vulnerability management platform
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

class VulnGuardAPITester:
    def __init__(self, base_url="https://vulnguard-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.created_assets = []
        self.created_findings = []
        self.created_scans = []

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

    def test_health_check(self):
        """Test API health check endpoint"""
        success, data, status = self.make_request('GET', '/')
        expected_keys = ['message', 'status']
        
        if success and all(key in data for key in expected_keys):
            self.log_test("Health Check", True, f"Status: {status}, Message: {data.get('message')}")
            return True
        else:
            self.log_test("Health Check", False, f"Status: {status}, Data: {data}")
            return False

    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        success, data, status = self.make_request('GET', '/dashboard/stats')
        
        if success and isinstance(data, dict):
            expected_keys = ['total_assets', 'total_findings', 'severity_breakdown']
            has_required_keys = any(key in data for key in expected_keys)
            
            if has_required_keys:
                self.log_test("Dashboard Stats", True, f"Status: {status}, Assets: {data.get('total_assets', 0)}, Findings: {data.get('total_findings', 0)}")
                return True
            else:
                self.log_test("Dashboard Stats", False, f"Missing expected keys. Got: {list(data.keys())}")
                return False
        else:
            self.log_test("Dashboard Stats", False, f"Status: {status}, Data: {data}")
            return False

    def test_create_asset(self):
        """Test asset creation"""
        test_asset = {
            "hostname": f"test-server-{int(time.time())}",
            "ip_address": "192.168.1.100",
            "asset_type": "server",
            "owner": "Test Team",
            "environment": "production",
            "criticality": 2
        }
        
        success, data, status = self.make_request('POST', '/assets', test_asset)
        
        if success and 'id' in data:
            self.created_assets.append(data['id'])
            self.log_test("Create Asset", True, f"Status: {status}, Asset ID: {data['id']}")
            return data
        else:
            self.log_test("Create Asset", False, f"Status: {status}, Data: {data}")
            return None

    def test_get_assets(self):
        """Test retrieving assets"""
        success, data, status = self.make_request('GET', '/assets')
        
        if success and isinstance(data, list):
            self.log_test("Get Assets", True, f"Status: {status}, Count: {len(data)}")
            return data
        else:
            self.log_test("Get Assets", False, f"Status: {status}, Data: {data}")
            return []

    def test_network_scan(self):
        """Test network scanning functionality"""
        scan_data = ["192.168.1.1", "192.168.1.100"]
        
        success, data, status = self.make_request('POST', '/scan/network', scan_data)
        
        if success and 'scan_id' in data:
            self.created_scans.append(data['scan_id'])
            self.log_test("Network Scan", True, f"Status: {status}, Scan ID: {data['scan_id']}, Findings: {data.get('findings_count', 0)}")
            return data
        else:
            self.log_test("Network Scan", False, f"Status: {status}, Data: {data}")
            return None

    def test_file_upload_scan(self):
        """Test file upload scanning"""
        # Create a sample JSON vulnerability file
        sample_vuln_data = {
            "vulnerabilities": [
                {
                    "id": "test-vuln-001",
                    "name": "Test Vulnerability",
                    "description": "This is a test vulnerability for upload testing",
                    "severity": "high",
                    "cve": ["CVE-2024-0001"]
                }
            ]
        }
        
        # Create a temporary file-like object
        json_content = json.dumps(sample_vuln_data)
        
        # First, we need an asset to associate with the scan
        if not self.created_assets:
            asset = self.test_create_asset()
            if not asset:
                self.log_test("File Upload Scan", False, "No asset available for file upload test")
                return None
        
        asset_id = self.created_assets[0]
        
        files = {'file': ('test_scan.json', json_content, 'application/json')}
        form_data = {
            'scan_name': f'Test File Upload {int(time.time())}',
            'asset_id': asset_id
        }
        
        success, data, status = self.make_request('POST', '/scan/upload', form_data, files)
        
        if success and 'scan_id' in data:
            self.created_scans.append(data['scan_id'])
            self.log_test("File Upload Scan", True, f"Status: {status}, Scan ID: {data['scan_id']}, Findings: {data.get('findings_count', 0)}")
            return data
        else:
            self.log_test("File Upload Scan", False, f"Status: {status}, Data: {data}")
            return None

    def test_get_findings(self):
        """Test retrieving vulnerability findings"""
        success, data, status = self.make_request('GET', '/findings')
        
        if success and isinstance(data, list):
            if data:
                self.created_findings.extend([f['id'] for f in data if 'id' in f])
            self.log_test("Get Findings", True, f"Status: {status}, Count: {len(data)}")
            return data
        else:
            self.log_test("Get Findings", False, f"Status: {status}, Data: {data}")
            return []

    def test_ai_analysis(self):
        """Test AI vulnerability analysis"""
        if not self.created_findings:
            findings = self.test_get_findings()
            if not findings:
                self.log_test("AI Analysis", False, "No findings available for AI analysis test")
                return None
        
        finding_id = self.created_findings[0]
        success, data, status = self.make_request('POST', f'/findings/{finding_id}/analyze')
        
        if success:
            self.log_test("AI Analysis", True, f"Status: {status}, Analysis completed")
            return data
        else:
            self.log_test("AI Analysis", False, f"Status: {status}, Data: {data}")
            return None

    def test_remediation_generation(self):
        """Test AI remediation generation"""
        if not self.created_findings:
            findings = self.test_get_findings()
            if not findings:
                self.log_test("Remediation Generation", False, "No findings available for remediation test")
                return None
        
        finding_id = self.created_findings[0]
        success, data, status = self.make_request('POST', f'/findings/{finding_id}/remediation')
        
        if success and 'id' in data:
            self.log_test("Remediation Generation", True, f"Status: {status}, Playbook ID: {data['id']}")
            return data
        else:
            self.log_test("Remediation Generation", False, f"Status: {status}, Data: {data}")
            return None

    def test_cve_intelligence(self):
        """Test CVE intelligence lookup"""
        test_cve = "CVE-2021-44228"  # Log4j vulnerability
        success, data, status = self.make_request('GET', f'/intel/cve/{test_cve}')
        
        if success and 'cve_id' in data:
            self.log_test("CVE Intelligence", True, f"Status: {status}, CVE: {data['cve_id']}, CVSS: {data.get('cvss_score', 'N/A')}")
            return data
        else:
            self.log_test("CVE Intelligence", False, f"Status: {status}, Data: {data}")
            return None

    def test_risk_calculation(self):
        """Test risk score calculation"""
        if not self.created_findings:
            findings = self.test_get_findings()
            if not findings:
                self.log_test("Risk Calculation", False, "No findings available for risk calculation test")
                return None
        
        finding_id = self.created_findings[0]
        success, data, status = self.make_request('POST', f'/risk/calculate/{finding_id}')
        
        if success and 'risk_score' in data:
            self.log_test("Risk Calculation", True, f"Status: {status}, Risk Score: {data['risk_score']}")
            return data
        else:
            self.log_test("Risk Calculation", False, f"Status: {status}, Data: {data}")
            return None

    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("🚀 Starting VulnGuard Backend API Tests")
        print("=" * 60)
        
        # Basic connectivity tests
        print("\n📡 Testing Basic Connectivity...")
        self.test_health_check()
        self.test_dashboard_stats()
        
        # Asset management tests
        print("\n🏢 Testing Asset Management...")
        self.test_create_asset()
        self.test_get_assets()
        
        # Scanning tests
        print("\n🔍 Testing Vulnerability Scanning...")
        self.test_network_scan()
        self.test_file_upload_scan()
        
        # Findings and analysis tests
        print("\n🔎 Testing Findings and Analysis...")
        self.test_get_findings()
        
        # AI-powered features (may take longer)
        print("\n🤖 Testing AI-Powered Features...")
        print("⏳ Note: AI features may take 10-30 seconds to respond...")
        self.test_ai_analysis()
        time.sleep(2)  # Brief pause between AI calls
        self.test_remediation_generation()
        
        # Intelligence and risk features
        print("\n📊 Testing Intelligence and Risk Features...")
        self.test_cve_intelligence()
        self.test_risk_calculation()
        
        # Print final results
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.created_assets:
            print(f"\n📝 Created Assets: {len(self.created_assets)}")
        if self.created_scans:
            print(f"📝 Created Scans: {len(self.created_scans)}")
        if self.created_findings:
            print(f"📝 Found Findings: {len(self.created_findings)}")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    print("VulnGuard Backend API Test Suite")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = VulnGuardAPITester()
    
    try:
        success = tester.run_comprehensive_test()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())