import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt

import bcrypt

# --- Configuration ---
# You should use environment variables for these in a real application
SECRET_KEY = os.environ.get("SECRET_KEY", "a_very_secret_key_that_should_be_in_env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str) -> str:
    """Hashes a password and returns it as a string for database storage."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    # CRITICAL: Decode the bytes into a string before returning
    return hashed_password_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password_from_db: str) -> bool:
    """Verifies a plain password against a hashed password string from the database."""
    plain_password_bytes = plain_password.encode('utf-8')
    # CRITICAL: Encode the string from the DB back into bytes for comparison
    hashed_password_bytes = hashed_password_from_db.encode('utf-8')
    return bcrypt.checkpw(password=plain_password_bytes, hashed_password=hashed_password_bytes)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt