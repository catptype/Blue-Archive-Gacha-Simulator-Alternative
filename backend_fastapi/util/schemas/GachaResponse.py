from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import List

from .AchievementResponse import AchievementResponse
from .StudentResponse import StudentResponse

class GachaPresetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    preset_id: int
    preset_name: str
    preset_pickup_rate: Decimal
    preset_r3_rate: Decimal
    preset_r2_rate: Decimal
    preset_r1_rate: Decimal

class GachaResultStudent(StudentResponse):
    is_pickup: bool
    is_new: bool

class GachaPullResponse(BaseModel):
    success: bool
    results: List[GachaResultStudent]
    unlocked_achievements: List[AchievementResponse]