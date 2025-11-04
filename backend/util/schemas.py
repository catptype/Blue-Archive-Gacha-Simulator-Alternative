# backend/schemas.py
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

from .models import Student
from fastapi import Request

# --- User Schemas ---

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

# --- Student Schemas ---

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

# --- Banner Schemas ---

class GachaPresetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    preset_id: int
    preset_name: str
    preset_pickup_rate: Decimal
    preset_r3_rate: Decimal
    preset_r2_rate: Decimal
    preset_r1_rate: Decimal

# --- Response Schemas ---
# These define the final JSON output, including dynamically generated fields.

class SchoolResponse(SchoolSchema):
    image_url: Optional[str] = None

class StudentResponse(StudentSchema):
    portrait_url: Optional[str] = None
    artwork_url: Optional[str] = None

class BannerDetailResponse(BaseModel):
    # This schema defines the exact structure the frontend wants.
    banner_id: int
    banner_name: str
    image_url: Optional[str] = None # We will compute this URL
    
    # Nested object for the preset details
    preset: GachaPresetSchema
    
    # Lists of students, using the StudentResponse schema you already have
    pickup_r3_students: List[StudentResponse]
    nonpickup_r3_students: List[StudentResponse]
    r2_students: List[StudentResponse]
    r1_students: List[StudentResponse]

def create_student_response(student: Student, request: Request) -> StudentResponse:
    school_response = SchoolResponse.model_validate(student.school)
    school_response.school_id = student.school.school_id
    if student.school.school_image:
        school_response.image_url = str(request.url_for('serve_school_image', school_id=student.school.school_id))

    student_response = StudentResponse(
        student_id=student.student_id,
        student_name=student.student_name,
        student_rarity=student.student_rarity,
        student_is_limited=student.student_is_limited,
        version=VersionSchema.model_validate(student.version),
        school=school_response
    )
    if student.asset:
        student_response.portrait_url = str(request.url_for('serve_student_image', student_id=student.student_id, image_type='portrait'))
        student_response.artwork_url = str(request.url_for('serve_student_image', student_id=student.student_id, image_type='artwork'))
    return student_response

