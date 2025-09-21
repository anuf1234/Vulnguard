"""
Compliance Framework Data for VulnGuard
Contains detailed mapping data for major compliance frameworks
"""

from typing import Dict, List, Any

# NIST 800-53 Rev 5 Controls (subset of key security controls)
NIST_800_53_CONTROLS = {
    "AC-2": {
        "title": "Account Management",
        "family": "Access Control",
        "description": "Manage system accounts, group memberships, privileges, workflow, notifications, deactivations, and authorizations.",
        "implementation_guidance": "Establish procedures for account management including automated mechanisms where feasible.",
        "assessment_procedures": [
            "Examine account management policy and procedures",
            "Interview personnel responsible for account management", 
            "Test account management automated mechanisms"
        ],
        "related_controls": ["AC-3", "AC-5", "AC-6", "IA-2", "IA-4", "IA-5", "IA-8"],
        "priority": "high"
    },
    "AC-3": {
        "title": "Access Enforcement", 
        "family": "Access Control",
        "description": "Enforce approved authorizations for logical access to information and system resources.",
        "implementation_guidance": "Use access control mechanisms to enforce authorized access determinations.",
        "assessment_procedures": [
            "Examine access control policy and procedures",
            "Examine system configuration settings and associated documentation",
            "Test access enforcement mechanisms"
        ],
        "related_controls": ["AC-2", "AC-4", "AC-5", "AC-6", "AU-9", "CM-5"],
        "priority": "high"
    },
    "AC-6": {
        "title": "Least Privilege",
        "family": "Access Control", 
        "description": "Employ the principle of least privilege, allowing only authorized access for users which are necessary to accomplish assigned tasks.",
        "implementation_guidance": "Define user privileges and implement mechanisms to enforce least privilege access.",
        "assessment_procedures": [
            "Examine access control policy and least privilege procedures",
            "Interview personnel about privilege assignment processes",
            "Test privilege enforcement mechanisms"
        ],
        "related_controls": ["AC-2", "AC-3", "AC-5", "CM-5", "CM-11"],
        "priority": "high"
    },
    "SI-2": {
        "title": "Flaw Remediation",
        "family": "System and Information Integrity",
        "description": "Identify, report, and correct system flaws including the installation of security-relevant software and firmware updates.",
        "implementation_guidance": "Establish procedures for flaw identification, reporting, and remediation including testing of updates.",
        "assessment_procedures": [
            "Examine flaw remediation policy and procedures",
            "Examine system documentation for flaw remediation records",
            "Test flaw remediation process and mechanisms"
        ],
        "related_controls": ["CM-3", "CM-5", "CM-8", "SI-3", "SI-5", "SI-11"],
        "priority": "critical"
    },
    "SI-4": {
        "title": "System Monitoring",
        "family": "System and Information Integrity",
        "description": "Monitor the system to detect attacks and indicators of potential attacks, unauthorized local connections.",
        "implementation_guidance": "Deploy monitoring tools and establish procedures for continuous system monitoring.",
        "assessment_procedures": [
            "Examine system monitoring policy and procedures", 
            "Examine system monitoring tools and associated documentation",
            "Test system monitoring capabilities and alerting mechanisms"
        ],
        "related_controls": ["AU-2", "AU-6", "AU-12", "CA-7", "IR-4", "SI-3"],
        "priority": "high"
    }
}

# ISO 27001:2022 Controls (Annex A)
ISO_27001_CONTROLS = {
    "A.8.2": {
        "title": "Privileged access rights",
        "family": "Access Management",
        "description": "The allocation and use of privileged access rights shall be restricted and managed.",
        "implementation_guidance": "Implement formal procedures for managing privileged access including regular reviews.",
        "assessment_procedures": [
            "Review privileged access management procedures",
            "Examine privileged account inventories and access reviews",
            "Test privileged access controls and monitoring"
        ],
        "related_controls": ["A.8.1", "A.8.3", "A.9.1", "A.9.2"],
        "priority": "high"
    },
    "A.8.8": {
        "title": "Management of privileged access rights",
        "family": "Access Management", 
        "description": "The allocation and use of privileged access rights shall be restricted and managed.",
        "implementation_guidance": "Establish procedures for granting, monitoring, and reviewing privileged access.",
        "assessment_procedures": [
            "Review privileged access policies and procedures",
            "Examine privileged access logs and reviews",
            "Test privileged access management controls"
        ],
        "related_controls": ["A.8.2", "A.8.3", "A.9.2"],
        "priority": "high"
    },
    "A.12.6": {
        "title": "Management of technical vulnerabilities",
        "family": "Operations Security",
        "description": "Information about technical vulnerabilities of information systems being used shall be obtained in a timely fashion.",
        "implementation_guidance": "Establish vulnerability management processes including scanning, assessment, and remediation.",
        "assessment_procedures": [
            "Review vulnerability management policy and procedures",
            "Examine vulnerability scan reports and remediation records",
            "Test vulnerability management process effectiveness"
        ],
        "related_controls": ["A.12.1", "A.12.2", "A.14.2", "A.12.5"],
        "priority": "critical"
    }
}

