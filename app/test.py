from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://eth-mainnet.alchemyapi.io/v2/<API_KEY>"))

# Test basic connection
latest_block = w3.eth.blockNumber
print(f"Latest block: {latest_block}")