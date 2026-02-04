from pydantic import BaseModel
from typing import List

from .StudentResponse import StudentResponse

class CollectionStudentSchema(StudentResponse):
    is_obtained: bool

# --- Response
class CollectionResponse(BaseModel):
    obtained_count: int
    total_students: int
    completion_percentage: float
    students: List[CollectionStudentSchema]