# HIPAA Security Rule Requirements
HIPAA_CONTROLS = {
    "164.308(a)(1)": {
        "title": "Security Officer",
        "family": "Administrative Safeguards",
        "description": "Assign security responsibilities to a security officer.",
        "implementation_guidance": "Designate a security officer responsible for developing and implementing security policies.",
        "assessment_procedures": [
            "Verify security officer designation documentation",
            "Review security officer responsibilities and qualifications",
            "Examine security program oversight activities"
        ],
        "related_controls": ["164.308(a)(2)", "164.308(a)(3)", "164.308(a)(4)"],
        "priority": "high"
    },
    "164.308(a)(5)": {
        "title": "Information System Activity Review",
        "family": "Administrative Safeguards", 
        "description": "Implement procedures to regularly review records of information system activity.",
        "implementation_guidance": "Establish regular review procedures for system logs, access reports, and security incidents.",
        "assessment_procedures": [
            "Examine information system activity review procedures",
            "Review system activity review records and reports",
            "Test information system monitoring and review processes"
        ],
        "related_controls": ["164.312(b)", "164.312(d)", "164.308(a)(1)"],
        "priority": "high"
    },
    "164.312(a)(2)": {
        "title": "Assigned Security Responsibility",
        "family": "Technical Safeguards",
        "description": "Assign a unique name and/or number for identifying and tracking user identity.",
        "implementation_guidance": "Implement unique user identification and authentication mechanisms.",
        "assessment_procedures": [
            "Examine user identification and authentication procedures",
            "Review user account management processes",
            "Test user identification and tracking mechanisms"
        ],
        "related_controls": ["164.312(a)(1)", "164.312(d)", "164.308(a)(3)"],
        "priority": "high"
    }
}

# FedRAMP Controls (subset based on NIST 800-53)
FEDRAMP_CONTROLS = {
    "AC-2": {
        "title": "Account Management",
        "family": "Access Control",
        "description": "Account management for FedRAMP systems with enhanced monitoring requirements.",
        "implementation_guidance": "Implement account management with automated tools and continuous monitoring for federal systems.",
        "assessment_procedures": [
            "Examine account management procedures specific to federal requirements",
            "Review account monitoring and reporting mechanisms",
            "Test automated account management controls"
        ],
        "related_controls": ["AC-3", "AC-6", "IA-2", "IA-4"],
        "priority": "critical"
    },
    "SI-2": {
        "title": "Flaw Remediation",
        "family": "System and Information Integrity",
        "description": "Enhanced flaw remediation requirements for federal cloud systems.",
        "implementation_guidance": "Implement accelerated patch management with mandatory timelines for federal systems.",
        "assessment_procedures": [
            "Examine flaw remediation procedures and timelines",
            "Review patch management automation and reporting",
            "Test flaw remediation compliance with federal timelines"
        ],
        "related_controls": ["CM-3", "SI-3", "SI-4"],
        "priority": "critical"
    }
}

# Compliance Framework to Vulnerability/Finding Type Mappings
COMPLIANCE_MAPPINGS = {
    # Authentication & Access Control Issues
    "weak_authentication": {
        "nist_800_53": [
            {"control_id": "AC-2", "relevance": 0.9},
            {"control_id": "AC-3", "relevance": 0.8},
            {"control_id": "IA-2", "relevance": 0.95},
            {"control_id": "IA-5", "relevance": 0.9}
        ],
        "iso_27001": [
            {"control_id": "A.8.2", "relevance": 0.9},
            {"control_id": "A.9.1", "relevance": 0.85},
            {"control_id": "A.9.2", "relevance": 0.9}
        ],
        "hipaa": [
            {"control_id": "164.312(a)(2)", "relevance": 0.95},
            {"control_id": "164.308(a)(3)", "relevance": 0.8}
        ],
        "fedramp": [
            {"control_id": "AC-2", "relevance": 0.95},
            {"control_id": "IA-2", "relevance": 0.9}
        ]
    },
    
    # Vulnerability Management
    "unpatched_vulnerability": {
        "nist_800_53": [
            {"control_id": "SI-2", "relevance": 0.95},
            {"control_id": "CM-3", "relevance": 0.8},
            {"control_id": "RA-5", "relevance": 0.9}
        ],
        "iso_27001": [
            {"control_id": "A.12.6", "relevance": 0.95},
            {"control_id": "A.14.2", "relevance": 0.85}
        ],
        "fedramp": [
            {"control_id": "SI-2", "relevance": 0.98},
            {"control_id": "RA-5", "relevance": 0.9}
        ]
    },
    
    # Configuration Management
    "misconfiguration": {
        "nist_800_53": [
            {"control_id": "CM-2", "relevance": 0.9},
            {"control_id": "CM-6", "relevance": 0.95},
            {"control_id": "SI-4", "relevance": 0.8}
        ],
        "iso_27001": [
            {"control_id": "A.12.1", "relevance": 0.9},
            {"control_id": "A.12.5", "relevance": 0.85}
        ],
        "hipaa": [
            {"control_id": "164.312(a)(1)", "relevance": 0.8}
        ]
    },
    
    # Privileged Access
    "excessive_privileges": {
        "nist_800_53": [
            {"control_id": "AC-6", "relevance": 0.95},
            {"control_id": "AC-2", "relevance": 0.8}
        ],
        "iso_27001": [
            {"control_id": "A.8.2", "relevance": 0.95},
            {"control_id": "A.8.8", "relevance": 0.9}
        ],
        "hipaa": [
            {"control_id": "164.308(a)(3)", "relevance": 0.9}
        ]
    },
    
    # Monitoring & Logging
    "insufficient_logging": {
        "nist_800_53": [
            {"control_id": "AU-2", "relevance": 0.9},
            {"control_id": "AU-6", "relevance": 0.95},
            {"control_id": "SI-4", "relevance": 0.9}
        ],
        "iso_27001": [
            {"control_id": "A.12.4", "relevance": 0.9}
        ],
        "hipaa": [
            {"control_id": "164.308(a)(5)", "relevance": 0.95},
            {"control_id": "164.312(b)", "relevance": 0.8}
        ]
    }
}

