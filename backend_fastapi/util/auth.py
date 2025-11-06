import bcrypt
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models
from .database import get_db

# --- Configuration ---
# You should use environment variables for these in a real application
SECRET_KEY = os.environ.get("SECRET_KEY", "a_very_secret_key_that_should_be_in_env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- NEW: An OAuth2 scheme that does NOT automatically throw an error ---
# This is the key. If the Authorization header is missing, it will pass `None` to the dependency.
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token", auto_error=False)

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

def get_optional_current_user(token: str | None = Depends(optional_oauth2_scheme), db: Session = Depends(get_db)) -> models.User | None:
    """
    Dependency that returns the User object from the token if present, otherwise returns None.
    """
    if token is None:
        return None # Guest user

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            return None # Or raise credentials_exception if you want to reject bad tokens
    except JWTError:
        return None # Or raise credentials_exception

    user = db.query(models.User).filter(models.User.username == username).first()
    return user