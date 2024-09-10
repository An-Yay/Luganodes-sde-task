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
