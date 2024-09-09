from web3 import Web3
from sqlalchemy import insert
from datetime import datetime
from db import engine, deposits
from logger import logger
from config import config
from utils import retry
import logging

# Enable detailed logging for Web3
logging.getLogger('web3').setLevel(logging.DEBUG)

# Initialize Web3 with Alchemy RPC using environment variable
w3 = Web3(Web3.HTTPProvider(
    f"https://eth-mainnet.g.alchemy.com/v2/iE6X9Ymmyo7Ym5aJwNmOVzqHnGrGpmka"))

# Deposit event ABI
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
    address=config.BEACON_DEPOSIT_CONTRACT_ADDRESS,
    abi=deposit_event_abi
)


@retry(max_attempts=5, delay=10)
def fetch_block_timestamp(block_number):
    """Fetch block timestamp."""
    try:
        block = w3.eth.get_block(block_number)  # Updated for Web3 v6.x.x
        return datetime.fromtimestamp(block['timestamp'])
    except Exception as e:
        logger.error(f"Error fetching block timestamp: {e}")
        raise


@retry(max_attempts=3, delay=2)
def handle_deposit_event(event):
    """Handle and process deposit events."""
    try:
        logger.info("New deposit detected!")

        # Fetch details
        tx_hash = event['transactionHash'].hex()
        block_number = event['blockNumber']
        timestamp = fetch_block_timestamp(block_number)

        # Calculate transaction fee
        transaction = w3.eth.get_transaction(
            tx_hash)  # Updated for Web3 v6.x.x
        receipt = w3.eth.get_transaction_receipt(
            tx_hash)  # Updated for Web3 v6.x.x
        fee = receipt.gasUsed * transaction.gasPrice

        pubkey = event['args']['pubkey'].hex()

        # Log deposit details
        logger.info(
            f"Transaction Hash: {tx_hash}, Block: {block_number}, Timestamp: {timestamp}, Fee: {fee}, Pubkey: {pubkey}")

        # Store deposit in the database
        with engine.begin() as conn:
            conn.execute(insert(deposits).values(
                hash=tx_hash,
                block_number=block_number,
                block_timestamp=timestamp,
                fee=str(fee),
                pubkey=pubkey,
            ))
    except Exception as e:
        logger.error(f"Error handling deposit event: {e}")


def start_tracking():
    logger.info("Starting Ethereum deposit tracker...")

    # Latest block to start tracking from
    latest_block = w3.eth.get_block_number()  # Updated for Web3 v6.x.x
    logger.info(f"Starting from block: {latest_block}")

    while True:
        try:
            # Use w3.eth.get_logs to manually fetch logs (simplified filter params)
            event_filter_params = {
                'fromBlock': latest_block,  # Start from the most recent block
                'address': config.BEACON_DEPOSIT_CONTRACT_ADDRESS,
            }

            # Log the event filter parameters for debugging
            logger.debug(f"Event filter params: {event_filter_params}")

            # Updated for Web3 v6.x.x
            logs = w3.eth.get_logs(event_filter_params)
            for log in logs:
                event = contract.events.DepositEvent().process_log(log)
                handle_deposit_event(event)

            # Update the latest block
            latest_block = w3.eth.get_block_number()  # Updated for Web3 v6.x.x

        except Exception as e:
            logger.error(f"Error during event processing: {e}")


if __name__ == "__main__":
    start_tracking()
