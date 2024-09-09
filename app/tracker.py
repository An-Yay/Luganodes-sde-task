from web3 import Web3
from web3.middleware import geth_poa_middleware
from sqlalchemy import insert
from datetime import datetime
from db import engine, deposits
from logger import logger
from config import config
from utils import retry

# Alchemy RPC
w3 = Web3(Web3.HTTPProvider(
    f"https://eth-mainnet.alchemyapi.io/v2/{config.ALCHEMY_API_KEY}"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Deposit event 
deposit_event_abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "pubkey", "type": "bytes"},
            {"indexed": False, "name": "withdrawal_credentials", "type": "bytes"},
            {"indexed": False, "name": "amount", "type": "bytes"},
            {"indexed": False, "name": "signature", "type": "bytes"},
            {"indexed": False, "name": "index", "type": "bytes"}
        ],
        "name": "DepositEvent",
        "type": "event"
    }
]

# Beacon Deposit Contract 
contract = w3.eth.contract(
    address=config.BEACON_DEPOSIT_CONTRACT_ADDRESS, abi=deposit_event_abi)


@retry(max_attempts=5, delay=10)
def fetch_block_timestamp(block_number):
    
    block = w3.eth.getBlock(block_number)
    return datetime.fromtimestamp(block.timestamp)


@retry(max_attempts=3, delay=2)
def handle_deposit_event(event):
    
    logger.info("New deposit detected!")

    # Fetch details
    tx_hash = event['transactionHash'].hex()
    block_number = event['blockNumber']
    timestamp = fetch_block_timestamp(block_number)

    # Calculate transaction fee
    transaction = w3.eth.getTransaction(tx_hash)
    receipt = w3.eth.getTransactionReceipt(tx_hash)
    fee = receipt.gasUsed * transaction.gasPrice

    pubkey = event['args']['pubkey'].hex()

    # Log
    logger.info(
        f"Transaction Hash: {tx_hash}, Block: {block_number}, Timestamp: {timestamp}")

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

    
    deposit_filter = contract.events.DepositEvent().createFilter(fromBlock="latest")

    while True:
        try:
            events = deposit_filter.get_new_entries()
            for event in events:
                handle_deposit_event(event)
        except Exception as e:
            logger.error(f"Error during event processing: {e}")
