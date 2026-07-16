from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL Connection configuration
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12345678@127.0.0.1:3306/supply_chain_db"

# create_engine connects to the database. pool_pre_ping=True tests the connection before using it.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

# SessionLocal is the local session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all model classes
Base = declarative_base()

# Dependency to provide db session to endpoints, closed after request completes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
