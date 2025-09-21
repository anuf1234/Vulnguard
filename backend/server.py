from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timezone
from enum import Enum
import os
import logging
import uuid
import json
import aiofiles
import asyncio
import requests
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Load environment
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# FastAPI app setup
app = FastAPI(title="VulnGuard - Vulnerability Management Platform", version="2.0.0")
api_router = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enums
class ScanType(str, Enum):
    NETWORK = "network"
    HOST = "host"
    CONTAINER = "container"
    CLOUD = "cloud"
    FILE_BASED = "file_based"
    CONFIGURATION = "configuration"
    COMPLIANCE = "compliance"

class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class FindingType(str, Enum):
    VULNERABILITY = "vulnerability"
    MISCONFIGURATION = "misconfiguration"
    COMPLIANCE = "compliance"
    POLICY_VIOLATION = "policy_violation"

class RemediationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    APPROVED = "approved"
    REJECTED = "rejected"

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class AuditAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    SCAN = "scan"
    REMEDIATE = "remediate"
    APPROVE = "approve"
    REJECT = "reject"

# Enhanced Data Models
class Asset(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hostname: str
    ip_address: Optional[str] = None
    asset_type: str
    owner: Optional[str] = None
    environment: str = "production"
    criticality: int = Field(default=3, ge=1, le=5)
    tags: List[str] = []
    operating_system: Optional[str] = None
    location: Optional[str] = None
    business_unit: Optional[str] = None
    compliance_requirements: List[str] = []
    last_scan: Optional[datetime] = None
    configuration_baseline: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class VulnerabilityIntel(BaseModel):
    cve_id: str
    cvss_score: float
    cvss_vector: Optional[str] = None
    epss_score: Optional[float] = None
    kev_catalog: bool = False
    description: str
    severity: RiskLevel
    published_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    references: List[str] = []
    exploit_available: bool = False
    patch_available: bool = False

class Finding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str
    plugin_id: str
    title: str
    description: str
    finding_type: FindingType = FindingType.VULNERABILITY
    cve_ids: List[str] = []
    risk_score: float = 0.0
    severity: RiskLevel
    category: Optional[str] = None
    compliance_frameworks: List[str] = []
    affected_hosts: List[str] = []
    first_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "open"
    raw_output: Optional[Dict[str, Any]] = None
    remediation_notes: Optional[str] = None
    business_impact: Optional[str] = None
    exploit_likelihood: Optional[str] = None

class RemediationPlaybook(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    finding_id: str
    title: str
    description: str
    ansible_playbook: Optional[str] = None
    ansible_inventory: Optional[str] = None
    powershell_script: Optional[str] = None
    bash_script: Optional[str] = None
    manual_steps: List[str] = []
    guided_steps: List[Dict[str, Any]] = []
    estimated_time: Optional[int] = None
    risk_level: RiskLevel
    requires_approval: bool = True
    validation_checks: List[str] = []
    rollback_plan: Optional[str] = None
    affected_systems: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AuditLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    action: AuditAction
    resource_type: str
    resource_id: str
    details: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChangeRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    remediation_id: str
    affected_systems: List[str]
    requestor: str
    approver: Optional[str] = None
    status: RemediationStatus = RemediationStatus.PENDING
    priority: RiskLevel
    scheduled_time: Optional[datetime] = None
    maintenance_window: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    approved_at: Optional[datetime] = None

class Ticket(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    external_id: Optional[str] = None
    title: str
    description: str
    finding_id: Optional[str] = None
    remediation_id: Optional[str] = None
    assignee: Optional[str] = None
    status: TicketStatus = TicketStatus.OPEN
    priority: RiskLevel
    external_system: Optional[str] = None  # jira, servicenow, etc.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ScanJob(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    scan_type: ScanType
    targets: List[str]
    scan_config: Optional[Dict[str, Any]] = None
    status: str = "pending"
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    findings_count: int = 0
    misconfigs_count: int = 0
    error_message: Optional[str] = None
    created_by: Optional[str] = None

class ConfigurationBaseline(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str
    baseline_name: str
    configuration_items: List[Dict[str, Any]]
    compliance_framework: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# === COMPLIANCE MAPPING FRAMEWORK ===

class ComplianceFramework(str, Enum):
    NIST_800_53 = "nist_800_53"
    ISO_27001 = "iso_27001"
    HIPAA = "hipaa"
    FEDRAMP = "fedramp"
    SOC2 = "soc2"
    PCI_DSS = "pci_dss" 
    CIS = "cis"
    GDPR = "gdpr"
    CMMC = "cmmc"

class ComplianceControl(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    framework: ComplianceFramework
    control_id: str  # e.g., "AC-2", "A.9.2.1", "45 CFR 164.308(a)(4)"
    control_title: str
    control_description: str
    control_family: Optional[str] = None  # e.g., "Access Control", "Cryptography"
    implementation_guidance: Optional[str] = None
    assessment_procedures: List[str] = []
    related_controls: List[str] = []
    priority: RiskLevel = RiskLevel.MEDIUM
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ComplianceMapping(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    finding_type: str  # vulnerability type or misconfiguration category
    cve_pattern: Optional[str] = None  # regex pattern for CVE matching
    compliance_controls: List[Dict[str, Any]]  # [{framework: "", control_id: "", relevance_score: 0.9}]
    mapping_confidence: float = 0.0  # 0.0-1.0 confidence in mapping accuracy
    business_impact: Optional[str] = None
    remediation_priority: RiskLevel = RiskLevel.MEDIUM
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ComplianceAssessment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str
    framework: ComplianceFramework
    assessment_name: str
    scope_description: str
    assets_in_scope: List[str] = []
    control_assessments: List[Dict[str, Any]] = []  # [{control_id: "", status: "", evidence: ""}]
    overall_score: float = 0.0  # percentage compliance
    gaps_identified: List[Dict[str, Any]] = []
    remediation_plan: Optional[str] = None
    assessor: Optional[str] = None
    assessment_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    next_assessment_due: Optional[datetime] = None
    status: str = "in_progress"  # draft, in_progress, completed, approved

# === RISK-BASED PRIORITIZATION ===

class RiskFactor(BaseModel):
    factor_name: str
    weight: float  # 0.0-1.0
    value: float   # 0.0-1.0
    description: Optional[str] = None

class RiskAssessment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    finding_id: str
    asset_id: str
    cvss_score: Optional[float] = None
    epss_score: Optional[float] = None  # Exploit Prediction Scoring System
    kev_listed: bool = False  # CISA Known Exploited Vulnerabilities
    asset_criticality: RiskLevel = RiskLevel.MEDIUM
    business_impact_score: float = 0.0
    exploit_likelihood: float = 0.0
    environmental_factors: List[RiskFactor] = []
    compensating_controls: List[str] = []
    final_risk_score: float = 0.0
    risk_category: RiskLevel = RiskLevel.MEDIUM
    justification: Optional[str] = None
    calculated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# === AUTOMATED REMEDIATION ===

class RemediationType(str, Enum):
    ANSIBLE = "ansible"
    TERRAFORM = "terraform"
    POWERSHELL = "powershell"
    BASH = "bash"
    MANUAL = "manual"
    API_CALL = "api_call"

class RemediationTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    remediation_type: RemediationType
    template_content: str  # Jinja2 template
    supported_platforms: List[str] = []  # ["linux", "windows", "cloud"]
    required_parameters: List[Dict[str, Any]] = []
    validation_commands: List[str] = []
    rollback_commands: List[str] = []
    estimated_duration: Optional[int] = None  # minutes
    risk_level: RiskLevel = RiskLevel.MEDIUM
    requires_approval: bool = True
    tags: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AutomatedRemediation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    finding_id: str
    template_id: str
    target_systems: List[str]
    remediation_script: str  # Generated from template
    parameters: Dict[str, Any] = {}
    execution_status: RemediationStatus = RemediationStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_log: List[Dict[str, Any]] = []  # [{timestamp, level, message, system}]
    success_rate: float = 0.0  # percentage of successful executions
    rollback_available: bool = False
    approval_required: bool = True
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

# === CONTINUOUS MONITORING ===

class MonitoringAgent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str
    agent_version: str
    platform: str  # linux, windows, container
    deployment_method: str  # agent, agentless, api
    status: str = "active"  # active, inactive, error
    last_checkin: Optional[datetime] = None
    capabilities: List[str] = []  # ["vulnerability_scan", "config_monitor", "file_integrity"]
    configuration: Dict[str, Any] = {}
    installed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MonitoringData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    asset_id: str
    data_type: str  # "vulnerability", "configuration", "file_integrity", "process", "network"
    data_payload: Dict[str, Any]
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed: bool = False
    alerts_generated: List[str] = []

# === INTEGRATION APIS ===

class IntegrationType(str, Enum):
    SIEM = "siem"
    TICKETING = "ticketing" 
    CLOUD = "cloud"
    NOTIFICATION = "notification"
    IDENTITY = "identity"

class IntegrationConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    integration_type: IntegrationType
    provider: str  # "splunk", "elk", "jira", "servicenow", "aws", "azure", "gcp"
    configuration: Dict[str, Any] = {}  # provider-specific config
    authentication: Dict[str, Any] = {}  # credentials, tokens, etc.
    enabled: bool = True
    sync_frequency: Optional[int] = None  # minutes
    last_sync: Optional[datetime] = None
    sync_status: str = "healthy"  # healthy, error, disabled
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class IntegrationEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    integration_id: str
    event_type: str  # "finding_created", "remediation_completed", "compliance_gap"
    payload: Dict[str, Any]
    external_id: Optional[str] = None  # ID in external system
    sync_status: str = "pending"  # pending, success, failed
    retry_count: int = 0
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    synced_at: Optional[datetime] = None

# === MULTI-TENANT SUPPORT ===

class Organization(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    display_name: str
    domain: Optional[str] = None
    subscription_tier: str = "free"  # free, professional, enterprise
    max_assets: Optional[int] = None
    max_users: Optional[int] = None
    features_enabled: List[str] = []
    compliance_frameworks: List[ComplianceFramework] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: str
    organization_id: str
    role: str = "analyst"  # admin, manager, analyst, viewer
    permissions: List[str] = []
    last_login: Optional[datetime] = None
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MSPClient(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    msp_organization_id: str  # MSP's organization ID
    client_organization_id: str  # Client's organization ID
    client_name: str
    service_level: str = "basic"  # basic, premium, enterprise
    billing_contact: Optional[str] = None
    technical_contact: Optional[str] = None
    asset_allocation: Optional[int] = None
    compliance_requirements: List[ComplianceFramework] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Enhanced LLM Integration
class VulnAnalyzer:
    def __init__(self):
        self.llm = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id="vuln-analyzer-v2",
            system_message="""You are a senior cybersecurity expert and DevOps engineer specializing in vulnerability analysis, 
            misconfiguration detection, and Ansible-based remediation. You have deep expertise in:
            - Vulnerability assessment and risk analysis
            - Infrastructure misconfiguration detection
            - Compliance framework mapping (CIS, NIST, SOX, PCI-DSS)
            - Ansible playbook development and automation
            - Cross-platform remediation strategies
            - Change management and approval workflows"""
        ).with_model("openai", "gpt-4o")
    
    async def analyze_vulnerability(self, finding_data: Dict) -> Dict:
        """Enhanced AI-powered vulnerability analysis"""
        try:
            prompt = f"""
            Analyze this security finding in detail:
            
            Title: {finding_data.get('title')}
            Description: {finding_data.get('description')}
            Type: {finding_data.get('finding_type', 'vulnerability')}
            CVE IDs: {finding_data.get('cve_ids', [])}
            Asset Type: {finding_data.get('asset_type')}
            Affected Hosts: {finding_data.get('affected_hosts', [])}
            
            Provide comprehensive analysis:
            1. Detailed risk assessment and CVSS analysis
            2. Exploitability assessment and attack vectors
            3. Business impact analysis and affected services
            4. Cross-host impact assessment
            5. Compliance implications (CIS, NIST, PCI-DSS, SOX)
            6. Prioritization recommendation with justification
            7. Suggested remediation timeline
            
            Respond in JSON format with keys: 
            risk_analysis, exploitability, business_impact, cross_host_impact, 
            compliance_impact, priority_score (1-10), recommended_timeline_days, attack_vectors
            """
            
            message = UserMessage(text=prompt)
            response = await self.llm.send_message(message)
            
            try:
                return json.loads(response)
            except:
                return {"analysis": response, "priority_score": 5}
                
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return {"error": str(e), "priority_score": 5}
    
    async def generate_ansible_remediation(self, finding_data: Dict, asset_data: Dict, guided: bool = False) -> Dict:
        """Generate comprehensive Ansible remediation with guided steps"""
        try:
            prompt = f"""
            Generate comprehensive Ansible remediation for this security finding:
            
            Finding: {finding_data.get('title')}
            Description: {finding_data.get('description')}
            Type: {finding_data.get('finding_type', 'vulnerability')}
            CVE IDs: {finding_data.get('cve_ids', [])}
            
            Asset Details:
            - Hostname: {asset_data.get('hostname')}
            - OS: {asset_data.get('operating_system', 'Linux')}
            - Environment: {asset_data.get('environment')}
            - Criticality: {asset_data.get('criticality')}
            
            Generate:
            1. Complete Ansible playbook with proper structure
            2. Ansible inventory file for target hosts
            3. Pre-execution validation checks
            4. Post-execution verification tasks
            5. Rollback playbook for failure scenarios
            6. Manual guided steps for complex procedures
            7. Estimated execution time and risk assessment
            8. Required approvals and change management notes
            
            {"Include step-by-step guided execution if requested." if guided else ""}
            
            Format as JSON with keys: 
            ansible_playbook, ansible_inventory, pre_checks, post_checks, 
            rollback_playbook, guided_steps, estimated_minutes, risk_assessment,
            change_management_notes, required_approvals
            """
            
            message = UserMessage(text=prompt)
            response = await self.llm.send_message(message)
            
            try:
                return json.loads(response)
            except:
                return {"ansible_playbook": response, "estimated_minutes": 30}
                
        except Exception as e:
            logger.error(f"Ansible remediation generation failed: {e}")
            return {"error": str(e), "ansible_playbook": "# Manual remediation required"}

    async def detect_misconfigurations(self, config_data: Dict, asset_type: str) -> List[Dict]:
        """AI-powered misconfiguration detection"""
        try:
            prompt = f"""
            Analyze this system configuration for security misconfigurations:
            
            Asset Type: {asset_type}
            Configuration Data: {json.dumps(config_data, indent=2)}
            
            Detect and analyze:
            1. Security misconfigurations and policy violations
            2. Compliance deviations (CIS benchmarks, NIST guidelines)
            3. Hardening opportunities and best practices
            4. Access control and permission issues
            5. Network security configurations
            6. Service and application misconfigurations
            
            For each misconfiguration found, provide:
            - Title and detailed description
            - Risk level and business impact
            - Compliance framework violations
            - Specific remediation steps
            - Ansible automation potential
            
            Respond as JSON array of misconfiguration objects with keys:
            title, description, risk_level, compliance_violations, 
            remediation_steps, ansible_remediable, business_impact
            """
            
            message = UserMessage(text=prompt)
            response = await self.llm.send_message(message)
            
            try:
                return json.loads(response)
            except:
                return []
                
        except Exception as e:
            logger.error(f"Misconfiguration detection failed: {e}")
            return []

# CVE/NVD Integration - Enhanced
class CVEIntegrator:
    def __init__(self):
        self.nvd_base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.cve_api_url = "https://cvedb.shodan.io/cve"
        self.exploit_db_url = "https://www.exploit-db.com/api/v1/search"
    
    async def fetch_cve_details(self, cve_id: str) -> Optional[VulnerabilityIntel]:
        """Enhanced CVE details with exploit information"""
        try:
            # Try NVD API first
            response = requests.get(f"{self.nvd_base_url}?cveId={cve_id}")
            if response.status_code == 200:
                data = response.json()
                if data.get('vulnerabilities'):
                    vuln_data = data['vulnerabilities'][0]['cve']
                    
                    # Extract CVSS score
                    cvss_score = 0.0
                    cvss_vector = None
                    if 'metrics' in vuln_data:
                        if 'cvssMetricV31' in vuln_data['metrics']:
                            cvss_data = vuln_data['metrics']['cvssMetricV31'][0]['cvssData']
                            cvss_score = cvss_data.get('baseScore', 0.0)
                            cvss_vector = cvss_data.get('vectorString')
                        elif 'cvssMetricV2' in vuln_data['metrics']:
                            cvss_data = vuln_data['metrics']['cvssMetricV2'][0]['cvssData']
                            cvss_score = cvss_data.get('baseScore', 0.0)
                            cvss_vector = cvss_data.get('vectorString')
                    
                    # Check for available exploits
                    exploit_available = await self.check_exploit_availability(cve_id)
                    
                    # Determine severity
                    if cvss_score >= 9.0:
                        severity = RiskLevel.CRITICAL
                    elif cvss_score >= 7.0:
                        severity = RiskLevel.HIGH
                    elif cvss_score >= 4.0:
                        severity = RiskLevel.MEDIUM
                    else:
                        severity = RiskLevel.LOW
                    
                    return VulnerabilityIntel(
                        cve_id=cve_id,
                        cvss_score=cvss_score,
                        cvss_vector=cvss_vector,
                        description=vuln_data['descriptions'][0]['value'],
                        severity=severity,
                        published_date=datetime.fromisoformat(vuln_data['published'].replace('Z', '+00:00')),
                        modified_date=datetime.fromisoformat(vuln_data['lastModified'].replace('Z', '+00:00')),
                        references=[ref['url'] for ref in vuln_data.get('references', [])],
                        exploit_available=exploit_available,
                        patch_available=True  # Assume patch available if in NVD
                    )
                
        except Exception as e:
            logger.error(f"Failed to fetch CVE {cve_id}: {e}")
        
        return None
    
    async def check_exploit_availability(self, cve_id: str) -> bool:
        """Check if exploits are available for this CVE"""
        try:
            # Check exploit-db for available exploits
            response = requests.get(f"{self.exploit_db_url}?cve={cve_id}")
            if response.status_code == 200:
                data = response.json()
                return len(data.get('data', [])) > 0
        except:
            pass
        return False

# Enhanced Risk Scoring Engine
class RiskEngine:
    def __init__(self):
        self.vuln_analyzer = VulnAnalyzer()
    
    async def calculate_comprehensive_risk_score(self, finding: Finding, asset: Asset, vuln_intel: Optional[VulnerabilityIntel] = None) -> Dict[str, Any]:
        """Calculate comprehensive risk score with multiple factors"""
        try:
            # Base CVSS score (0-30 points)
            cvss_score = 0.0
            if vuln_intel and vuln_intel.cvss_score:
                cvss_score = (vuln_intel.cvss_score / 10.0) * 30
            
            # EPSS score (0-20 points)
            epss_score = 0.0
            if vuln_intel and vuln_intel.epss_score:
                epss_score = vuln_intel.epss_score * 20
            
            # KEV catalog (0-15 points)
            kev_score = 15 if vuln_intel and vuln_intel.kev_catalog else 0
            
            # Exploit availability (0-10 points)
            exploit_score = 10 if vuln_intel and vuln_intel.exploit_available else 0
            
            # Asset criticality (0-10 points)
            criticality_score = (6 - asset.criticality) * 2
            
            # Environment factor (0-10 points)
            env_multiplier = {"production": 1.0, "staging": 0.6, "development": 0.3}
            environment_score = env_multiplier.get(asset.environment, 0.5) * 10
            
            # Cross-host impact (0-5 points)
            cross_host_score = min(len(finding.affected_hosts) * 1, 5)
            
            # Total risk score
            total_score = cvss_score + epss_score + kev_score + exploit_score + criticality_score + environment_score + cross_host_score
            
            # Normalize to 0-100 scale
            normalized_score = min(total_score, 100.0)
            
            return {
                "total_risk_score": normalized_score,
                "components": {
                    "cvss_contribution": cvss_score,
                    "epss_contribution": epss_score,
                    "kev_contribution": kev_score,
                    "exploit_contribution": exploit_score,
                    "criticality_contribution": criticality_score,
                    "environment_contribution": environment_score,
                    "cross_host_contribution": cross_host_score
                },
                "risk_category": self.get_risk_category(normalized_score),
                "recommended_sla": self.get_recommended_sla(normalized_score)
            }
            
        except Exception as e:
            logger.error(f"Risk calculation failed: {e}")
            return {
                "total_risk_score": 50.0,
                "components": {},
                "risk_category": "medium",
                "recommended_sla": "30 days"
            }
    
    def get_risk_category(self, score: float) -> str:
        """Get risk category based on score"""
        if score >= 85:
            return "critical"
        elif score >= 70:
            return "high"
        elif score >= 40:
            return "medium"
        else:
            return "low"
    
    def get_recommended_sla(self, score: float) -> str:
        """Get recommended SLA based on risk score"""
        if score >= 85:
            return "24 hours"
        elif score >= 70:
            return "7 days"
        elif score >= 40:
            return "30 days"
        else:
            return "90 days"

# Ticketing Integration
class TicketingIntegration:
    def __init__(self):
        self.jira_url = os.environ.get('JIRA_URL')
        self.jira_token = os.environ.get('JIRA_TOKEN')
        self.servicenow_url = os.environ.get('SERVICENOW_URL')
        self.servicenow_token = os.environ.get('SERVICENOW_TOKEN')
    
    async def create_jira_ticket(self, finding: Finding, remediation: RemediationPlaybook) -> Optional[str]:
        """Create JIRA ticket for remediation"""
        if not self.jira_url or not self.jira_token:
            return None
        
        try:
            ticket_data = {
                "fields": {
                    "project": {"key": os.environ.get('JIRA_PROJECT', 'SEC')},
                    "summary": f"Security Finding: {finding.title}",
                    "description": f"""
Security Finding Details:
- Finding ID: {finding.id}
- Severity: {finding.severity}
- Asset: {finding.asset_id}
- CVE IDs: {', '.join(finding.cve_ids)}

Description: {finding.description}

Remediation Playbook: {remediation.id}
Estimated Time: {remediation.estimated_time} minutes

Ansible Playbook Available: {'Yes' if remediation.ansible_playbook else 'No'}
                    """,
                    "issuetype": {"name": "Task"},
                    "priority": {"name": self.get_jira_priority(finding.severity)}
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.jira_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.jira_url}/rest/api/2/issue",
                json=ticket_data,
                headers=headers
            )
            
            if response.status_code == 201:
                return response.json().get('key')
                
        except Exception as e:
            logger.error(f"JIRA ticket creation failed: {e}")
        
        return None
    
    def get_jira_priority(self, severity: RiskLevel) -> str:
        """Convert severity to JIRA priority"""
        mapping = {
            RiskLevel.CRITICAL: "Highest",
            RiskLevel.HIGH: "High",
            RiskLevel.MEDIUM: "Medium",
            RiskLevel.LOW: "Low",
            RiskLevel.INFO: "Lowest"
        }
        return mapping.get(severity, "Medium")

# Initialize services
vuln_analyzer = VulnAnalyzer()
cve_integrator = CVEIntegrator()
risk_engine = RiskEngine()
ticketing = TicketingIntegration()

# Helper functions for audit logging
async def log_audit(user_id: str, action: AuditAction, resource_type: str, resource_id: str, details: Dict[str, Any], ip_address: str = None):
    """Log audit events"""
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address
    )
    await db.audit_logs.insert_one(audit_log.dict())

# Enhanced API Endpoints

@api_router.get("/")
async def root():
    return {"message": "VulnGuard API v2.0.0", "status": "operational", "features": ["vulnerability_scanning", "misconfiguration_detection", "ansible_remediation", "audit_trails", "cross_host_tracking", "change_management", "ticketing_integration"]}

# Asset Management with Enhanced Features
@api_router.post("/assets", response_model=Asset)
async def create_asset(asset_data: Asset):
    asset_dict = asset_data.dict()
    asset_dict["updated_at"] = datetime.now(timezone.utc)
    await db.assets.insert_one(asset_dict)
    
    # Log audit event
    await log_audit("system", AuditAction.CREATE, "asset", asset_data.id, {"hostname": asset_data.hostname})
    
    return asset_data

@api_router.get("/assets", response_model=List[Asset])
async def get_assets(business_unit: Optional[str] = None, environment: Optional[str] = None):
    query = {}
    if business_unit:
        query["business_unit"] = business_unit
    if environment:
        query["environment"] = environment
    
    assets = await db.assets.find(query).to_list(1000)
    return [Asset(**asset) for asset in assets]

@api_router.get("/assets/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):
    asset = await db.assets.find_one({"id": asset_id})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return Asset(**asset)

# Enhanced Scanning with Misconfiguration Detection
@api_router.post("/scan/configuration")
async def scan_configuration(asset_id: str, config_data: Dict[str, Any]):
    """Scan for security misconfigurations"""
    try:
        asset = await db.assets.find_one({"id": asset_id})
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        # Detect misconfigurations using AI
        misconfigs = await vuln_analyzer.detect_misconfigurations(config_data, asset["asset_type"])
        
        # Create findings for each misconfiguration
        findings = []
        for misconfig in misconfigs:
            finding = Finding(
                asset_id=asset_id,
                plugin_id="config-analyzer",
                title=misconfig.get("title", "Configuration Issue"),
                description=misconfig.get("description", ""),
                finding_type=FindingType.MISCONFIGURATION,
                severity=RiskLevel(misconfig.get("risk_level", "medium").lower()),
                compliance_frameworks=misconfig.get("compliance_violations", []),
                business_impact=misconfig.get("business_impact")
            )
            findings.append(finding)
            await db.findings.insert_one(finding.dict())
        
        # Log audit event
        await log_audit("system", AuditAction.SCAN, "asset", asset_id, {"misconfigs_found": len(misconfigs)})
        
        return {
            "asset_id": asset_id,
            "misconfigurations_found": len(misconfigs),
            "findings": [f.id for f in findings]
        }
        
    except Exception as e:
        logger.error(f"Configuration scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/scan/compliance")
async def scan_compliance(asset_ids: List[str], framework: str = "CIS"):
    """Scan for compliance violations"""
    try:
        compliance_findings = []
        
        for asset_id in asset_ids:
            asset = await db.assets.find_one({"id": asset_id})
            if not asset:
                continue
            
            # Mock compliance scan - in production, integrate with actual compliance tools
            mock_violations = [
                {
                    "title": f"{framework} - Password Policy Violation",
                    "description": f"System does not meet {framework} password complexity requirements",
                    "control_id": f"{framework}-5.1.1",
                    "severity": "medium"
                },
                {
                    "title": f"{framework} - Audit Logging Not Configured",
                    "description": f"System audit logging not configured per {framework} guidelines",
                    "control_id": f"{framework}-8.2.1",
                    "severity": "high"
                }
            ]
            
            for violation in mock_violations:
                finding = Finding(
                    asset_id=asset_id,
                    plugin_id=f"compliance-{framework.lower()}",
                    title=violation["title"],
                    description=violation["description"],
                    finding_type=FindingType.COMPLIANCE,
                    severity=RiskLevel(violation["severity"]),
                    compliance_frameworks=[framework],
                    category=violation.get("control_id")
                )
                compliance_findings.append(finding)
                await db.findings.insert_one(finding.dict())
        
        return {
            "framework": framework,
            "assets_scanned": len(asset_ids),
            "violations_found": len(compliance_findings),
            "findings": [f.id for f in compliance_findings]
        }
        
    except Exception as e:
        logger.error(f"Compliance scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced Network Scanning
@api_router.post("/scan/network")
async def simulate_network_scan(request_data: Dict[str, Any]):
    """Enhanced network vulnerability scanning with misconfiguration detection"""
    try:
        targets = request_data.get("targets", [])
        scan_name = request_data.get("scan_name", "Network Discovery")
        include_misconfigs = request_data.get("include_misconfigs", True)
        
        scan_job = ScanJob(
            name=scan_name,
            scan_type=ScanType.NETWORK,
            targets=targets,
            status="running",
            started_at=datetime.now(timezone.utc)
        )
        await db.scan_jobs.insert_one(scan_job.dict())
        
        # Generate mock findings (vulnerabilities and misconfigurations)
        mock_findings = await generate_enhanced_mock_findings(targets, scan_job.id, include_misconfigs)
        
        # Store findings
        vuln_count = 0
        misconfig_count = 0
        for finding in mock_findings:
            await db.findings.insert_one(finding.dict())
            if finding.finding_type == FindingType.VULNERABILITY:
                vuln_count += 1
            elif finding.finding_type == FindingType.MISCONFIGURATION:
                misconfig_count += 1
        
        # Update scan job
        await db.scan_jobs.update_one(
            {"id": scan_job.id},
            {"$set": {
                "status": "completed",
                "completed_at": datetime.now(timezone.utc),
                "findings_count": vuln_count,
                "misconfigs_count": misconfig_count
            }}
        )
        
        # Log audit event
        await log_audit("system", AuditAction.SCAN, "network", scan_job.id, {
            "targets": targets,
            "vulnerabilities": vuln_count,
            "misconfigurations": misconfig_count
        })
        
        return {
            "scan_id": scan_job.id,
            "status": "completed",
            "findings_count": len(mock_findings),
            "vulnerabilities": vuln_count,
            "misconfigurations": misconfig_count
        }
        
    except Exception as e:
        logger.error(f"Network scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced Findings Management with Cross-Host Tracking
@api_router.get("/findings", response_model=List[Finding])
async def get_findings(
    asset_id: Optional[str] = None,
    severity: Optional[RiskLevel] = None,
    finding_type: Optional[FindingType] = None,
    cross_host: bool = False,
    limit: int = 100
):
    query = {}
    if asset_id:
        query["asset_id"] = asset_id
    if severity:
        query["severity"] = severity
    if finding_type:
        query["finding_type"] = finding_type
    if cross_host:
        query["affected_hosts.1"] = {"$exists": True}  # Has at least 2 affected hosts
    
    findings = await db.findings.find(query).limit(limit).to_list(limit)
    return [Finding(**finding) for finding in findings]

@api_router.get("/findings/cross-host-analysis")
async def get_cross_host_analysis():
    """Analyze findings that affect multiple hosts"""
    try:
        # Aggregate findings by CVE across hosts
        pipeline = [
            {"$match": {"cve_ids": {"$ne": []}}},
            {"$unwind": "$cve_ids"},
            {"$group": {
                "_id": "$cve_ids",
                "affected_assets": {"$addToSet": "$asset_id"},
                "total_instances": {"$sum": 1},
                "max_severity": {"$max": "$severity"},
                "finding_ids": {"$push": "$id"}
            }},
            {"$match": {"total_instances": {"$gt": 1}}},
            {"$sort": {"total_instances": -1}},
            {"$limit": 20}
        ]
        
        cross_host_vulns = await db.findings.aggregate(pipeline).to_list(20)
        
        return {
            "cross_host_vulnerabilities": cross_host_vulns,
            "summary": {
                "total_cross_host_vulns": len(cross_host_vulns),
                "most_widespread": cross_host_vulns[0] if cross_host_vulns else None
            }
        }
        
    except Exception as e:
        logger.error(f"Cross-host analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced AI Analysis and Ansible Remediation
@api_router.post("/findings/{finding_id}/analyze")
async def analyze_finding(finding_id: str):
    """Enhanced AI-powered vulnerability analysis"""
    finding = await db.findings.find_one({"id": finding_id})
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    asset = await db.assets.find_one({"id": finding["asset_id"]})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Enhanced analysis including cross-host impact
    analysis = await vuln_analyzer.analyze_vulnerability({
        **finding,
        "asset_type": asset.get("asset_type"),
        "environment": asset.get("environment")
    })
    
    # Update finding with analysis
    await db.findings.update_one(
        {"id": finding_id},
        {"$set": {"ai_analysis": analysis, "updated_at": datetime.now(timezone.utc)}}
    )
    
    # Log audit event
    await log_audit("system", AuditAction.UPDATE, "finding", finding_id, {"analysis_completed": True})
    
    return analysis

@api_router.post("/findings/{finding_id}/remediation/ansible", response_model=RemediationPlaybook)
async def generate_ansible_remediation(finding_id: str, guided: bool = False):
    """Generate comprehensive Ansible remediation playbooks"""
    finding = await db.findings.find_one({"id": finding_id})
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    asset = await db.assets.find_one({"id": finding["asset_id"]})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Generate Ansible remediation
    remediation_data = await vuln_analyzer.generate_ansible_remediation(finding, asset, guided)
    
    # Get affected systems for multi-host remediation
    affected_systems = []
    if finding.get("cve_ids"):
        # Find other assets with the same CVE
        related_findings = await db.findings.find({
            "cve_ids": {"$in": finding["cve_ids"]},
            "id": {"$ne": finding_id}
        }).to_list(100)
        affected_systems = list(set([f["asset_id"] for f in related_findings]))
    
    playbook = RemediationPlaybook(
        finding_id=finding_id,
        title=f"Ansible Remediation: {finding['title']}",
        description=f"AI-generated Ansible remediation for {finding['title']}",
        ansible_playbook=remediation_data.get("ansible_playbook"),
        ansible_inventory=remediation_data.get("ansible_inventory"),
        manual_steps=remediation_data.get("manual_steps", []),
        guided_steps=remediation_data.get("guided_steps", []),
        estimated_time=remediation_data.get("estimated_minutes", 30),
        risk_level=RiskLevel(finding["severity"]),
        validation_checks=remediation_data.get("pre_checks", []),
        rollback_plan=remediation_data.get("rollback_playbook"),
        affected_systems=affected_systems,
        requires_approval=finding["severity"] in ["critical", "high"]
    )
    
    await db.remediation_playbooks.insert_one(playbook.dict())
    
    # Log audit event
    await log_audit("system", AuditAction.CREATE, "remediation", playbook.id, {
        "finding_id": finding_id,
        "type": "ansible",
        "guided": guided
    })
    
    return playbook

# Change Management and Approval Workflows
@api_router.post("/change-requests", response_model=ChangeRequest)
async def create_change_request(
    title: str,
    description: str,
    remediation_id: str,
    requestor: str,
    priority: RiskLevel,
    scheduled_time: Optional[datetime] = None
):
    """Create change management request for remediation"""
    remediation = await db.remediation_playbooks.find_one({"id": remediation_id})
    if not remediation:
        raise HTTPException(status_code=404, detail="Remediation playbook not found")
    
    change_request = ChangeRequest(
        title=title,
        description=description,
        remediation_id=remediation_id,
        affected_systems=remediation.get("affected_systems", []),
        requestor=requestor,
        priority=priority,
        scheduled_time=scheduled_time
    )
    
    await db.change_requests.insert_one(change_request.dict())
    
    # Log audit event
    await log_audit(requestor, AuditAction.CREATE, "change_request", change_request.id, {
        "remediation_id": remediation_id,
        "priority": priority
    })
    
    return change_request

@api_router.post("/change-requests/{request_id}/approve")
async def approve_change_request(request_id: str, approver: str, approval_notes: Optional[str] = None):
    """Approve change management request"""
    change_request = await db.change_requests.find_one({"id": request_id})
    if not change_request:
        raise HTTPException(status_code=404, detail="Change request not found")
    
    await db.change_requests.update_one(
        {"id": request_id},
        {"$set": {
            "status": RemediationStatus.APPROVED,
            "approver": approver,
            "approved_at": datetime.now(timezone.utc),
            "approval_notes": approval_notes
        }}
    )
    
    # Log audit event
    await log_audit(approver, AuditAction.APPROVE, "change_request", request_id, {
        "notes": approval_notes
    })
    
    return {"status": "approved", "approver": approver}

@api_router.get("/change-requests")
async def get_change_requests(status: Optional[RemediationStatus] = None):
    """Get change management requests"""
    query = {}
    if status:
        query["status"] = status
    
    requests = await db.change_requests.find(query).to_list(100)
    return [ChangeRequest(**req) for req in requests]

# Ticketing Integration
@api_router.post("/tickets", response_model=Ticket)
async def create_ticket(
    title: str,
    description: str,
    finding_id: Optional[str] = None,
    remediation_id: Optional[str] = None,
    priority: RiskLevel = RiskLevel.MEDIUM,
    external_system: Optional[str] = None
):
    """Create ticket for external systems"""
    ticket = Ticket(
        title=title,
        description=description,
        finding_id=finding_id,
        remediation_id=remediation_id,
        priority=priority,
        external_system=external_system
    )
    
    # Create external ticket if system is configured
    if external_system == "jira" and finding_id and remediation_id:
        finding = await db.findings.find_one({"id": finding_id})
        remediation = await db.remediation_playbooks.find_one({"id": remediation_id})
        if finding and remediation:
            external_id = await ticketing.create_jira_ticket(Finding(**finding), RemediationPlaybook(**remediation))
            ticket.external_id = external_id
    
    await db.tickets.insert_one(ticket.dict())
    
    # Log audit event
    await log_audit("system", AuditAction.CREATE, "ticket", ticket.id, {
        "external_system": external_system,
        "external_id": ticket.external_id
    })
    
    return ticket

@api_router.get("/tickets")
async def get_tickets(status: Optional[TicketStatus] = None):
    """Get tickets"""
    query = {}
    if status:
        query["status"] = status
    
    tickets = await db.tickets.find(query).to_list(100)
    return [Ticket(**ticket) for ticket in tickets]

# Audit Trail
@api_router.get("/audit-logs")
async def get_audit_logs(
    user_id: Optional[str] = None,
    action: Optional[AuditAction] = None,
    resource_type: Optional[str] = None,
    limit: int = 100
):
    """Get audit logs"""
    query = {}
    if user_id:
        query["user_id"] = user_id
    if action:
        query["action"] = action
    if resource_type:
        query["resource_type"] = resource_type
    
    logs = await db.audit_logs.find(query).sort("timestamp", -1).limit(limit).to_list(limit)
    return [AuditLog(**log) for log in logs]

# Enhanced Dashboard with Audit and Change Management Stats
@api_router.get("/dashboard/stats")
async def get_enhanced_dashboard_stats():
    """Get comprehensive dashboard statistics"""
    # Basic counts
    total_assets = await db.assets.count_documents({})
    total_findings = await db.findings.count_documents({})
    total_remediations = await db.remediation_playbooks.count_documents({})
    
    # Severity breakdown
    severity_counts = {}
    for severity in RiskLevel:
        count = await db.findings.count_documents({"severity": severity.value})
        severity_counts[severity.value] = count
    
    # Finding type breakdown
    type_counts = {}
    for finding_type in FindingType:
        count = await db.findings.count_documents({"finding_type": finding_type.value})
        type_counts[finding_type.value] = count
    
    # Change management stats
    change_requests = await db.change_requests.count_documents({})
    pending_approvals = await db.change_requests.count_documents({"status": RemediationStatus.PENDING})
    
    # Cross-host vulnerabilities
    cross_host_pipeline = [
        {"$match": {"affected_hosts.1": {"$exists": True}}},
        {"$count": "cross_host_vulns"}
    ]
    cross_host_result = await db.findings.aggregate(cross_host_pipeline).to_list(1)
    cross_host_vulns = cross_host_result[0]["cross_host_vulns"] if cross_host_result else 0
    
    # Recent activities
    recent_scans = await db.scan_jobs.find().sort("created_at", -1).limit(10).to_list(10)
    recent_audit_logs = await db.audit_logs.find().sort("timestamp", -1).limit(10).to_list(10)
    
    # Top CVEs
    pipeline = [
        {"$unwind": "$cve_ids"},
        {"$group": {"_id": "$cve_ids", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_cves = await db.findings.aggregate(pipeline).to_list(10)
    
    return {
        "summary": {
            "total_assets": total_assets,
            "total_findings": total_findings,
            "total_remediations": total_remediations,
            "change_requests": change_requests,
            "pending_approvals": pending_approvals,
            "cross_host_vulnerabilities": cross_host_vulns
        },
        "severity_breakdown": severity_counts,
        "finding_types": type_counts,
        "recent_scans": [ScanJob(**scan) for scan in recent_scans],
        "recent_activities": [AuditLog(**log) for log in recent_audit_logs],
        "top_cves": top_cves,
        "compliance_status": {
            "total_compliance_findings": type_counts.get("compliance", 0),
            "misconfigurations": type_counts.get("misconfiguration", 0)
        }
    }

# Helper function for enhanced mock findings
async def generate_enhanced_mock_findings(targets: List[str], scan_id: str, include_misconfigs: bool = True) -> List[Finding]:
    """Generate realistic mock vulnerability and misconfiguration findings"""
    mock_vulns = [
        {
            "title": "OpenSSL Heartbleed Vulnerability",
            "description": "OpenSSL versions 1.0.1 through 1.0.1f are vulnerable to the Heartbleed bug",
            "cve_ids": ["CVE-2014-0160"],
            "severity": RiskLevel.CRITICAL,
            "plugin_id": "ssl_heartbleed",
            "finding_type": FindingType.VULNERABILITY,
            "category": "SSL/TLS"
        },
        {
            "title": "SSH Weak Encryption Algorithms",
            "description": "SSH server supports weak encryption algorithms",
            "cve_ids": ["CVE-2008-5161"],
            "severity": RiskLevel.MEDIUM,
            "plugin_id": "ssh_weak_crypto",
            "finding_type": FindingType.VULNERABILITY,
            "category": "SSH"
        },
        {
            "title": "Apache HTTP Server Path Traversal",
            "description": "Apache HTTP Server vulnerable to path traversal attacks",
            "cve_ids": ["CVE-2021-41773", "CVE-2021-42013"],
            "severity": RiskLevel.HIGH,
            "plugin_id": "apache_path_traversal",
            "finding_type": FindingType.VULNERABILITY,
            "category": "Web Server"
        }
    ]
    
    mock_misconfigs = [
        {
            "title": "Default Admin Credentials",
            "description": "System using default administrative credentials",
            "cve_ids": [],
            "severity": RiskLevel.HIGH,
            "plugin_id": "default_creds",
            "finding_type": FindingType.MISCONFIGURATION,
            "category": "Authentication",
            "compliance_frameworks": ["CIS", "NIST"]
        },
        {
            "title": "Unencrypted Database Connection",
            "description": "Database connections not using SSL/TLS encryption",
            "cve_ids": [],
            "severity": RiskLevel.MEDIUM,
            "plugin_id": "unencrypted_db",
            "finding_type": FindingType.MISCONFIGURATION,
            "category": "Database Security",
            "compliance_frameworks": ["PCI-DSS", "SOX"]
        },
        {
            "title": "Audit Logging Disabled",
            "description": "System audit logging is not properly configured",
            "cve_ids": [],
            "severity": RiskLevel.MEDIUM,
            "plugin_id": "audit_disabled",
            "finding_type": FindingType.COMPLIANCE,
            "category": "Logging",
            "compliance_frameworks": ["CIS", "NIST", "SOX"]
        }
    ]
    
    findings = []
    for target in targets:
        # Create asset if not exists
        asset = await db.assets.find_one({"hostname": target})
        if not asset:
            new_asset = Asset(
                hostname=target,
                ip_address=target if target.replace('.', '').isdigit() else None,
                asset_type="server",
                environment="production",
                operating_system="Linux Ubuntu 20.04"
            )
            await db.assets.insert_one(new_asset.dict())
            asset_id = new_asset.id
        else:
            asset_id = asset["id"]
        
        # Generate vulnerability findings
        import random
        selected_vulns = random.sample(mock_vulns, random.randint(1, 3))
        
        for vuln in selected_vulns:
            finding = Finding(
                asset_id=asset_id,
                plugin_id=vuln["plugin_id"],
                title=vuln["title"],
                description=vuln["description"],
                finding_type=vuln["finding_type"],
                cve_ids=vuln["cve_ids"],
                severity=vuln["severity"],
                category=vuln.get("category"),
                affected_hosts=[target]
            )
            findings.append(finding)
        
        # Generate misconfiguration findings if requested
        if include_misconfigs:
            selected_misconfigs = random.sample(mock_misconfigs, random.randint(1, 2))
            
            for misconfig in selected_misconfigs:
                finding = Finding(
                    asset_id=asset_id,
                    plugin_id=misconfig["plugin_id"],
                    title=misconfig["title"],
                    description=misconfig["description"],
                    finding_type=misconfig["finding_type"],
                    cve_ids=misconfig["cve_ids"],
                    severity=misconfig["severity"],
                    category=misconfig.get("category"),
                    compliance_frameworks=misconfig.get("compliance_frameworks", []),
                    affected_hosts=[target]
                )
                findings.append(finding)
    
    return findings

# Include router
app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)