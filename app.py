from tracker import start_tracking
from migrations import run_migrations
from logger import logger
from prometheus_client import start_http_server, Counter

deposit_counter = Counter('deposit_total', 'Number of ETH deposits tracked')



def main():
   
    try:
        start_http_server(8000) # Starting prometheus
        logger.info("Running migrations...")
        run_migrations()

        logger.info("Starting deposit tracking...")
        start_tracking()

    except Exception as e:
        logger.error(f"Critical error: {e}")


if __name__ == "__main__":
    main()
