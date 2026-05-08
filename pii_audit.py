"""
PII (Personally Identifiable Information) Audit Tool
Scans the project for sensitive data including:
- Social Security Numbers (SSN)
- Credit Card Numbers (CC)
- Email Addresses
- Phone Numbers
- API Keys / Secrets
- Database Credentials
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set

# Define PII patterns
PII_PATTERNS = {
    'ssn': r'\b\d{3}-\d{2}-\d{4}\b|\b\d{9}\b',
    'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\b\(\d{3}\)\s?\d{3}[-.]?\d{4}\b',
    'api_key': r'(api[_-]?key|apikey|api_secret|secret[_-]?key)\s*[:=]\s*[\'\"]?[A-Za-z0-9_\-]{20,}',
    'password': r'(password|passwd|pwd)\s*[:=]\s*[\'\"]?[^\s\'\"]*[\'\"]?',
    'database_url': r'(postgresql|mysql|mongodb)://[^:]+:[^@]+@',
    'private_key': r'-----BEGIN\s+(PRIVATE|RSA)\s+KEY-----',
    'aws_key': r'AKIA[0-9A-Z]{16}',
}

# File extensions to scan
SCAN_EXTENSIONS = {'.py', '.java', '.json', '.xml', '.yml', '.yaml', '.md', '.txt', '.sql', '.sh'}

# Directories to skip
SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv', 
             'target', 'build', '.gradle', '.mvn'}


class PIIAudit:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.findings = {}
        self.scanned_files = 0
        self.clean_files = 0
        
    def should_skip_path(self, path: Path) -> bool:
        """Check if path should be skipped"""
        for part in path.parts:
            if part in SKIP_DIRS:
                return True
        return False
    
    def should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned"""
        return file_path.suffix in SCAN_EXTENSIONS and not self.should_skip_path(file_path)
    
    def scan_file(self, file_path: Path) -> Dict[str, List[int]]:
        """
        Scan a file for PII patterns.
        Returns dict of pattern_name -> list of line numbers with matches
        """
        findings = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    # Skip comments and test data markers
                    if line.strip().startswith('#') or 'test' in line.lower() or 'example' in line.lower():
                        continue
                    
                    for pattern_name, pattern in PII_PATTERNS.items():
                        if re.search(pattern, line, re.IGNORECASE):
                            if pattern_name not in findings:
                                findings[pattern_name] = []
                            findings[pattern_name].append(line_num)
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
        
        return findings
    
    def audit(self) -> Dict:
        """Run audit on entire directory"""
        print(f"Starting PII Audit on {self.root_path}")
        print(f"Scanning for {len(PII_PATTERNS)} PII pattern types...")
        print("-" * 70)
        
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and self.should_scan_file(file_path):
                self.scanned_files += 1
                relative_path = file_path.relative_to(self.root_path)
                
                findings = self.scan_file(file_path)
                
                if findings:
                    self.findings[str(relative_path)] = findings
                    print(f"⚠️  PII FOUND: {relative_path}")
                    for pattern, lines in findings.items():
                        print(f"    - {pattern}: lines {lines}")
                else:
                    self.clean_files += 1
        
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Generate audit report"""
        total_files = self.scanned_files
        affected_files = len(self.findings)
        clean_percentage = (self.clean_files / total_files * 100) if total_files > 0 else 0
        
        report = {
            'total_files_scanned': total_files,
            'clean_files': self.clean_files,
            'files_with_pii': affected_files,
            'clean_percentage': clean_percentage,
            'patterns_checked': list(PII_PATTERNS.keys()),
            'findings': self.findings
        }
        
        return report


def main():
    """Run PII audit on ai-service and backend directories"""
    project_root = Path("c:/Users/user/OneDrive/Documents/Desktop/campus pe gen ai project/ai-risk-register")
    
    # Audit ai-service
    print("\n" + "="*70)
    print("AUDITING: ai-service")
    print("="*70)
    ai_service_path = project_root / "ai-service"
    audit_ai = PIIAudit(ai_service_path)
    report_ai = audit_ai.audit()
    
    # Audit backend
    print("\n" + "="*70)
    print("AUDITING: backend")
    print("="*70)
    backend_path = project_root / "backend"
    audit_backend = PIIAudit(backend_path)
    report_backend = audit_backend.audit()
    
    # Audit frontend
    print("\n" + "="*70)
    print("AUDITING: frontend")
    print("="*70)
    frontend_path = project_root / "frontend"
    audit_frontend = PIIAudit(frontend_path)
    report_frontend = audit_frontend.audit()
    
    # Generate summary report
    print("\n" + "="*70)
    print("PII AUDIT SUMMARY")
    print("="*70)
    
    total_scanned = (report_ai['total_files_scanned'] + 
                    report_backend['total_files_scanned'] + 
                    report_frontend['total_files_scanned'])
    
    total_clean = (report_ai['clean_files'] + 
                  report_backend['clean_files'] + 
                  report_frontend['clean_files'])
    
    total_findings = (len(report_ai['findings']) + 
                     len(report_backend['findings']) + 
                     len(report_frontend['findings']))
    
    print(f"\nTotal files scanned: {total_scanned}")
    print(f"Clean files: {total_clean}")
    print(f"Files with potential PII: {total_findings}")
    
    if total_findings == 0:
        print("\n✅ AUDIT RESULT: PASSED")
        print("No PII detected in source code")
    else:
        print("\n⚠️  AUDIT RESULT: REVIEW REQUIRED")
        print("Please review flagged files above")
    
    print(f"\nPII patterns scanned: {len(PII_PATTERNS)}")
    print("  1. Social Security Numbers (SSN)")
    print("  2. Credit Card Numbers")
    print("  3. Email Addresses")
    print("  4. Phone Numbers")
    print("  5. API Keys")
    print("  6. Passwords")
    print("  7. Database URLs")
    print("  8. Private Keys")
    print("  9. AWS Keys")


if __name__ == '__main__':
    main()
