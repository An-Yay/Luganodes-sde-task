from db import engine, metadata


def run_migrations():   
    metadata.create_all(engine)
