from datetime import datetime
from decimal import Decimal
from fastapi import Request
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict

from .models import Student

#############################
#       User Schemas        #
#############################

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

#############################
#      Student Schemas      #
#############################

class VersionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    version_id: int
    version_name: str

class SchoolSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    school_id: int
    school_name: str

# --- Response
class SchoolResponse(SchoolSchema):
    image_url: Optional[str] = None

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

#############################
#       Gacha Schemas       #
#############################

class GachaPresetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    preset_id: int
    preset_name: str
    preset_pickup_rate: Decimal
    preset_r3_rate: Decimal
    preset_r2_rate: Decimal
    preset_r1_rate: Decimal

class BannerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    banner_id: int
    banner_name: str
    banner_include_limited: bool
    preset: GachaPresetSchema

class GachaResultStudent(StudentResponse):
    is_pickup: bool
    is_new: bool

# --- Response
class BannerResponse(BannerSchema):
    image_url: Optional[str] = None

# --- Response
class BannerDetailResponse(BannerResponse):
    pickup_r3_students: List[StudentResponse]
    nonpickup_r3_students: List[StudentResponse]
    r2_students: List[StudentResponse]
    r1_students: List[StudentResponse]

#############################
#     Dashboard Schemas     #
#############################

class LuckGapsSchema(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None
    avg: Optional[float] = None

class OverallRaritySchema(BaseModel):
    r3_count: int
    r2_count: int
    r1_count: int

# --- Response
class DashboardKpiResponse(OverallRaritySchema):
    total_pulls: int
    total_pyroxene_spent: int

# --- Response
class TopStudentResponse(BaseModel):
    student: StudentResponse
    count: int
    first_obtained: datetime

# --- Response
class FirstR3Response(BaseModel):
    transaction_id: int
    transaction_create_on: datetime
    student: StudentResponse

# --- Response
class CollectionProgressionResponse(BaseModel):
    rarity: int
    obtained: int
    total: int

# --- Response
class BannerBreakdownChartResponse(BaseModel):
    data: Dict[str, OverallRaritySchema]

# --- Response
class MilestoneResponse(BaseModel):
    student: StudentResponse 
    pull_number: int

# --- Response
class LuckPerformanceResponse(BaseModel):
    banner_name: str
    total_pulls: int
    r3_count: int
    user_rate: float
    banner_rate: float
    luck_variance: float
    gaps: Optional[LuckGapsSchema] = None

#############################
#      History Schemas      #
#############################

class TransactionSchema(FirstR3Response): # Reuse from FirstR3 because it similar to gacha transaction
    banner: BannerResponse

# --- The main paginated response schema ---
class HistoryResponse(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    limit: int
    items: List[TransactionSchema]

#############################
#     Collection Schemas    #
#############################

class CollectionStudentSchema(StudentResponse):
    is_obtained: bool

# --- Response
class CollectionResponse(BaseModel):
    obtained_count: int
    total_students: int
    completion_percentage: float
    students: List[CollectionStudentSchema]

#############################
#    Achievement Schemas    #
#############################
class AchievementSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    achievement_id: int
    achievement_name: str
    achievement_description: str
    achievement_category: str
    achievement_key: str

# --- Response
class AchievementResponse(AchievementSchema):
    image_url: Optional[str] = None

#############################
#       Mixing Schemas      #
#############################

# --- Response    
class GachaPullResponse(BaseModel):
    success: bool
    results: List[GachaResultStudent]
    unlocked_achievements: List[AchievementResponse]


















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
