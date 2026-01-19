from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from .StudentResponse import StudentResponse

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

# --- Response
class BannerResponse(BannerSchema):
    image_url: Optional[str] = None

# --- Response
class BannerDetailResponse(BannerResponse):
    pickup_r3_students: List[StudentResponse]
    nonpickup_r3_students: List[StudentResponse]
    r2_students: List[StudentResponse]
    r1_students: List[StudentResponse]