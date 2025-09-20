from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
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
app = FastAPI(title="VulnGuard - Vulnerability Management Platform", version="1.0.0")
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

class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class RemediationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

# Data Models
class Asset(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hostname: str
    ip_address: Optional[str] = None
    asset_type: str
    owner: Optional[str] = None
    environment: str = "production"
    criticality: int = Field(default=3, ge=1, le=5)  # 1=critical, 5=low
    tags: List[str] = []
    last_scan: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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

class Finding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str
    plugin_id: str
    title: str
    description: str
    cve_ids: List[str] = []
    risk_score: float = 0.0
    severity: RiskLevel
    first_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "open"
    raw_output: Optional[Dict[str, Any]] = None
    remediation_notes: Optional[str] = None

class RemediationPlaybook(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    finding_id: str
    title: str
    description: str
    ansible_playbook: Optional[str] = None
    powershell_script: Optional[str] = None
    bash_script: Optional[str] = None
    manual_steps: List[str] = []
    estimated_time: Optional[int] = None  # minutes
    risk_level: RiskLevel
    requires_approval: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ScanJob(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    scan_type: ScanType
    targets: List[str]
    status: str = "pending"
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    findings_count: int = 0
    error_message: Optional[str] = None
    created_by: Optional[str] = None

# LLM Integration
class VulnAnalyzer:
    def __init__(self):
        self.llm = LlmChat(
            api_key=os.environ.get('EMERGENT_LLM_KEY'),
            session_id="vuln-analyzer",
            system_message="""You are a cybersecurity expert specializing in vulnerability analysis and remediation. 
            Analyze vulnerabilities and provide actionable remediation guidance."""
        ).with_model("openai", "gpt-4o")
    
    async def analyze_vulnerability(self, finding_data: Dict) -> Dict:
        """AI-powered vulnerability analysis"""
        try:
            prompt = f"""
            Analyze this vulnerability finding:
            
            Title: {finding_data.get('title')}
            Description: {finding_data.get('description')}
            CVE IDs: {finding_data.get('cve_ids', [])}
            Asset Type: {finding_data.get('asset_type')}
            
            Provide:
            1. Risk assessment and impact analysis
            2. Exploitability likelihood
            3. Business impact assessment
            4. Prioritization recommendation
            
            Respond in JSON format with keys: risk_analysis, exploitability, business_impact, priority_score (1-10)
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
    
    async def generate_remediation(self, finding_data: Dict, asset_type: str) -> Dict:
        """Generate remediation playbooks using AI"""
        try:
            prompt = f"""
            Generate remediation guidance for this vulnerability:
            
            Title: {finding_data.get('title')}
            Description: {finding_data.get('description')}
            CVE IDs: {finding_data.get('cve_ids', [])}
            Asset Type: {asset_type}
            
            Provide:
            1. Ansible playbook (if applicable)
            2. PowerShell script (for Windows)
            3. Bash script (for Linux)
            4. Manual step-by-step instructions
            5. Estimated remediation time
            6. Prerequisites and risks
            
            Format as JSON with keys: ansible_playbook, powershell_script, bash_script, manual_steps, estimated_minutes, prerequisites, risks
            """
            
            message = UserMessage(text=prompt)
            response = await self.llm.send_message(message)
            
            try:
                return json.loads(response)
            except:
                return {"manual_steps": [response], "estimated_minutes": 30}
                
        except Exception as e:
            logger.error(f"Remediation generation failed: {e}")
            return {"error": str(e), "manual_steps": ["Manual remediation required"]}

# CVE/NVD Integration
class CVEIntegrator:
    def __init__(self):
        self.nvd_base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.cve_api_url = "https://cvedb.shodan.io/cve"
    
    async def fetch_cve_details(self, cve_id: str) -> Optional[VulnerabilityIntel]:
        """Fetch CVE details from NVD/CVE databases"""
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
                        references=[ref['url'] for ref in vuln_data.get('references', [])]
                    )
            
            # Fallback to CVE DB
            response = requests.get(f"{self.cve_api_url}/{cve_id}")
            if response.status_code == 200:
                data = response.json()
                return VulnerabilityIntel(
                    cve_id=cve_id,
                    cvss_score=data.get('cvss', 0.0),
                    description=data.get('summary', 'No description available'),
                    severity=RiskLevel.MEDIUM,
                    references=data.get('references', [])
                )
                
        except Exception as e:
            logger.error(f"Failed to fetch CVE {cve_id}: {e}")
        
        return None

# Risk Scoring Engine
class RiskEngine:
    def __init__(self):
        self.vuln_analyzer = VulnAnalyzer()
    
    async def calculate_risk_score(self, finding: Finding, asset: Asset, vuln_intel: Optional[VulnerabilityIntel] = None) -> float:
        """Calculate comprehensive risk score"""
        try:
            base_score = 0.0
            
            # CVSS base score (0-40 points)
            if vuln_intel and vuln_intel.cvss_score:
                base_score += (vuln_intel.cvss_score / 10.0) * 40
            
            # EPSS score (0-25 points)
            if vuln_intel and vuln_intel.epss_score:
                base_score += vuln_intel.epss_score * 25
            
            # KEV catalog (0-20 points)
            if vuln_intel and vuln_intel.kev_catalog:
                base_score += 20
            
            # Asset criticality (0-10 points)
            criticality_score = (6 - asset.criticality) * 2  # Invert scale
            base_score += criticality_score
            
            # Environment factor (0-5 points)
            env_multiplier = {"production": 1.0, "staging": 0.7, "development": 0.3}
            base_score += env_multiplier.get(asset.environment, 0.5) * 5
            
            # Normalize to 0-100 scale
            return min(base_score, 100.0)
            
        except Exception as e:
            logger.error(f"Risk calculation failed: {e}")
            return 50.0  # Default medium risk

# Initialize services
vuln_analyzer = VulnAnalyzer()
cve_integrator = CVEIntegrator()
risk_engine = RiskEngine()

# API Endpoints

@api_router.get("/")
async def root():
    return {"message": "VulnGuard API v1.0.0", "status": "operational"}

# Asset Management
@api_router.post("/assets", response_model=Asset)
async def create_asset(asset_data: Asset):
    asset_dict = asset_data.dict()
    await db.assets.insert_one(asset_dict)
    return asset_data

@api_router.get("/assets", response_model=List[Asset])
async def get_assets():
    assets = await db.assets.find().to_list(1000)
    return [Asset(**asset) for asset in assets]

@api_router.get("/assets/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):
    asset = await db.assets.find_one({"id": asset_id})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return Asset(**asset)

# Vulnerability Intelligence
@api_router.get("/intel/cve/{cve_id}")
async def get_cve_intel(cve_id: str):
    # Check cache first
    cached = await db.vuln_intel.find_one({"cve_id": cve_id})
    if cached:
        return VulnerabilityIntel(**cached)
    
    # Fetch from external sources
    intel = await cve_integrator.fetch_cve_details(cve_id)
    if intel:
        await db.vuln_intel.insert_one(intel.dict())
        return intel
    
    raise HTTPException(status_code=404, detail="CVE not found")

# File Upload and Analysis
@api_router.post("/scan/upload")
async def upload_scan_file(
    file: UploadFile = File(...),
    scan_name: str = Form(...),
    asset_id: str = Form(...)
):
    """Upload and analyze vulnerability scan files"""
    try:
        # Save uploaded file
        file_path = f"/tmp/{file.filename}"
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Parse based on file type
        findings = []
        if file.filename.endswith('.json'):
            findings = await parse_json_scan(file_path, asset_id)
        elif file.filename.endswith('.xml'):
            findings = await parse_nmap_xml(file_path, asset_id)
        elif file.filename.endswith('.csv'):
            findings = await parse_csv_scan(file_path, asset_id)
        
        # Store findings
        for finding in findings:
            await db.findings.insert_one(finding.dict())
        
        # Create scan job record
        scan_job = ScanJob(
            name=scan_name,
            scan_type=ScanType.FILE_BASED,
            targets=[asset_id],
            status="completed",
            findings_count=len(findings),
            completed_at=datetime.now(timezone.utc)
        )
        await db.scan_jobs.insert_one(scan_job.dict())
        
        return {
            "message": f"Successfully processed {len(findings)} findings",
            "scan_id": scan_job.id,
            "findings_count": len(findings)
        }
        
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Findings Management
@api_router.get("/findings", response_model=List[Finding])
async def get_findings(
    asset_id: Optional[str] = None,
    severity: Optional[RiskLevel] = None,
    limit: int = 100
):
    query = {}
    if asset_id:
        query["asset_id"] = asset_id
    if severity:
        query["severity"] = severity
    
    findings = await db.findings.find(query).limit(limit).to_list(limit)
    return [Finding(**finding) for finding in findings]

@api_router.get("/findings/{finding_id}", response_model=Finding)
async def get_finding(finding_id: str):
    finding = await db.findings.find_one({"id": finding_id})
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return Finding(**finding)

# AI Analysis
@api_router.post("/findings/{finding_id}/analyze")
async def analyze_finding(finding_id: str):
    """AI-powered vulnerability analysis"""
    finding = await db.findings.find_one({"id": finding_id})
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    # Get asset details
    asset = await db.assets.find_one({"id": finding["asset_id"]})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Perform AI analysis
    analysis = await vuln_analyzer.analyze_vulnerability(finding)
    
    # Update finding with analysis
    await db.findings.update_one(
        {"id": finding_id},
        {"$set": {"ai_analysis": analysis, "updated_at": datetime.now(timezone.utc)}}
    )
    
    return analysis

# Remediation Management
@api_router.post("/findings/{finding_id}/remediation", response_model=RemediationPlaybook)
async def generate_remediation(finding_id: str):
    """Generate AI-powered remediation playbooks"""
    finding = await db.findings.find_one({"id": finding_id})
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    asset = await db.assets.find_one({"id": finding["asset_id"]})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Generate remediation using AI
    remediation_data = await vuln_analyzer.generate_remediation(finding, asset["asset_type"])
    
    playbook = RemediationPlaybook(
        finding_id=finding_id,
        title=f"Remediation for {finding['title']}",
        description=f"AI-generated remediation for {finding['title']}",
        ansible_playbook=remediation_data.get("ansible_playbook"),
        powershell_script=remediation_data.get("powershell_script"),
        bash_script=remediation_data.get("bash_script"),
        manual_steps=remediation_data.get("manual_steps", []),
        estimated_time=remediation_data.get("estimated_minutes", 30),
        risk_level=RiskLevel(finding["severity"])
    )
    
    await db.remediation_playbooks.insert_one(playbook.dict())
    return playbook

@api_router.get("/findings/{finding_id}/remediation", response_model=List[RemediationPlaybook])
async def get_remediation_playbooks(finding_id: str):
    playbooks = await db.remediation_playbooks.find({"finding_id": finding_id}).to_list(100)
    return [RemediationPlaybook(**pb) for pb in playbooks]

# Dashboard and Analytics
@api_router.get("/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    # Count assets
    total_assets = await db.assets.count_documents({})
    
    # Count findings by severity
    severity_counts = {}
    for severity in RiskLevel:
        count = await db.findings.count_documents({"severity": severity.value})
        severity_counts[severity.value] = count
    
    # Recent scan jobs
    recent_scans = await db.scan_jobs.find().sort("created_at", -1).limit(10).to_list(10)
    
    # Top CVEs
    pipeline = [
        {"$unwind": "$cve_ids"},
        {"$group": {"_id": "$cve_ids", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_cves = await db.findings.aggregate(pipeline).to_list(10)
    
    return {
        "total_assets": total_assets,
        "total_findings": sum(severity_counts.values()),
        "severity_breakdown": severity_counts,
        "recent_scans": [ScanJob(**scan) for scan in recent_scans],
        "top_cves": top_cves
    }

# Risk Analysis
@api_router.post("/risk/calculate/{finding_id}")
async def calculate_finding_risk(finding_id: str):
    """Calculate comprehensive risk score for a finding"""
    finding = await db.findings.find_one({"id": finding_id})
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    asset = await db.assets.find_one({"id": finding["asset_id"]})
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Get vulnerability intelligence
    vuln_intel = None
    if finding.get("cve_ids"):
        cve_id = finding["cve_ids"][0]
        intel_data = await db.vuln_intel.find_one({"cve_id": cve_id})
        if intel_data:
            vuln_intel = VulnerabilityIntel(**intel_data)
    
    # Calculate risk score
    risk_score = await risk_engine.calculate_risk_score(
        Finding(**finding),
        Asset(**asset),
        vuln_intel
    )
    
    # Update finding with risk score
    await db.findings.update_one(
        {"id": finding_id},
        {"$set": {"risk_score": risk_score, "updated_at": datetime.now(timezone.utc)}}
    )
    
    return {"finding_id": finding_id, "risk_score": risk_score}

# Network Discovery Simulation
@api_router.post("/scan/network")
async def simulate_network_scan(targets: List[str], scan_name: str = "Network Discovery"):
    """Simulate network vulnerability scanning"""
    try:
        scan_job = ScanJob(
            name=scan_name,
            scan_type=ScanType.NETWORK,
            targets=targets,
            status="running",
            started_at=datetime.now(timezone.utc)
        )
        await db.scan_jobs.insert_one(scan_job.dict())
        
        # Simulate scan results with common vulnerabilities
        mock_findings = await generate_mock_findings(targets, scan_job.id)
        
        # Store findings
        for finding in mock_findings:
            await db.findings.insert_one(finding.dict())
        
        # Update scan job
        await db.scan_jobs.update_one(
            {"id": scan_job.id},
            {"$set": {
                "status": "completed",
                "completed_at": datetime.now(timezone.utc),
                "findings_count": len(mock_findings)
            }}
        )
        
        return {
            "scan_id": scan_job.id,
            "status": "completed",
            "findings_count": len(mock_findings)
        }
        
    except Exception as e:
        logger.error(f"Network scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions
async def parse_json_scan(file_path: str, asset_id: str) -> List[Finding]:
    """Parse JSON vulnerability scan files"""
    findings = []
    try:
        async with aiofiles.open(file_path, 'r') as f:
            content = await f.read()
            data = json.loads(content)
            
            # Handle various JSON formats
            if 'vulnerabilities' in data:
                for vuln in data['vulnerabilities']:
                    finding = Finding(
                        asset_id=asset_id,
                        plugin_id=vuln.get('id', 'unknown'),
                        title=vuln.get('name', 'Unknown Vulnerability'),
                        description=vuln.get('description', ''),
                        cve_ids=vuln.get('cve', []),
                        severity=RiskLevel(vuln.get('severity', 'medium').lower())
                    )
                    findings.append(finding)
            
    except Exception as e:
        logger.error(f"JSON parsing failed: {e}")
    
    return findings

async def parse_nmap_xml(file_path: str, asset_id: str) -> List[Finding]:
    """Parse Nmap XML scan files"""
    findings = []
    # Mock implementation - in production, use xml.etree.ElementTree
    mock_findings = await generate_mock_findings([asset_id], "nmap-scan")
    return mock_findings

async def parse_csv_scan(file_path: str, asset_id: str) -> List[Finding]:
    """Parse CSV vulnerability scan files"""
    findings = []
    try:
        async with aiofiles.open(file_path, 'r') as f:
            content = await f.read()
            lines = content.strip().split('\n')
            
            if lines:
                headers = lines[0].split(',')
                for line in lines[1:]:
                    values = line.split(',')
                    if len(values) >= 3:
                        finding = Finding(
                            asset_id=asset_id,
                            plugin_id=values[0] if len(values) > 0 else 'csv-import',
                            title=values[1] if len(values) > 1 else 'CSV Import Finding',
                            description=values[2] if len(values) > 2 else '',
                            severity=RiskLevel(values[3].lower() if len(values) > 3 and values[3].lower() in ['critical', 'high', 'medium', 'low'] else 'medium')
                        )
                        findings.append(finding)
                        
    except Exception as e:
        logger.error(f"CSV parsing failed: {e}")
    
    return findings

async def generate_mock_findings(targets: List[str], scan_id: str) -> List[Finding]:
    """Generate realistic mock vulnerability findings"""
    mock_vulns = [
        {
            "title": "OpenSSL Heartbleed Vulnerability",
            "description": "OpenSSL versions 1.0.1 through 1.0.1f are vulnerable to the Heartbleed bug",
            "cve_ids": ["CVE-2014-0160"],
            "severity": RiskLevel.CRITICAL,
            "plugin_id": "ssl_heartbleed"
        },
        {
            "title": "SSH Weak Encryption Algorithms",
            "description": "SSH server supports weak encryption algorithms",
            "cve_ids": ["CVE-2008-5161"],
            "severity": RiskLevel.MEDIUM,
            "plugin_id": "ssh_weak_crypto"
        },
        {
            "title": "Apache HTTP Server Multiple Vulnerabilities",
            "description": "Multiple vulnerabilities in Apache HTTP Server",
            "cve_ids": ["CVE-2021-41773", "CVE-2021-42013"],
            "severity": RiskLevel.HIGH,
            "plugin_id": "apache_multi_vuln"
        },
        {
            "title": "MySQL Root Account Without Password",
            "description": "MySQL server has root account without password",
            "cve_ids": [],
            "severity": RiskLevel.CRITICAL,
            "plugin_id": "mysql_no_password"
        },
        {
            "title": "TLS/SSL Certificate Expired",
            "description": "TLS/SSL certificate has expired",
            "cve_ids": [],
            "severity": RiskLevel.MEDIUM,
            "plugin_id": "ssl_cert_expired"
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
                environment="production"
            )
            await db.assets.insert_one(new_asset.dict())
            asset_id = new_asset.id
        else:
            asset_id = asset["id"]
        
        # Generate 2-4 findings per target
        import random
        selected_vulns = random.sample(mock_vulns, random.randint(2, 4))
        
        for vuln in selected_vulns:
            finding = Finding(
                asset_id=asset_id,
                plugin_id=vuln["plugin_id"],
                title=vuln["title"],
                description=vuln["description"],
                cve_ids=vuln["cve_ids"],
                severity=vuln["severity"]
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