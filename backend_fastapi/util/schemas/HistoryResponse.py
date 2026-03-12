from datetime import datetime
from pydantic import BaseModel
from typing import List

from .BannerResponse import BannerResponse
from .StudentResponse import StudentResponse

class TransactionSchema(BaseModel):
    id: int
    create_on: datetime
    student: StudentResponse
    banner: BannerResponse

class HistoryResponse(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    limit: int
    items: List[TransactionSchema]