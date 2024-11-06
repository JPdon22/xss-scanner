"""
Configuration settings for the Algorand XSS Scanner.
Contains environment-specific settings and constants.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Algorand node configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "localnet")

if ENVIRONMENT == "localnet":
    ALGOD_ADDRESS = "http://localhost:4001"
    ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
else:
    ALGOD_ADDRESS = os.getenv("ALGOD_ADDRESS", "https://testnet-api.algonode.cloud")
    ALGOD_TOKEN = os.getenv("ALGOD_TOKEN", "")

# XSS detection patterns
XSS_PATTERNS = [
    r"<script\b[^>]*>(.*?)</script>",
    r"javascript:",
    r"onerror=",
    r"onload=",
    r"eval\(",
    r"document\.cookie",
]

# Risk level definitions
RISK_LEVELS = {
    "HIGH": "High",
    "MEDIUM": "Medium",
    "LOW": "Low"
}

# Vulnerability Database API configuration
VULN_API_KEY = os.getenv("VULN_API_KEY")
VULN_API_ENABLED = os.getenv("VULN_API_ENABLED", "false").lower() == "true"
