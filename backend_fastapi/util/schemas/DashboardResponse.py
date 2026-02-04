from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict

from .StudentResponse import StudentResponse

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

class KpiResponse(OverallRaritySchema):
    total_pulls: int
    total_pyroxene_spent: int

class Top3StudentResponse(BaseModel):
    student: StudentResponse
    count: int
    first_obtained: datetime

class FirstR3Response(BaseModel):
    transaction_id: int
    transaction_create_on: datetime
    student: StudentResponse

class CollectionProgressionResponse(BaseModel):
    rarity: int
    obtained: int
    total: int

class BannerBreakdownChartResponse(BaseModel):
    data: Dict[str, OverallRaritySchema]

class MilestoneResponse(BaseModel):
    student: StudentResponse 
    pull_number: int

class LuckPerformanceResponse(BaseModel):
    banner_name: str
    total_pulls: int
    r3_count: int
    user_rate: float
    banner_rate: float
    luck_variance: float
    gaps: Optional[LuckGapsSchema] = None