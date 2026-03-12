from fastapi import Request
from pydantic import BaseModel, ConfigDict
from typing import Optional
from ..models import Student
from .SchoolResponse import SchoolResponse

class VersionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class StudentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    rarity: int
    is_limited: bool
    version: VersionSchema
    school: SchoolResponse

# --- Response
class StudentResponse(StudentSchema):
    portrait_url: Optional[str] = None
    artwork_url: Optional[str] = None

def create_student_response(student: Student, request: Request) -> StudentResponse:
    school_response = SchoolResponse.model_validate(student.school)
    school_response.id = student.school.id
    if student.school.image_data:
        school_response.image_url = str(request.url_for('serve_school_image', school_id=student.school.id))

    student_response = StudentResponse(
        id=student.id,
        name=student.name,
        rarity=student.rarity,
        is_limited=student.is_limited,
        version=VersionSchema.model_validate(student.version),
        school=school_response
    )
    if student.asset:
        student_response.portrait_url = str(request.url_for('serve_student_image', student_id=student.id, image_type='portrait'))
        student_response.artwork_url = str(request.url_for('serve_student_image', student_id=student.id, image_type='artwork'))
    return student_response