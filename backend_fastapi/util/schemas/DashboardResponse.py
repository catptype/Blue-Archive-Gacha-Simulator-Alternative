from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, List

from .StudentResponse import StudentResponse

#############################
#     Dashboard Schemas     #
#############################

class LuckGapsSchema(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None
    avg: Optional[float] = None

class RarityCounterSchema(BaseModel):
    r3_count: int
    r2_count: int
    r1_count: int

class BannerBreakdownSchema(BaseModel):
    data: Dict[str, RarityCounterSchema]

class TopStudentSchema(BaseModel):
    student: StudentResponse
    count: int
    first_obtained_on: datetime

class FirstR3Schema(BaseModel):
    student: StudentResponse
    obtained_on: datetime

class ProgressionSchema(BaseModel):
    rarity: int
    obtained: int
    total: int

class R3MilestoneSchema(BaseModel):
    student: StudentResponse 
    pull_number: int

class LuckPerformanceSchema(BaseModel):
    banner_name: str
    total_pulls: int
    r3_count: int
    user_rate: float
    banner_rate: float
    luck_variance: float
    gaps: Optional[LuckGapsSchema] = None

class DashboardSummaryResponse(RarityCounterSchema):
    total_pulls: int
    total_pyroxene: int
    breakdown: BannerBreakdownSchema
    first_r3: FirstR3Schema
    top3: List[TopStudentSchema]
    progression: List[ProgressionSchema]
    milestone: List[R3MilestoneSchema]
    performance: List[LuckPerformanceSchema]

#####

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
    student: StudentResponse
    first_obtain_on: datetime

class CollectionProgressionResponse(BaseModel):
    rarity: int
    obtained: int
    total: int

class DistributionResponse(BaseModel):
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
