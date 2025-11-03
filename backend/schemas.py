# backend/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional

# --- Base Schemas ---

class VersionSchema(BaseModel):
    # This replaces the old `class Config: orm_mode = True`
    model_config = ConfigDict(from_attributes=True)

    version_name: str

class SchoolSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    school_name: str

# This schema is used when reading a Student from the database
class StudentFromDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    student_id: int
    student_name: str
    student_rarity: int
    student_is_limited: bool
    version: VersionSchema
    school: SchoolSchema
    asset: Optional[object] # We just need to know if it exists, not its data


# --- Response Schemas ---
# These define the final JSON output, including dynamically generated fields.

class SchoolResponse(SchoolSchema):
    # This model doesn't need to read from the DB, so no config is strictly needed,
    # but it's good practice to inherit it.
    school_id: int
    image_url: Optional[str] = None

class StudentResponse(BaseModel):
    student_id: int
    student_name: str
    student_rarity: int
    student_is_limited: bool
    version: VersionSchema
    school: SchoolResponse # Notice this now uses the response schema for School
    portrait_url: Optional[str] = None
    artwork_url: Optional[str] = None