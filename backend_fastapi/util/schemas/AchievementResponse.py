from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class AchievementSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    category: str
    key: str

# --- Response
class AchievementResponse(AchievementSchema):
    image_url: Optional[str] = None

# --- Response
class UserAchievementResponse(AchievementResponse):
    # User-specific augmented data
    is_unlocked: bool
    unlocked_on: Optional[datetime] = None