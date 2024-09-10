from web3 import Web3
from sqlalchemy import insert, select
from datetime import datetime
from db import engine, deposits
from logger import logger
from config import config
from utils import retry
from notifications import TelegramNotifier
import logging
import time  # Import time module

# Initialize notifier
notifier = TelegramNotifier()

logging.getLogger('web3').setLevel(logging.DEBUG)

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(
    f"https://eth-mainnet.g.alchemy.com/v2/{config.ALCHEMY_API_KEY}"))

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
  
    try:
        block = w3.eth.get_block(block_number)
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
        transaction = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        fee = receipt.gasUsed * transaction.gasPrice

        pubkey = event['args']['pubkey'].hex()

        # Check if the deposit already exists
        with engine.connect() as conn:
            result = conn.execute(
                select(deposits).where(deposits.c.hash == tx_hash))
            if result.fetchone():
                logger.info(
                    f"Deposit with hash {tx_hash} already exists. Skipping...")
                return

        # Log deposit
        logger.info(
            f"Transaction Hash: {tx_hash}, Block: {block_number}, Timestamp: {timestamp}, Fee: {fee}, Pubkey: {pubkey}")

        # Store deposit
        with engine.begin() as conn:
            conn.execute(insert(deposits).values(
                hash=tx_hash,
                block_number=block_number,
                block_timestamp=timestamp,
                fee=str(fee),
                pubkey=pubkey,
            ))

        # Telegram notification
        notifier.send_message(
            f"New ETH Deposit:\nTx Hash: {tx_hash}\nBlock: {block_number}\nFee: {fee} Wei\nTimestamp: {timestamp}"
        )

    except Exception as e:
        logger.error(f"Error handling deposit event: {e}")


def start_tracking():
    logger.info("Starting Ethereum deposit tracker...")

    # Latest block 
    latest_block = w3.eth.get_block_number()
    logger.info(f"Starting from block: {latest_block}")

    while True:
        try:
            event_filter_params = {
                'fromBlock': latest_block,
                'address': config.BEACON_DEPOSIT_CONTRACT_ADDRESS,
            }

            # Log event filter
            logger.debug(f"Event filter params: {event_filter_params}")

            logs = w3.eth.get_logs(event_filter_params)
            for log in logs:
                event = contract.events.DepositEvent().process_log(log)
                handle_deposit_event(event)

            
            latest_block = w3.eth.get_block_number()

        except Exception as e:
            logger.error(f"Error during event processing: {e}")

        
        time.sleep(1000)  


if __name__ == "__main__":
    start_tracking()
