import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

api_key = os.getenv("VULN_API_KEY")
if api_key is None:
    raise ValueError("API_KEY is not set in the environment variables.")

def fetch_vulndb_data(contract_teal):
    url = "https://api.vulndb.com/v1/vulnerabilities"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "contract": contract_teal
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        vulnerabilities = response.json()
        for vuln in vulnerabilities:
          vuln['risk_level'] = "High" if vuln['risk_score'] > 7 else "Medium" if vuln['risk_score'] > 4 else "Low"
          vuln['recommendations'] = vuln.get('recommendations', [])
          return vulnerabilities
    else:
        return None


def scan_app_state(app_state):
    url = "https://api.vulndb.com/v1/vulnerabilities"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }

    data = {
        "app_state": app_state
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example usage:
# contract_teal = """
# #pragma version 2
# txn TypeEnum
# int 1
# ==
# bnz main_l1
# err

# main_l1:
# ...
# """

# vulnerabilities = fetch_vulndb_data(contract_teal)
# if vulnerabilities:
#     print("Vulnerabilities found:", vulnerabilities)
# else:
#     print("No vulnerabilities found or there was an error with the API request.")