# Risk scoring weights for different factors
RISK_SCORING_WEIGHTS = {
    "cvss_score": 0.25,
    "epss_score": 0.20, 
    "kev_listed": 0.15,
    "asset_criticality": 0.20,
    "business_impact": 0.10,
    "compensating_controls": -0.10  # negative weight reduces risk
}

# Business impact scoring
BUSINESS_IMPACT_SCORES = {
    "critical_system": 1.0,
    "production_system": 0.8,
    "customer_facing": 0.9,
    "financial_system": 1.0,
    "development_system": 0.3,
    "test_system": 0.2,
    "archived_system": 0.1
}

# Asset criticality mapping
ASSET_CRITICALITY_SCORES = {
    "critical": 1.0,
    "high": 0.8,
    "medium": 0.5,
    "low": 0.2,
    "info": 0.1
}

def get_compliance_controls(framework: str) -> Dict[str, Any]:
    """Get all controls for a specific compliance framework"""
    framework_map = {
        "nist_800_53": NIST_800_53_CONTROLS,
        "iso_27001": ISO_27001_CONTROLS,
        "hipaa": HIPAA_CONTROLS,
        "fedramp": FEDRAMP_CONTROLS
    }
    return framework_map.get(framework, {})

def get_compliance_mapping(finding_type: str) -> Dict[str, List[Dict[str, Any]]]:
    """Get compliance control mappings for a specific finding type"""
    return COMPLIANCE_MAPPINGS.get(finding_type, {})

def calculate_risk_score(
    cvss_score: float = 0.0,
    epss_score: float = 0.0,
    kev_listed: bool = False,
    asset_criticality: str = "medium",
    business_impact: str = "medium",
    compensating_controls: List[str] = None
) -> float:
    """Calculate comprehensive risk score based on multiple factors"""
    if compensating_controls is None:
        compensating_controls = []
    
    # Normalize scores to 0-1 range
    normalized_cvss = cvss_score / 10.0 if cvss_score else 0.0
    normalized_epss = epss_score if epss_score else 0.0
    kev_multiplier = 1.5 if kev_listed else 1.0
    
    asset_score = ASSET_CRITICALITY_SCORES.get(asset_criticality.lower(), 0.5)
    impact_score = BUSINESS_IMPACT_SCORES.get(business_impact.lower(), 0.5)
    
    # Calculate compensating controls reduction
    controls_reduction = len(compensating_controls) * 0.1
    
    # Weighted risk calculation
    risk_score = (
        normalized_cvss * RISK_SCORING_WEIGHTS["cvss_score"] +
        normalized_epss * RISK_SCORING_WEIGHTS["epss_score"] +
        asset_score * RISK_SCORING_WEIGHTS["asset_criticality"] +
        impact_score * RISK_SCORING_WEIGHTS["business_impact"] -
        controls_reduction
    ) * kev_multiplier
    
    # KEV bonus for critical vulnerabilities
    if kev_listed:
        risk_score *= 1.2
    
    # Ensure score is between 0 and 1
    return max(0.0, min(1.0, risk_score))

def get_remediation_priority(risk_score: float) -> str:
    """Determine remediation priority based on risk score"""
    if risk_score >= 0.8:
        return "critical"
    elif risk_score >= 0.6:
        return "high"
    elif risk_score >= 0.4:
        return "medium"
    elif risk_score >= 0.2:
        return "low"
    else:
        return "info"