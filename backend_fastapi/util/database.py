import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define the default SQLite URL for local development.
DEFAULT_SQLITE_URL = "sqlite:///./db.sqlite3"

# 2. Get the database URL from an environment variable. If it's not set, use the default.
# This makes your app configurable for production without changing the code.
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# 3. Create a dictionary for engine arguments.
engine_args = {}
# The 'check_same_thread' argument is ONLY for SQLite.
if DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

# 4. Create the engine with the configurable URL and arguments.
engine = create_engine(DATABASE_URL, **engine_args)

# --- The rest of the file is unchanged ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
