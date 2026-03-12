from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import List

from .AchievementResponse import AchievementResponse
from .StudentResponse import StudentResponse

class GachaPresetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    pickup_rate: Decimal
    r3_rate: Decimal
    r2_rate: Decimal
    r1_rate: Decimal

class GachaStudentSchema(BaseModel):
    student: StudentResponse
    is_pickup: bool
    is_new: bool

class GachaPullResponse(BaseModel):
    results: List[GachaStudentSchema]
    unlocked_achievements: List[AchievementResponse]