from algosdk import account

# Your private key from setup_localnet.py
private_key = "GhRPjqFVPC8IbOgO0BQ6nHi+ThrbTadT/REFwEV342dFCie0mBcupfReYFDuOi1sj1phw54Yl4lcfH0PKCVe4g=="

# Get the address
address = account.address_from_private_key(private_key)
print("\nYour contract address is:")
print(address)

# Save this for later use
with open("contract_address.txt", "w") as f:
    f.write(address)
print("\nAddress has been saved to contract_address.txt")
