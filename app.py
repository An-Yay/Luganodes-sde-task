from tracker import start_tracking
from migrations import run_migrations
from logger import logger



def main():
   
    try:
        logger.info("Running migrations...")
        run_migrations()

        logger.info("Starting deposit tracking...")
        start_tracking()
    except Exception as e:
        logger.error(f"Critical error: {e}")


if __name__ == "__main__":
    main()
