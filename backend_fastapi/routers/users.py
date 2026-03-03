from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

from ..util.models import User, Role
from ..util.auth import create_access_token, get_required_current_user, get_password_hash, verify_password
from ..util.schemas.User import UserCreate, UserSchema, Token
from ..util.database import get_db

router = APIRouter()

# --- Helper functions

def is_username_exist(db: Session, username:str) -> bool:
    return db.query(User).filter_by(username=username).first() is not None

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter_by(username=username).first()
    if not user: return False
    if not verify_password(password, user.hashed_password): return False
    return user

# --- Endpoints ---

@router.post("/register", tags=["users"], response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    
    if is_username_exist(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check role 'member'
    member_obj = db.query(Role).filter_by(name="member").first()
    if not member_obj:
        raise HTTPException(status_code=500, detail="Default user role 'member' not configured on server.")

    hashed_password = get_password_hash(user.password)
    
    new_user = User(
        username=user.username, 
        hashed_password=hashed_password,
        role_id=member_obj.id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token", tags=["users"], response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Check username and password
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", tags=["users"], response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_required_current_user)):
    """
    Fetches the data for the currently authenticated user.
    If the token is invalid or expired, this endpoint will automatically
    return a 401 Unauthorized error.
    """
    return current_user