import requests

def fetch_vulndb_data(contract_teal):
    url = "https://api.vulndb.com/v1/vulnerabilities"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }

    data = {
        "contract": contract_teal
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
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
