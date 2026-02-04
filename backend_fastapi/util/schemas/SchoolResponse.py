from pydantic import BaseModel, ConfigDict
from typing import Optional

class SchoolSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

# --- Response
class SchoolResponse(SchoolSchema):
    image_url: Optional[str] = None