from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class SensorDataIn(BaseModel):
    id: str
    type: str
    subtype: str
    reading: int
    location: str
    timestamp: datetime

    class Config:
        orm_mode = True

class FilterSchema(BaseModel):
    id: Optional[List[str]] = None
    type: Optional[List[str]] = None
    subtype: Optional[List[str]] = None
    location: Optional[List[str]] = None

class MedianResponse(BaseModel):
    count: int
    median: float
