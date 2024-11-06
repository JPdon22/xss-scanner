from algosdk import account, mnemonic
from algosdk.v2client import algod
import algosdk.transaction as txn
import time

def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print(f"Transaction {txid} confirmed in round {txinfo.get('confirmed-round')}.")
    return txinfo

def fund_contract_account(contract_address):
    """
    Fund your contract account from Pera testnet wallet
    """
    try:
        # TestNet connection
        algod_address = "https://testnet-api.algonode.cloud"
        algod_token = ""
        client = algod.AlgodClient(algod_token, algod_address)

        print("\nEnter your Pera Wallet testnet mnemonic (25 words)")
        print("Type each word and press Enter:")
        mnemonic_words = []
        for i in range(25):
            word = input(f"Word {i+1}: ").strip()
            mnemonic_words.append(word)

        sender_mnemonic = " ".join(mnemonic_words)
        sender_private_key = mnemonic.to_private_key(sender_mnemonic)
        sender_address = account.address_from_private_key(sender_private_key)

        # Check sender's balance
        account_info = client.account_info(sender_address)
        sender_balance = account_info.get('amount')
        print(f"\nYour testnet wallet balance: {sender_balance/1000000:.6f} Algos")

        # Standard amount for contract operation (1 Algo)
        amount = 1000000  # 1 Algo in microAlgos

        if sender_balance < amount + 1000:  # Adding extra for fees
            print(f"Error: Insufficient funds in testnet wallet. Please get testnet Algos from the faucet:")
            print("https://bank.testnet.algorand.network/")
            return

        # Get suggested parameters
        params = client.suggested_params()

        # Create and sign transaction
        unsigned_txn = txn.PaymentTxn(
            sender=sender_address,
            sp=params,
            receiver=contract_address,
            amt=amount
        )

        signed_txn = unsigned_txn.sign(sender_private_key)

        # Submit transaction
        tx_id = client.send_transaction(signed_txn)
        print(f"\nSending 1 Algo to contract account...")
        print(f"Transaction ID: {tx_id}")

        # Wait for confirmation using our custom function
        wait_for_confirmation(client, tx_id)

        # Show new balance
        contract_info = client.account_info(contract_address)
        print(f"\nContract account new balance: {contract_info['amount']/1000000:.6f} Algos")

        print("\nFunding successful!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    print("Enter the contract account address:")
    print("(This is the address you want to fund)")
    contract_address = input().strip()

    fund_contract_account(contract_address)
