import logging


def setup_logger(name):
    """Set up a logger with standard configuration."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    
    handler = logging.StreamHandler()

    # format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

logger = setup_logger("eth_tracker")
