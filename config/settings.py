"""
Configuration settings for the Algorand XSS Scanner.
Contains environment-specific settings and constants.
"""

# AlgoKit LocalNet connection settings
ALGOD_ADDRESS = "http://localhost:4001"  # This is already correct for AlgoKit LocalNet
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  # AlgoKit LocalNet default token

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