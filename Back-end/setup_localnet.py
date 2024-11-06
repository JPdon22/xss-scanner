from algosdk.v2client import algod
from algosdk.transaction import PaymentTxn, wait_for_confirmation
from algosdk.account import generate_account
import json

def setup_localnet():
    # Connect to local Algorand node
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    client = algod.AlgodClient(algod_token, algod_address)

    # Create test account
    private_key, address = generate_account()

    # Get the dispenser account (first account in LocalNet)
    # This command assumes you're running sandbox or have access to the default funded account
    try:
        # Fund the account from dispenser
        dispenser_private_key = "your_dispenser_private_key"  # Replace with your LocalNet's funded account private key
        dispenser_address = "your_dispenser_address"  # Replace with your LocalNet's funded account address

        params = client.suggested_params()

        # Create funding transaction
        txn = PaymentTxn(
            sender=dispenser_address,
            sp=params,
            receiver=address,
            amt=10000000  # 10 Algos
        )

        # Sign and send transaction
        signed_txn = txn.sign(dispenser_private_key)
        tx_id = client.send_transaction(signed_txn)

        # Wait for confirmation
        wait_for_confirmation(client, tx_id, 4)

        # Get the new account info
        account_info = client.account_info(address)

        print("LocalNet is running and accessible")
        print("Test Account Created:")
        print(f"Address: {address}")
        print(f"Private Key: {private_key}")
        print(f"Account Balance: {account_info['amount']} microAlgos")
        print("Save these credentials for testing!")

    except Exception as e:
        print(f"Error setting up LocalNet: {str(e)}")

if __name__ == "__main__":
    setup_localnet()
