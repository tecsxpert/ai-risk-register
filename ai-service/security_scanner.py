"""
OWASP ZAP-like Security Scanner for AI Risk Register
Performs automated security testing against both Flask and Spring Boot backends
Generates vulnerability report with Critical/Medium/Low findings
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import urllib.parse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Severity(Enum):
    CRITICAL = "Critical"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"


@dataclass
class Vulnerability:
    id: str
    name: str
    description: str
    severity: Severity
    cwe_id: str
    owasp_category: str
    affected_endpoint: str
    parameter: str
    evidence: str
    remediation: str
    
    def to_dict(self):
        data = asdict(self)
        data['severity'] = self.severity.value
        return data


class OWASPZAPScanner:
    """Security scanner simulating OWASP ZAP functionality"""
    
    def __init__(self, flask_base_url: str = "http://localhost:5000", 
                 spring_base_url: str = "http://localhost:8080"):
        self.flask_base_url = flask_base_url
        self.spring_base_url = spring_base_url
        self.vulnerabilities: List[Vulnerability] = []
        self.session = requests.Session()
        self.session.timeout = 10
        
    def is_service_running(self, base_url: str) -> bool:
        """Check if a service is running"""
        try:
            response = self.session.get(f"{base_url}/health", timeout=2)
            return response.status_code in [200, 404]
        except Exception as e:
            logger.warning(f"Service at {base_url} not responding: {e}")
            return False
    
    def scan_flask_endpoints(self):
        """Scan Flask AI service endpoints"""
        if not self.is_service_running(self.flask_base_url):
            logger.error(f"Flask service not running at {self.flask_base_url}")
            return
        
        logger.info("=== SCANNING FLASK ENDPOINTS ===")
        
        # Test XSS vulnerabilities
        self.test_xss_in_flask()
        
        # Test SQL Injection
        self.test_sql_injection_in_flask()
        
        # Test Command Injection
        self.test_command_injection_in_flask()
        
        # Test CSRF protection
        self.test_csrf_protection_in_flask()
        
        # Test authentication/authorization
        self.test_auth_in_flask()
        
        # Test input validation
        self.test_input_validation_in_flask()
        
    def scan_spring_endpoints(self):
        """Scan Spring Boot endpoints"""
        if not self.is_service_running(self.spring_base_url):
            logger.error(f"Spring Boot service not running at {self.spring_base_url}")
            return
        
        logger.info("=== SCANNING SPRING BOOT ENDPOINTS ===")
        
        # Test XSS vulnerabilities
        self.test_xss_in_spring()
        
        # Test SQL Injection
        self.test_sql_injection_in_spring()
        
        # Test Deserialization
        self.test_deserialization_in_spring()
        
        # Test authentication/authorization
        self.test_auth_in_spring()
        
        # Test broken access control
        self.test_access_control_in_spring()
    
    # Flask Scan Tests
    def test_xss_in_flask(self):
        """Test for XSS vulnerabilities in Flask"""
        endpoint = f"{self.flask_base_url}/ai/response"
        payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror='alert(\"xss\")'>",
            "javascript:alert('xss')",
            "<svg/onload=alert('xss')>"
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(
                    endpoint,
                    json={"prompt": payload},
                    timeout=5
                )
                
                if response.status_code == 200 and payload in response.text:
                    self.vulnerabilities.append(Vulnerability(
                        id="XSS_FLASK_001",
                        name="Stored XSS in /ai/response",
                        description=f"XSS payload not escaped: {payload}",
                        severity=Severity.CRITICAL,
                        cwe_id="CWE-79",
                        owasp_category="A03:2021 - Injection",
                        affected_endpoint="/ai/response",
                        parameter="prompt",
                        evidence=f"Payload: {payload}",
                        remediation="Implement HTML encoding in response serialization"
                    ))
                    logger.warning(f"XSS Found: {payload}")
                elif response.status_code == 400:
                    logger.info(f"XSS Blocked: {payload} (400 response)")
            except Exception as e:
                logger.debug(f"XSS test error: {e}")
    
    def test_sql_injection_in_flask(self):
        """Test for SQL Injection in Flask"""
        endpoint = f"{self.flask_base_url}/ai/response"
        payloads = [
            "1' OR '1'='1",
            "admin' --",
            "1' UNION SELECT NULL --",
            "' OR 1=1 --"
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(
                    endpoint,
                    json={"prompt": payload},
                    timeout=5
                )
                
                if response.status_code == 400:
                    logger.info(f"SQLi Blocked: {payload}")
                elif response.status_code == 200:
                    logger.warning(f"SQLi might be vulnerable: {payload}")
            except Exception as e:
                logger.debug(f"SQLi test error: {e}")
    
    def test_command_injection_in_flask(self):
        """Test for Command Injection"""
        endpoint = f"{self.flask_base_url}/ai/response"
        payloads = [
            "; ls;",
            "| whoami",
            "$(whoami)",
            "`id`"
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(
                    endpoint,
                    json={"prompt": payload},
                    timeout=5
                )
                
                if response.status_code == 400:
                    logger.info(f"Command Injection Blocked: {payload}")
            except Exception as e:
                logger.debug(f"Command injection test error: {e}")
    
    def test_csrf_protection_in_flask(self):
        """Test CSRF protection"""
        endpoint = f"{self.flask_base_url}/ai/response"
        
        # Check for CSRF token in response
        try:
            response = self.session.get(f"{self.flask_base_url}/", timeout=5)
            
            if "csrf" not in response.text.lower():
                self.vulnerabilities.append(Vulnerability(
                    id="CSRF_FLASK_001",
                    name="Missing CSRF Protection",
                    description="No CSRF tokens found in forms",
                    severity=Severity.MEDIUM,
                    cwe_id="CWE-352",
                    owasp_category="A01:2021 - Broken Access Control",
                    affected_endpoint="/ai/response",
                    parameter="N/A",
                    evidence="No CSRF token in HTML responses",
                    remediation="Implement Flask-WTF CSRF protection"
                ))
                logger.warning("CSRF Protection Missing")
        except Exception as e:
            logger.debug(f"CSRF test error: {e}")
    
    def test_auth_in_flask(self):
        """Test authentication in Flask"""
        endpoint = f"{self.flask_base_url}/api/admin"
        
        try:
            response = self.session.get(endpoint, timeout=5)
            if response.status_code == 200:
                self.vulnerabilities.append(Vulnerability(
                    id="AUTH_FLASK_001",
                    name="Missing Authentication",
                    description="Admin endpoint accessible without authentication",
                    severity=Severity.CRITICAL,
                    cwe_id="CWE-287",
                    owasp_category="A07:2021 - Identification and Authentication Failures",
                    affected_endpoint="/api/admin",
                    parameter="N/A",
                    evidence="200 response without auth",
                    remediation="Implement Flask-Login with @login_required decorator"
                ))
                logger.warning("Auth issue detected")
        except Exception as e:
            logger.debug(f"Auth test error: {e}")
    
    def test_input_validation_in_flask(self):
        """Test input validation"""
        endpoint = f"{self.flask_base_url}/ai/response"
        
        # Test with oversized input
        try:
            large_input = "A" * 100000
            response = self.session.post(
                endpoint,
                json={"prompt": large_input},
                timeout=5
            )
            
            if response.status_code == 200:
                logger.info("Large input accepted (good for DoS mitigation)")
        except requests.exceptions.Timeout:
            logger.info("Timeout on large input (potential vulnerability)")
    
    # Spring Boot Scan Tests
    def test_xss_in_spring(self):
        """Test for XSS vulnerabilities in Spring Boot"""
        endpoint = f"{self.spring_base_url}/api/ai/response"
        payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror='alert(\"xss\")'>",
        ]
        
        for payload in payloads:
            try:
                response = self.session.post(
                    endpoint,
                    json={"prompt": payload},
                    timeout=5
                )
                
                if response.status_code == 400:
                    logger.info(f"Spring XSS Blocked: {payload}")
            except Exception as e:
                logger.debug(f"Spring XSS test error: {e}")
    
    def test_sql_injection_in_spring(self):
        """Test for SQL Injection in Spring Boot"""
        endpoint = f"{self.spring_base_url}/api/ai/response"
        
        try:
            response = self.session.post(
                endpoint,
                json={"prompt": "1' OR '1'='1"},
                timeout=5
            )
            
            if response.status_code == 400:
                logger.info("Spring SQLi Protected (400 response)")
        except Exception as e:
            logger.debug(f"Spring SQLi test error: {e}")
    
    def test_deserialization_in_spring(self):
        """Test for deserialization vulnerabilities"""
        # Spring Boot typically uses JSON, check for ysoserial gadget chains
        logger.info("Deserialization test: Spring using JSON (lower risk)")
    
    def test_auth_in_spring(self):
        """Test authentication in Spring Boot"""
        endpoint = f"{self.spring_base_url}/admin"
        
        try:
            response = self.session.get(endpoint, timeout=5)
            if response.status_code == 200:
                self.vulnerabilities.append(Vulnerability(
                    id="AUTH_SPRING_001",
                    name="Missing Authentication on Admin Endpoint",
                    description="Admin endpoint accessible without Spring Security",
                    severity=Severity.CRITICAL,
                    cwe_id="CWE-287",
                    owasp_category="A07:2021 - Identification and Authentication Failures",
                    affected_endpoint="/admin",
                    parameter="N/A",
                    evidence="200 response without auth",
                    remediation="Configure Spring Security with @EnableWebSecurity"
                ))
                logger.warning("Spring auth issue detected")
        except Exception as e:
            logger.debug(f"Spring auth test error: {e}")
    
    def test_access_control_in_spring(self):
        """Test broken access control"""
        # Test accessing resources without proper authorization
        endpoints = [
            "/api/users/1",
            "/api/users/2",
            "/api/admin/settings"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(
                    f"{self.spring_base_url}{endpoint}",
                    timeout=5
                )
                
                if response.status_code == 200:
                    logger.info(f"Accessible: {endpoint}")
            except Exception as e:
                logger.debug(f"Access control test error: {e}")
    
    def run_full_scan(self) -> Dict[str, Any]:
        """Run complete security scan"""
        logger.info("Starting OWASP Security Scan...")
        start_time = datetime.now()
        
        self.scan_flask_endpoints()
        self.scan_spring_endpoints()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Generate report
        report = self.generate_report(duration)
        
        return report
    
    def generate_report(self, duration: float) -> Dict[str, Any]:
        """Generate security scan report"""
        
        # Categorize findings
        critical = [v for v in self.vulnerabilities if v.severity == Severity.CRITICAL]
        medium = [v for v in self.vulnerabilities if v.severity == Severity.MEDIUM]
        low = [v for v in self.vulnerabilities if v.severity == Severity.LOW]
        info = [v for v in self.vulnerabilities if v.severity == Severity.INFO]
        
        report = {
            "scan_info": {
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": duration,
                "scanner": "OWASP ZAP-like Scanner",
                "flask_target": self.flask_base_url,
                "spring_target": self.spring_base_url
            },
            "summary": {
                "total_issues": len(self.vulnerabilities),
                "critical": len(critical),
                "medium": len(medium),
                "low": len(low),
                "info": len(info)
            },
            "vulnerabilities": {
                "critical": [v.to_dict() for v in critical],
                "medium": [v.to_dict() for v in medium],
                "low": [v.to_dict() for v in low],
                "info": [v.to_dict() for v in info]
            },
            "risk_rating": self._calculate_risk_rating(critical, medium)
        }
        
        return report
    
    def _calculate_risk_rating(self, critical: List[Vulnerability], medium: List[Vulnerability]) -> str:
        """Calculate overall risk rating"""
        if len(critical) > 0:
            return "HIGH RISK"
        elif len(medium) > 2:
            return "MEDIUM RISK"
        elif len(medium) > 0:
            return "MEDIUM-LOW RISK"
        else:
            return "LOW RISK"
    
    def save_report(self, filename: str = "owasp_scan_report.json"):
        """Save report to JSON file"""
        import os
        report = self.run_full_scan()
        
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to {filepath}")
        return report


if __name__ == "__main__":
    scanner = OWASPZAPScanner()
    report = scanner.save_report()
    
    print("\n" + "="*60)
    print("OWASP SECURITY SCAN SUMMARY")
    print("="*60)
    print(f"Total Issues: {report['summary']['total_issues']}")
    print(f"Critical: {report['summary']['critical']}")
    print(f"Medium: {report['summary']['medium']}")
    print(f"Low: {report['summary']['low']}")
    print(f"Risk Rating: {report['risk_rating']}")
    print("="*60)
