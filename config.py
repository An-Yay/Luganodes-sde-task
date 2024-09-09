from dotenv import load_dotenv
import os


load_dotenv()


class Config:
    ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    BEACON_DEPOSIT_CONTRACT_ADDRESS = os.getenv(
        "BEACON_DEPOSIT_CONTRACT_ADDRESS")


config = Config()
