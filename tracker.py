from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
import os
from sqlalchemy import insert
from datetime import datetime
from db import engine
from migrations import deposits
from logger import logger

# Load environment variables
load_dotenv()

ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
BEACON_DEPOSIT_CONTRACT_ADDRESS = os.getenv("BEACON_DEPOSIT_CONTRACT_ADDRESS")

# ABI for the Deposit event (simplified)
deposit_event_abi = [
    "event DepositEvent(bytes pubkey, bytes withdrawal_credentials, bytes amount, bytes signature, bytes index)"
]

# Create a Web3 instance
w3 = Web3(Web3.HTTPProvider(
    f"https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_API_KEY}"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Initialize contract
contract = w3.eth.contract(
    address=BEACON_DEPOSIT_CONTRACT_ADDRESS, abi=deposit_event_abi)


def handle_deposit_event(event):
    logger.info("New deposit detected!")

    tx_hash = event['transactionHash'].hex()
    block_number = event['blockNumber']
    block = w3.eth.getBlock(block_number)
    timestamp = datetime.fromtimestamp(block.timestamp)

    # Example: Calculate gas fee
    transaction = w3.eth.getTransaction(tx_hash)
    receipt = w3.eth.getTransactionReceipt(tx_hash)
    fee = receipt.gasUsed * transaction.gasPrice

    pubkey = event['args']['pubkey'].hex()

    logger.info(
        f"Transaction Hash: {tx_hash}, Block: {block_number}, Timestamp: {timestamp}")

    # Insert the deposit into the database
    with engine.begin() as conn:
        conn.execute(insert(deposits).values(
            hash=tx_hash,
            block_number=block_number,
            block_timestamp=timestamp,
            fee=str(fee),
            pubkey=pubkey,
        ))


def start_tracking():
    logger.info("Starting Ethereum deposit tracker...")

    # Subscribe to deposit events
    contract.events.DepositEvent().on('data', handle_deposit_event).on(
        'error', lambda e: logger.error(e))

    # Start listening
    while True:
        try:
            w3.eth.filter(
                {"fromBlock": "latest", "address": BEACON_DEPOSIT_CONTRACT_ADDRESS}).get_new_entries()
        except Exception as e:
            logger.error(f"Error fetching new events: {e}")
      