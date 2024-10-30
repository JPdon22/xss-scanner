"""
Main XSS scanner implementation for Algorand smart contracts.
"""
from algosdk.v2client import algod
from typing import Optional, Dict, List
from src.models.vulnerability import Vulnerability, ScanResult
from src.scanner.pattern_matcher import XSSPatternMatcher
from datetime import datetime

class AlgorandXSSScanner:
    """
    Scanner for detecting XSS vulnerabilities in Algorand smart contracts.
    """
    
    def __init__(self, algod_address: str, algod_token: str):
        """
        Initialize scanner with Algorand node connection.
        
        Args:
            algod_address: Algorand node address
            algod_token: API token for Algorand node
        """
        self.algod_client = algod.AlgodClient(algod_token, algod_address)
        self.pattern_matcher = XSSPatternMatcher()

    def scan_contract(self, app_id: int) -> ScanResult:
        """
        Perform comprehensive XSS vulnerability scan on a smart contract.
        
        Args:
            app_id: Algorand application ID
            
        Returns:
            ScanResult containing all findings
        """
        vulnerabilities = []
        
        # Get contract info
        contract_info = self._get_contract_info(app_id)
        if contract_info:
            # Scan TEAL code
            teal_vulnerabilities = self._scan_teal_code(
                contract_info.get('params', {}).get('approval-program', '')
            )
            vulnerabilities.extend(teal_vulnerabilities)
            
            # Scan application state
            state_vulnerabilities = self._scan_application_state(app_id)
            vulnerabilities.extend(state_vulnerabilities)
        
        # Determine overall risk level
        risk_level = self._calculate_risk_level(vulnerabilities)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(vulnerabilities)
        
        return ScanResult(
            app_id=app_id,
            vulnerabilities=vulnerabilities,
            risk_level=risk_level,
            recommendations=recommendations,
            scan_timestamp=datetime.now().isoformat()
        )

    def _get_contract_info(self, app_id: int) -> Optional[Dict]:
        """Get smart contract information from Algorand network."""
        try:
            return self.algod_client.application_info(app_id)
        except Exception as e:
            print(f"Error retrieving contract info: {e}")
            return None

    # ... (implementation of other private methods)