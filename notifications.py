from notifications import TelegramNotifier
import requests
from config import config
from logger import logger


class TelegramNotifier:
    def __init__(self):
        self.bot_token = config.TELEGRAM_NOTIFICATIONS_BOT_TOKEN
        self.chat_id = config.TELEGRAM_NOTIFICATIONS_CHAT_ID

    def send_message(self, message):
        """Send a message to the configured Telegram chat."""
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram notification: {e}")




notifier = TelegramNotifier()


def handle_deposit_event(event):
   
    logger.info("New deposit detected!")

    # Fetch details
    tx_hash = event['transactionHash'].hex()
    block_number = event['blockNumber']
    timestamp = fetch_block_timestamp(block_number)

    
    transaction = w3.eth.getTransaction(tx_hash)
    receipt = w3.eth.getTransactionReceipt(tx_hash)
    fee = receipt.gasUsed * transaction.gasPrice

    pubkey = event['args']['pubkey'].hex()

    # Log
    logger.info(
        f"Transaction Hash: {tx_hash}, Block: {block_number}, Timestamp: {timestamp}")

    # Insert into the database
    with engine.begin() as conn:
        conn.execute(insert(deposits).values(
            hash=tx_hash,
            block_number=block_number,
            block_timestamp=timestamp,
            fee=str(fee),
            pubkey=pubkey,
        ))

    
    notifier.send_message(
        f"New ETH Deposit:\nTx Hash: {tx_hash}\nBlock: {block_number}\nAmount: {fee} Wei")
