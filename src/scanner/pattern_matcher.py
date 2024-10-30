"""
Pattern matching functionality for XSS vulnerability detection.
"""
import re
from typing import List
from config.settings import XSS_PATTERNS

class XSSPatternMatcher:
    """Handles pattern matching for XSS vulnerability detection."""
    
    @staticmethod
    def check_for_xss_patterns(content: str) -> List[str]:
        """
        Check content for XSS patterns.
        
        Args:
            content: String content to check
            
        Returns:
            List of matched patterns
        """
        matches = []
        for pattern in XSS_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                matches.append(pattern)
        return matches

    @staticmethod
    def analyze_teal_operations(teal_code: str) -> List[dict]:
        """
        Analyze TEAL code for potentially dangerous operations.
        
        Args:
            teal_code: TEAL source code
            
        Returns:
            List of suspicious operations
        """
        suspicious_ops = []
        unsafe_ops = ['concat', 'substring', 'replace']
        
        for line_num, line in enumerate(teal_code.split('\n'), 1):
            for op in unsafe_ops:
                if op in line.lower():
                    suspicious_ops.append({
                        'line': line_num,
                        'operation': op,
                        'code': line.strip()
                    })
        return suspicious_ops