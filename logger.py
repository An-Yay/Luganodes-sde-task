import logging

# Setup logger
logger = logging.getLogger("eth_tracker")
logger.setLevel(logging.INFO)

# Configure logging format
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
