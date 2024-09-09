from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from config import config


load_dotenv()


engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

deposits = Table(
    "deposits", metadata,
    Column("hash", String, primary_key=True),
    Column("block_number", Integer, nullable=False),
    Column("block_timestamp", DateTime, nullable=False),
    Column("fee", String),
    Column("pubkey", String, nullable=False),
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
