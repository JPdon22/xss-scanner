from algosdk.v2client import algod
from algosdk import account
import sys

def test_contract(private_key):
    try:
        # Connect to local Algorand node
        algod_address = "http://localhost:4001"
        algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        client = algod.AlgodClient(algod_token, algod_address)

        # Get account address from private key
        address = account.address_from_private_key(private_key)

        # Check account balance before proceeding
        account_info = client.account_info(address)
        balance = account_info['amount']

        if balance < 1000:  # Minimum balance needed
            print(f"Error: Insufficient funds. Account balance: {balance} microAlgos")
            print("Please make sure the account is funded before deploying the contract")
            return

        # Your contract deployment code here
        # ...

    except Exception as e:
        print(f"Error in test_contract: {str(e)}")
        print("\nDebugging information:")
        print(f"Account address: {address}")
        print(f"Current balance: {balance if 'balance' in locals() else 'unknown'} microAlgos")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        private_key = sys.argv[1]
    else:
        private_key = input("Enter the private key from setup_localnet.py: ")

    test_contract(private_key)
