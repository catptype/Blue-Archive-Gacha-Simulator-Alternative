from fastapi import Request
from pydantic import BaseModel, ConfigDict
from typing import Optional
from ..models import Student
from .SchoolResponse import SchoolResponse

class VersionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    version_id: int
    version_name: str

class StudentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    student_id: int
    student_name: str
    student_rarity: int
    student_is_limited: bool
    version: VersionSchema
    school: SchoolResponse

# --- Response
class StudentResponse(StudentSchema):
    portrait_url: Optional[str] = None
    artwork_url: Optional[str] = None

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