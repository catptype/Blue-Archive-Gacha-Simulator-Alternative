import bcrypt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models
from .database import get_db
from ..config import settings

# --- NEW: An OAuth2 scheme that does NOT automatically throw an error ---
# This is the key. If the Authorization header is missing, it will pass `None` to the dependency.
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token", auto_error=False)
required_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# --- Password Utilities ---
def get_password_hash(password: str) -> str:
    """Hashes a password and returns it as a string for database storage."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    
    # Decode the bytes into a string before returning
    return hashed_password_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password_from_db: str) -> bool:
    """Verifies a plain password against a hashed password string from the database."""
    plain_password_bytes = plain_password.encode('utf-8')
    
    # Encode the string from DB back into bytes for comparison
    hashed_password_bytes = hashed_password_from_db.encode('utf-8')
    
    return bcrypt.checkpw(password=plain_password_bytes, hashed_password=hashed_password_bytes)

# --- JWT Utilities ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# --- Dependencies functions ---

# ----- Shared logic ---
def _get_user_from_token(token: str, db: Session) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter_by(username=username).first()
    if user is None:
        raise credentials_exception
    return user

# --- The dependencies used by FastAPI ---
def get_optional_current_user(token: str | None = Depends(optional_oauth2_scheme), db: Session = Depends(get_db)) -> models.User | None:
    if token is None: 
        return None
    return _get_user_from_token(token, db)

def get_required_current_user(token: str = Depends(required_oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    return _get_user_from_token(token, db)
