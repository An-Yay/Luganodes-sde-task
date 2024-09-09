from db import engine, metadata
def run_migrations():
    """Run database migrations."""
    metadata.create_all(engine)
