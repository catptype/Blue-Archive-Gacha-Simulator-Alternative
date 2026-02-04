from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

from .GachaResponse import GachaPresetSchema
from .StudentResponse import StudentResponse

class BannerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    include_limited: bool
    preset: GachaPresetSchema

class BannerResponse(BannerSchema):
    image_url: Optional[str] = None

class BannerDetailResponse(BannerResponse):
    pickup_r3_students: List[StudentResponse]
    nonpickup_r3_students: List[StudentResponse]
    r2_students: List[StudentResponse]
    r1_students: List[StudentResponse]