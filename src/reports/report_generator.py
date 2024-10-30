"""
Report generation functionality for scan results.
"""
import json
from src.models.vulnerability import ScanResult

class ReportGenerator:
    """Generates formatted reports from scan results."""
    
    @staticmethod
    def generate_json_report(scan_result: ScanResult) -> str:
        """
        Generate a JSON format report from scan results.
        
        Args:
            scan_result: Complete scan results
            
        Returns:
            JSON formatted report string
        """
        report = {
            'summary': {
                'app_id': scan_result.app_id,
                'risk_level': scan_result.risk_level,
                'vulnerability_count': len(scan_result.vulnerabilities),
                'scan_timestamp': scan_result.scan_timestamp
            },
            'vulnerabilities': [
                {
                    'type': v.type,
                    'description': v.description,
                    'risk_level': v.risk_level,
                    'location': v.location,
                    'code_snippet': v.code_snippet,
                    'recommendation': v.recommendation
                }
                for v in scan_result.vulnerabilities
            ],
            'recommendations': scan_result.recommendations
        }
        
        return json.dumps(report, indent=2)