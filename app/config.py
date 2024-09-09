from dotenv import load_dotenv
import os


load_dotenv()


class Config:
    ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    BEACON_DEPOSIT_CONTRACT_ADDRESS = os.getenv(
        "BEACON_DEPOSIT_CONTRACT_ADDRESS")
    TELEGRAM_NOTIFICATIONS_BOT_TOKEN = os.getenv(
        "TELEGRAM_NOTIFICATIONS_BOT_TOKEN")
    TELEGRAM_NOTIFICATIONS_CHAT_ID = os.getenv(
        "TELEGRAM_NOTIFICATIONS_CHAT_ID")


config = Config()
