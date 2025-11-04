# backend/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional

# --- Base Schemas ---

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class RoleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    role_name: str

class UserSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    role: RoleSchema

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# ------------------------------------

class VersionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    version_id: int
    version_name: str

class SchoolSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    school_id: int
    school_name: str

# This schema is used when reading a Student from the database
class StudentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    student_id: int
    student_name: str
    student_rarity: int
    student_is_limited: bool
    version: VersionSchema
    school: SchoolSchema

# --- Response Schemas ---
# These define the final JSON output, including dynamically generated fields.

class SchoolResponse(SchoolSchema):
    image_url: Optional[str] = None

class StudentResponse(StudentSchema):
    portrait_url: Optional[str] = None
    artwork_url: Optional[str] = None
